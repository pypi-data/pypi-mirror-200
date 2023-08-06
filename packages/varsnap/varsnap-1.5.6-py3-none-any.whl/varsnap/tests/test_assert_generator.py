import json
import logging
import os
import unittest
from unittest.mock import MagicMock, patch

from typing import Any

from varsnap import assert_generator, core


def add(x: int, y: int) -> int:
    return x + y


null = open(os.devnull, 'w')


class TestResult(unittest.runner.TextTestResult):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(TestResult, self).__init__(*args, **kwargs)
        self.successes: list[Any] = []

    def addSuccess(self, test: Any) -> None:
        super(TestResult, self).addSuccess(test)
        self.successes.append(test)


def mock_logger() -> logging.Logger:
    test_logger = logging.getLogger(assert_generator.__name__)
    test_logger.setLevel(logging.ERROR)
    return test_logger


class TestGenerateTrialGroup(unittest.TestCase):
    def setUp(self) -> None:
        self.post_return = {
            'status': 'ok',
            'project_id': 'project_id',
            'trial_group_id': 'trial_group_id',
            'trial_group_url': 'trial_group_url',
        }

    @patch('requests.post')
    def test_get_trial_group(self, mock_post: MagicMock) -> None:
        response_content = json.dumps(self.post_return)
        mock_post.return_value = MagicMock(content=response_content)
        trial_group = assert_generator.generate_trial_group()
        self.assertEqual(
            mock_post.call_args[1]['data']['client'],
            core.CLIENT_NAME
        )
        self.assertTrue('branch' in mock_post.call_args[1]['data'])
        self.assertTrue('consumer_token' in mock_post.call_args[1]['data'])
        self.assertEqual(
            trial_group.project_id, self.post_return['project_id']
        )
        self.assertEqual(
            trial_group.trial_group_id, self.post_return['trial_group_id']
        )
        self.assertEqual(
            trial_group.trial_group_url, self.post_return['trial_group_url']
        )

    @patch('requests.post')
    def test_get_trial_group_not_ok(self, mock_post: MagicMock) -> None:
        self.post_return['status'] = 'not ok'
        response_content = json.dumps(self.post_return)
        mock_post.return_value = MagicMock(content=response_content)
        trial_group = assert_generator.generate_trial_group()
        self.assertEqual(trial_group.project_id, '')
        self.assertEqual(trial_group.trial_group_id, '')
        self.assertEqual(trial_group.trial_group_url, '')

    @patch('requests.post')
    def test_get_trial_group_error(self, mock_post: MagicMock) -> None:
        mock_post.return_value = MagicMock(content='')
        trial_group = assert_generator.generate_trial_group()
        self.assertEqual(trial_group.project_id, '')
        self.assertEqual(trial_group.trial_group_id, '')
        self.assertEqual(trial_group.trial_group_url, '')


class TestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.original_configure_logger = assert_generator._configure_logger
        assert_generator._configure_logger = mock_logger
        core.CONSUMERS = []
        self.trial_group = core.TrialGroup(
            'project_id', 'trial_group_id', 'trial_group_url'
        )
        self.patcher = patch(
            'varsnap.assert_generator.generate_trial_group'
        )
        self.patched_generate_trial_group = self.patcher.start()
        self.patched_generate_trial_group.return_value = self.trial_group

    def tearDown(self) -> None:
        assert_generator._configure_logger = self.original_configure_logger
        core.CONSUMERS = []
        self.patcher.stop()

    def test_no_consumers(self) -> None:
        all_matches, all_logs = assert_generator.test()
        self.assertEqual(all_matches, None)
        self.assertEqual(all_logs, 'Test Results: trial_group_url')

    @patch('varsnap.core.Consumer.consume')
    def test_consume(self, mock_consume: MagicMock) -> None:
        core.Consumer(add)
        trial = core.Trial(core.Inputs([1, 1], {}, {}), 2)
        trial.matches = True
        mock_consume.return_value = [trial]
        all_matches, all_logs = assert_generator.test()
        self.assertTrue(all_matches)
        self.assertEqual(all_logs, 'Test Results: trial_group_url')

    @patch('varsnap.core.Consumer.consume')
    def test_consume_fail(self, mock_consume: MagicMock) -> None:
        core.Consumer(add)
        trial = core.Trial(core.Inputs([1, 1], {}, {}), 2)
        trial.matches = False
        trial.report = 'abcd'
        mock_consume.return_value = [trial]
        all_matches, all_logs = assert_generator.test()
        self.assertFalse(all_matches)
        self.assertEqual(all_logs, (
            '\n\n'
            'Test Results: trial_group_url'
            '\n\n'
            'abcd'
            '\n\n'
            'Test Results: trial_group_url'
            '\n\n'
        ))
