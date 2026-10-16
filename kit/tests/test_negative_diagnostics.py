# SPDX-License-Identifier: AGPL-3.0-or-later
"""Mocked subprocess evidence; no external package scripts are executed."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

CHECKER = Path(os.environ.get('CHECK_RUN_UNDER_TEST', str(Path(__file__).parents[1] / 'check_run.py')))
spec = importlib.util.spec_from_file_location('negative_checker', CHECKER)
check_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_run)


class NegativeDiagnostics(unittest.TestCase):
    def replay(self, negative, clean=(0, 'PASS')):
        with tempfile.TemporaryDirectory() as tmp:
            pkg = Path(tmp) / 'pkg'
            (pkg / 'object').mkdir(parents=True)
            (pkg / 'object' / 'toy.txt').write_text('123')
            c = check_run.Checker()
            out = io.StringIO()
            with mock.patch.object(check_run, '_run_checks', side_effect=[clean, negative]) as runner, contextlib.redirect_stdout(out):
                check_run.run_own_checker(c, str(pkg), 'synthetic', 1)
            return c, out.getvalue(), runner.call_count

    def test_infrastructure_and_untyped_output_inconclusive(self):
        cases = [(127, 'checker missing'), (139, 'crash'), (-11, ''), (-1, 'TIMEOUT'),
                 (None, 'no sh'), (1, ''), (1, '{'), (1, '{"status":"reject"}'),
                 (1, '{"status":"reject","object":"wrong-object"}'),
                 (0, 'FAIL'), (1, 'PASS'), (0, 'PASS\ntrailing noise'),
                 (1, 'NOT FAIL'), (1, 'FAIL\ntrailing noise'),
                 (None, 'FAIL'), (-1, 'FAIL'), (-11, 'FAIL')]
        for result in cases:
            with self.subTest(result=result):
                c, output, count = self.replay(result)
                self.assertEqual(2, count)
                self.assertEqual([], c.fails)
                self.assertEqual(1, len(c.warns))
                self.assertIn('inconclusive', c.warns[0])
                self.assertIn('no semantic rejection was established', c.warns[0])
                self.assertNotIn('a corrupted copy of the object is rejected', output)

    def test_protocol_rejection_is_ok(self):
        # Positive codes are not reserved by the package protocol, including
        # values shells conventionally use for missing commands or signals.
        for code in (1, 2, 125, 126, 127, 128, 139, 255):
            for text in ('FAIL', 'detail\nFAIL\n', 'detail\r\nFAIL\r\n\r\n'):
                with self.subTest(code=code, text=text):
                    c, output, count = self.replay((code, text))
                    self.assertEqual(2, count)
                    self.assertEqual([], c.fails)
                    self.assertEqual([], c.warns)
                    self.assertIn('a corrupted copy of the object is rejected', output)

    def test_run_checks_infrastructure_results_are_inconclusive(self):
        # Exercise the real runner's error mapping without launching programs.
        with mock.patch.object(check_run.shutil, 'which', return_value=None):
            missing = check_run._run_checks('unused', 1)
        self.assertEqual((None, 'no sh'), missing)
        results = [missing]
        for error in (check_run.subprocess.TimeoutExpired('sh', 1),
                      FileNotFoundError('shell vanished'), PermissionError('cannot launch')):
            with mock.patch.object(check_run.shutil, 'which', return_value='/bin/sh'), \
                    mock.patch.object(check_run.subprocess, 'run', side_effect=error):
                results.append(check_run._run_checks('unused', 1))
        for result in results:
            with self.subTest(result=result):
                c, output, count = self.replay(result)
                self.assertEqual(2, count)
                self.assertEqual([], c.fails)
                self.assertEqual(1, len(c.warns))
                self.assertIn('inconclusive', c.warns[0])

    def test_explicit_corrupted_pass_warning_unchanged(self):
        c, output, count = self.replay((0, 'PASS'))
        self.assertEqual(2, count)
        self.assertEqual([], c.fails)
        self.assertEqual(['synthetic: the checker still printed PASS after one digit of the object was changed; make sure it really checks the object'], c.warns)
        self.assertNotIn('inconclusive', output)
        self.assertNotIn('a corrupted copy of the object is rejected', output)

    def test_clean_failure_still_fails_before_mutation(self):
        for result in ((127, 'missing'), (-1, 'TIMEOUT'), (1, 'FAIL'), (0, '')):
            with self.subTest(result=result):
                c, output, count = self.replay((0, 'PASS'), clean=result)
                self.assertEqual(1, count)
                self.assertEqual(1, len(c.fails))
                self.assertIn('its own checker did not pass', c.fails[0])
                self.assertEqual([], c.warns)


if __name__ == '__main__':
    unittest.main(verbosity=2)
