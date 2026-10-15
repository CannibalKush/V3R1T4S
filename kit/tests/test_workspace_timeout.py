# SPDX-License-Identifier: AGPL-3.0-or-later
"""CLI timeout propagation; subprocess results are mocked, never executed."""
import importlib.util
import os
import unittest
from types import SimpleNamespace
from unittest import mock
import test_check_run as fixtures

if os.environ.get('CHECK_RUN_UNDER_TEST'):
    spec = importlib.util.spec_from_file_location('timeout_checker', os.environ['CHECK_RUN_UNDER_TEST'])
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    fixtures.check_run = checker


class WorkspaceTimeout(fixtures.Base):
    def setUp(self):
        super().setUp()
        self.attack()
        self.P = self.package()

    def timeouts(self, *args):
        # Workspace setup also probes git; keep that read-only probe mocked.
        git_result = SimpleNamespace(returncode=0, stdout=b'c' * 40 + b'\n')
        with mock.patch.object(fixtures.check_run, '_run_checks', return_value=(0, 'PASS')) as runner, \
                mock.patch.object(fixtures.check_run.subprocess, 'run', return_value=git_result):
            self.assertPass(*args)
        return [call.args[1] for call in runner.call_args_list]

    def test_package_explicit_timeout_unchanged(self):
        self.assertEqual([7, 7], self.timeouts('--package', self.P, '--timeout', '7'))

    def test_workspace_explicit_timeout_reaches_clean_and_mutant(self):
        self.assertEqual([7, 7], self.timeouts(self.W, '--timeout', '7'))

    def test_setup_explicit_timeout_reaches_outbox(self):
        self.assertEqual([7, 7], self.timeouts(self.W, '--setup', '--timeout', '7'))

    def test_selected_run_explicit_timeout_reaches_outbox(self):
        self.assertEqual([7, 7], self.timeouts(self.W, '--run', self.R, '--timeout', '7'))

    def test_default_timeout_unchanged(self):
        for args in ((self.W,), ('--package', self.P)):
            with self.subTest(args=args):
                self.assertEqual([900, 900], self.timeouts(*args))

    def test_every_outbox_package_gets_requested_timeout(self):
        self.package(name='2026-10-12-second-0123abcd')
        self.assertEqual([7, 7, 7, 7], self.timeouts(self.W, '--timeout', '7'))

    def test_no_exec_still_skips_package_checker_calls(self):
        for args in ((self.W, '--timeout', '7', '--no-exec'),
                     ('--package', self.P, '--timeout', '7', '--no-exec')):
            with self.subTest(args=args):
                self.assertEqual([], self.timeouts(*args))


if __name__ == '__main__':
    unittest.main(verbosity=2)
