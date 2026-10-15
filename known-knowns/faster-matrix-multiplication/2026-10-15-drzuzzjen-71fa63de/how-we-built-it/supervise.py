#!/usr/bin/env python3
"""Windows-native supervisor for one V3R1T4S cycle. Launches worker jobs at BELOW_NORMAL priority, records the
exact owned processes (pid + create_time), enforces a hard deadline, honours PAUSE (suspend/resume owned
processes) and STOP (graceful early stop), measures aggregate RSS against a memory budget, and keeps a
workspace-local lock. It never touches a process it did not start; ownership is verified by create_time
before every suspend/resume/kill, and termination goes through the Popen handle.

usage: supervise.py --run RUNDIR --jobs JOBS.json --deadline-utc 2026-10-14T21:15:00Z --workers 28 --mem-gib 44
JOBS.json: [{"lens":..., "file":..., "ref":..., "seed":..., "out":...}, ...]  (out = attempts/<lens>/output)
State: RUNDIR/supervisor_state.json (atomic). Log: RUNDIR/supervisor.log.
"""
import argparse, json, os, subprocess, sys, time, datetime as dt
import psutil

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
VENV = os.path.join(WS, ".venv")


def base_python():
    """The venv's Scripts\\python.exe on Windows is a launcher that runs the base interpreter as a CHILD process,
    so the pid we would own is not the one computing. Run the base interpreter directly with the venv's
    site-packages on PYTHONPATH; then the owned pid is the worker itself."""
    home = None
    for line in open(os.path.join(VENV, "pyvenv.cfg"), encoding="utf-8"):
        if line.lower().startswith("home"):
            home = line.split("=", 1)[1].strip()
    exe = os.path.join(home, "python.exe") if home else sys.executable
    return exe if os.path.exists(exe) else sys.executable


PY = base_python()
SITE = os.path.join(VENV, "Lib", "site-packages")


def utc(ts=None):
    return dt.datetime.fromtimestamp(ts if ts is not None else time.time(), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--jobs", required=True)
    ap.add_argument("--deadline-utc", required=True)
    ap.add_argument("--workers", type=int, required=True)
    ap.add_argument("--mem-gib", type=float, required=True)
    ap.add_argument("--grace", type=float, default=20.0, help="seconds between terminate and kill")
    ap.add_argument("--adopt", help="state file of a previous supervisor of THIS run whose recorded workers are still "
                                    "running; they count toward the cap and are paused/stopped like our own")
    a = ap.parse_args()
    run = os.path.abspath(a.run)
    deadline = dt.datetime.strptime(a.deadline_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp()
    lock = os.path.join(WS, ".lock")
    try:
        os.mkdir(lock)
    except FileExistsError:
        print("refusing: %s exists (another cycle is running?)" % lock, file=sys.stderr)
        sys.exit(2)
    me = psutil.Process()
    with open(os.path.join(lock, "supervisor.json"), "w") as f:
        json.dump({"pid": me.pid, "create_time": me.create_time(), "run": run, "started": utc()}, f)
    logf = open(os.path.join(run, "supervisor.log"), "a", encoding="utf-8")

    def log(msg):
        line = "%s %s" % (utc(), msg)
        logf.write(line + "\n"); logf.flush()
        print(line, flush=True)

    jobs = json.load(open(a.jobs, encoding="utf-8"))
    queue = list(enumerate(jobs))
    running = {}  # idx -> dict(proc, pid, create_time, job, started)
    adopted = []  # records from a crashed supervisor of this run: verified by pid + create_time, no Popen handle
    if a.adopt:
        for r in json.load(open(a.adopt, encoding="utf-8")).get("running", []):
            try:
                p = psutil.Process(r["pid"])
                if abs(p.create_time() - r["create_time"]) < 1.0:
                    adopted.append(r)
            except psutil.Error:
                pass
    done = []
    state_path = os.path.join(run, "supervisor_state.json")
    budget = a.mem_gib * 1024 ** 3
    paused = False
    env = dict(os.environ, PYTHONUTF8="1", NUMBA_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1",
               OPENBLAS_NUM_THREADS="1", PYTHONPATH=SITE, VIRTUAL_ENV=VENV)
    flags = getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0) | getattr(subprocess, "CREATE_NO_WINDOW", 0)

    def owned(rec):
        try:
            p = psutil.Process(rec["pid"])
            return p if abs(p.create_time() - rec["create_time"]) < 1.0 else None
        except psutil.Error:
            return None

    def owned_tree(rec):
        """The owned process plus its descendants (a launcher's child, numba helpers): all started by us."""
        p = owned(rec)
        if p is None:
            return []
        try:
            return [p] + p.children(recursive=True)
        except psutil.Error:
            return [p]

    def write_state(extra=None):
        st = {"updated": utc(), "updated_epoch": time.time(), "deadline_utc": a.deadline_utc, "deadline_epoch": deadline,
              "workers_cap": a.workers, "mem_budget_gib": a.mem_gib, "paused": paused,
              "running": [{"idx": i, "pid": r["pid"], "create_time": r["create_time"], "job": r["job"], "started": r["started"]}
                          for i, r in running.items()],
              "adopted": [{"pid": r["pid"], "create_time": r["create_time"], "job": r["job"]} for r in adopted if owned(r)],
              "queued": len(queue), "done": done, "supervisor_pid": me.pid}
        if extra:
            st.update(extra)
        tmp = state_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(st, f, indent=1)
        for _ in range(20):  # Windows refuses os.replace while another process (the status view) has the file open
            try:
                os.replace(tmp, state_path)
                return
            except PermissionError:
                time.sleep(0.1)
        log("state write skipped: target busy")

    def launch(idx, job):
        out = os.path.join(run, job["out"])
        os.makedirs(out, exist_ok=True)
        job_deadline = min(deadline, time.time() + 60.0 * float(job.get("minutes", 1e9)))
        cmd = [PY, "-X", "utf8", os.path.join(HERE, "worker.py"), "--lens", job["lens"], "--file", job["file"],
               "--ref", str(job["ref"]), "--eligibility", os.path.join(run, "data_eligibility.md"),
               "--deadline", str(job_deadline), "--out", out, "--seed", str(job["seed"])]
        lg = open(os.path.join(out, "job%03d_%s_s%d.log" % (idx, os.path.basename(job["file"]).split("_ZT")[0], job["seed"])), "a")
        lg.write("%s %s\n" % (utc(), " ".join(cmd)))
        proc = subprocess.Popen(cmd, stdout=lg, stderr=subprocess.STDOUT, env=env, creationflags=flags, cwd=WS)
        rec = {"proc": proc, "pid": proc.pid, "create_time": psutil.Process(proc.pid).create_time(), "job": job,
               "started": utc(), "log": lg}
        running[idx] = rec
        log("launched job %d pid %d %s %s seed %d" % (idx, proc.pid, job["lens"], os.path.basename(job["file"]), job["seed"]))

    def stop_all(reason):
        log("stopping all owned processes: %s" % reason)
        for r in adopted:
            for p in reversed(owned_tree(r)):
                try:
                    p.resume(); p.terminate()
                except psutil.Error:
                    pass
        for i, r in list(running.items()):
            tree = owned_tree(r)
            for p in tree:
                try:
                    p.resume()
                except psutil.Error:
                    pass
            for p in reversed(tree):  # children first, then the owned parent
                try:
                    p.terminate()
                except psutil.Error:
                    pass
        t0 = time.time()
        while any(r["proc"].poll() is None for r in running.values()) and time.time() - t0 < a.grace:
            time.sleep(0.5)
        for i, r in list(running.items()):
            for p in reversed(owned_tree(r)):
                try:
                    p.kill()
                except psutil.Error:
                    pass
            done.append({"idx": i, "pid": r["pid"], "job": r["job"], "returncode": r["proc"].poll(), "ended": utc(), "stopped": reason})
            r["log"].close()
        running.clear()

    log("supervisor start: run=%s jobs=%d workers=%d mem_gib=%.1f deadline=%s" % (run, len(jobs), a.workers, a.mem_gib, a.deadline_utc))
    write_state()
    try:
        while True:
            now = time.time()
            if now >= deadline:
                stop_all("deadline"); break
            if os.path.exists(os.path.join(WS, "STOP")):
                stop_all("STOP file"); break
            want_pause = os.path.exists(os.path.join(WS, "PAUSE"))
            if want_pause != paused:
                for r in list(running.values()) + adopted:
                    for p in owned_tree(r):
                        try:
                            (p.suspend if want_pause else p.resume)()
                        except psutil.Error as e:
                            log("suspend/resume pid %d: %r" % (p.pid, e))
                paused = want_pause
                log("paused" if paused else "resumed")
            # reap finished
            for i, r in list(running.items()):
                rc = r["proc"].poll()
                if rc is not None:
                    done.append({"idx": i, "pid": r["pid"], "job": r["job"], "returncode": rc, "ended": utc()})
                    r["log"].close()
                    del running[i]
                    log("job %d pid %d exited rc=%s" % (i, r["pid"], rc))
            # memory
            rss = 0
            for r in list(running.values()) + adopted:
                for p in owned_tree(r):
                    try:
                        rss += p.memory_info().rss
                    except psutil.Error:
                        pass
            vm = psutil.virtual_memory()
            over = rss > budget or vm.available < 4 * 1024 ** 3
            if over:
                log("memory pressure: owned rss %.1f GiB, system available %.1f GiB" % (rss / 1024 ** 3, vm.available / 1024 ** 3))
            # launch
            adopted[:] = [r for r in adopted if owned(r) is not None]
            while not paused and not over and queue and len(running) + len(adopted) < a.workers and time.time() < deadline - 60:
                idx, job = queue.pop(0)
                launch(idx, job)
            write_state({"owned_rss_gib": round(rss / 1024 ** 3, 2), "system_available_gib": round(vm.available / 1024 ** 3, 2),
                         "cpu_percent": psutil.cpu_percent(interval=None), "load_sample_utc": utc()})
            if not running and not queue and not adopted:
                log("all jobs finished"); break
            time.sleep(5)
    finally:
        write_state({"finished": utc()})
        try:
            os.remove(os.path.join(lock, "supervisor.json")); os.rmdir(lock)
        except OSError as e:
            log("lock cleanup: %r" % e)
        log("supervisor end")


if __name__ == "__main__":
    main()
