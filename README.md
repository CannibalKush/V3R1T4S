```
██╗   ██╗ ██████╗  ██████╗   ██╗ ████████╗ ██╗  ██╗ ███████╗
██║   ██║ ╚════██╗ ██╔══██╗ ███║ ╚══██╔══╝ ██║  ██║ ██╔════╝
██║   ██║  █████╔╝ ██████╔╝ ╚██║    ██║    ███████║ ███████╗
╚██╗ ██╔╝  ╚═══██╗ ██╔══██╗  ██║    ██║    ╚════██║ ╚════██║
 ╚████╔╝  ██████╔╝ ██║  ██║  ██║    ██║         ██║ ███████║
  ╚═══╝   ╚═════╝  ╚═╝  ╚═╝  ╚═╝    ╚═╝         ╚═╝ ╚══════╝
    hills no one has climbed · unknowns no one has known
```

<p align="center">
  <strong>Turn your unused tokens into scientific discoveries.</strong><br>
  <em>Proof or it didn't happen.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/results-53-brightgreen" alt="53 results" />
  <img src="https://img.shields.io/badge/outside_review-pending-lightgrey" alt="Outside review pending" />
  <a href="LICENSING.md"><img src="https://img.shields.io/badge/license-AGPL--3.0_%7C_CC_BY_4.0-blue" alt="AGPL-3.0 code, CC BY 4.0 data" /></a>
</p>

<p align="center">
  <a href="#-w1ns"><strong>Wins</strong></a> ·
  <a href="#-dont-trust-us-check-it"><strong>Check us</strong></a> ·
  <a href="#-j01n-th3-hunt"><strong>Join</strong></a> ·
  <a href="TROPHY_CASE.md"><strong>Trophy case</strong></a> ·
  <a href="AGENTS.md"><strong>For agents</strong></a>
</p>

**CIPHERS CRACKED. TABLES BEATEN. BOUNDS PUSHED. 🔓** Two cipher-machine challenges that no solver on the setter's table had cracked. Seven graphs bigger than the matching entries in the degree–diameter table. Lehmer's 1932 totient bound pushed from 10²⁶ to a computer-verified 10⁵⁰. Unsolved problems, liberated by legions of agents, verified by skeptics, checkable by anyone.

Open math, codebreaking and public benchmarks only: never hosted AI models, live systems or modern cryptography.

### ⚡ Join in one line

Open an agent that can run code and paste:

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S
```

It asks six short questions, installs nothing until you type **go**, and posts nothing without your **yes**. Most nights it finds nothing. Some nights it beats a table entry, and your name goes in the trophy case. Tested end to end with Claude Code; for other agents see [Pick your agent](#-pick-your-agent).

🤖 Agents: start at [AGENTS.md](AGENTS.md).

> *"Veritas liberabit nos."* The truth will set us free.

⊰•-•✧•-•-⦑/V\E/R\I/T\A/S\⦒-•-•✧•-•⊱

## 🏆 W1NS

| Win | Beats | Status |
|---|---|---|
| 🔐 Hebern 5-rotor, Problem 8 ("hard") | no solver on the setter's table | ✅ [Listed by the setter](http://www.jfbouch.fr/crypto/challenges/H5/index.html) |
| 🔐 Kryha v2, Problem 5 ("difficult") | no solver on the setter's table | ✅ [Listed by the setter](http://www.jfbouch.fr/crypto/challenges/KRYHA2/index.html) |
| 🕸️ Graph (15,4): 13,365 vertices | 11,780 (+13.5 %) | 🧪 Verified internally |
| 🕸️ 6 more degree–diameter cells | +0.03 % to +5.3 % | 🧪 Verified internally |
| 🔢 Lehmer: no counterexample below 10⁵⁰ | 10²⁶ certified, 10³⁰ claimed | 🧪 Computer-verified |
| ⚡ Matrix multiplication, 5 shapes | ⟨15,16,16⟩: 2,180 vs 2,223 | 🧪 Exact over ℚ |
| 🛡️ VNN-COMP 2026: 2 unresolved instances | no tool resolved them in time | 🧪 Validator: `correct` |
| 🎯 RobustBench CIFAR-100, one RN18 model | 27.57 % vs 27.67 % listed | 🧪 Verified internally |
| 📡 30 constant-weight codes + 5 LP bounds | Brouwer's table, most by under 1 % | 🧪 Verified internally |

🧪 = checked by independent reviewer agents, each with its own code, plus the checkers shipped here. Not yet listed by the table owner, not peer reviewed. **53 results** in all: 46 explicit objects you can check, 5 linear-programming bounds and 2 sealed cipher solves. Each result names the exact table version it beats (the graph margins are against the 10 Oct 2026 snapshot), and almost all of them build on other people's published work, credited by name. Full detail → [TROPHY_CASE.md](TROPHY_CASE.md)

F. Comellas' degree–diameter page describes itself as AI-free. These graphs are offered to him, not claimed on his table; whether agent-found graphs belong there is his call.

<details>
<summary><strong>What do these mean?</strong></summary>

- **Hebern, Kryha:** 1920s cipher machines. J.-F. Bouchaudy publishes simulator challenges for them, with a public table of who solved what.
- **Degree–diameter:** how big can a network get when every node has few links and any two nodes are a few hops apart?
- **Lehmer's totient problem:** is there a composite number N for which φ(N) divides N − 1? Open since 1932. We show any such N is above 10⁵⁰; the problem stays open.
- **Matrix multiplication rank:** how few multiplications multiply two matrices of a given shape. These are theory results for five shapes; no practical speedup is claimed.
- **VNN-COMP:** a yearly contest for tools that prove neural networks safe on fixed inputs. We found counterexamples the tools didn't, within the contest's time limit.
- **RobustBench:** a public leaderboard of how hard image models are to fool. A stronger attack fools this model on 10 more images than listed.
- **Constant-weight codes:** error-correcting codes in which every codeword has the same number of 1s.

</details>

## 🔍 Don't trust us, check it

Every open result ships with the object itself, a short checker you can read in one sitting, a snapshot of the table it beat, and the code that generated it. Check the 13,365-vertex graph yourself in seconds (it prints `VALID`):

```sh
cc -O3 -o ddcheck known-knowns/biggest-graphs/verify-it-yourself/ddcheck.c -lpthread
./ddcheck known-knowns/biggest-graphs/graphs/G_15_4_n13365.edges 15 4 4
```

Start here → [READ_BEFORE_CITING.md](READ_BEFORE_CITING.md)

The results above predate the contributor kit: each was re-checked before release by two or three independent reviewer agents, then by the shipped checkers. No outside expert has reviewed them yet. If one is wrong, tell us and we will correct it in the open.

Puzzles with a living setter stay puzzles: the solution goes privately to the setter, and only a sealed hash (a fingerprint that proves we had the answer without revealing it) lives here → [DONT_SPOIL_THE_HUNT.md](DONT_SPOIL_THE_HUNT.md)

## 🛠 J01N TH3 HUNT

**1. Paste the line** from [Join in one line](#-join-in-one-line) into your agent.

**2. Answer six short questions,** or reply "ok" to the defaults: the name to credit, what you're curious about, how long each run gets, whether it runs nightly, whether your research charter (the topic brief your agent writes) can be shared publicly, and whether it may use what it already knows about you to pick topics (default: no).

**3. Let it hunt.** It picks an open problem from the [bank](bank/) that fits your interests and works on it in its own folder on your machine.

**What you get**
- 🏴 **Credit:** confirmed wins carry the name you choose, or a pseudonym.
- 🧠 **A front-row seat:** every run leaves a plain-language report of what your agent tried, what failed and why.
- 🎲 **Honest odds:** most nights it finds nothing, and a clean "no" counts as a good night.
- 🔓 **Your own niche:** the six questions shape a research charter around what *you're* curious about.

**🛡️ Safe by design.** This is math and codebreaking, not jailbreaking. Nothing is installed until you type **go**, and nothing is posted, emailed or submitted without your **yes**. Runs spend your agent's own plan or API budget, within the time per run you set.

Every new claim has to survive the gauntlet before it counts:

```
hunt --> null test --> 3 skeptics --> check_run.py --> your "yes" --> trophy case
```

- **Null test:** whenever luck could fake a result, the same pipeline runs on 400+ decoys first. If a decoy wins, so does luck.
- **3 skeptics:** three fresh contexts, each with its own code. Any one of them can kill the claim.
- **check_run.py:** a mechanical honesty check. PASS, or it didn't happen.
- **Your "yes":** nothing leaves your machine without it.

### 🧭 Pick your agent

✅ **Claude Code:** run `claude` in any folder and paste the line. Tested end to end.

<details>
<summary><strong>Codex, Gemini CLI, Grok Build, Hermes, OpenClaw, Meta Muse, Cursor and more</strong></summary>

You need an agent that can run code: a terminal, a shell tool, or its own cloud computer. 🧪 = smoke-tested, ➖ = should work, not yet tested.

| Agent | How to start | Notes |
|---|---|---|
| ➖ **Codex CLI** | `codex`, paste the line | Reads `AGENTS.md` natively; skeptics via `codex exec` |
| ➖ **Gemini CLI** | `gemini`, paste the line | Skeptics via `gemini -p` |
| ➖ **Grok Build** (xAI) | start it in any folder, paste the line | Skeptics as its subagents |
| 🧪 **Hermes Agent** (Nous) | `hermes`, paste the line | Honest in our tests but often stopped early: use your strongest model |
| ➖ **OpenClaw** | message it the line | Approve its exec prompts during setup |
| ➖ **Meta Muse** | ask Muse the line | Runs in Muse's own cloud computer, not your laptop |
| ➖ **Cursor, OpenHands, Aider** | open an agent session, paste the line | No scheduler: say "run V3R1T4S" to hunt |
| 💬 **Chat-only bots** (@grok on X, chat apps) | paste the link | Can read and explain the repo, can't hunt without a shell |

Got it working somewhere new? [Open an issue](https://github.com/elder-plinius/V3R1T4S/issues) and tell us.

</details>

⊰•-•✧•-•-⦑/V\E/R\I/T\A/S\⦒-•-•✧•-•⊱

🐉 Siblings: [L1B3RT4S](https://github.com/elder-plinius/L1B3RT4S) · [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) · V3R1T4S

#V3R1T4S #FREEAI #LIBERTAS

*Made with love by Pliny the Liberator <3*
