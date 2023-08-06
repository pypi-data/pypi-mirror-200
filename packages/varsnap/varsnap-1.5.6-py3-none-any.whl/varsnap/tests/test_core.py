import inspect
import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from typing import Any, Iterator

from varsnap import core
from varsnap.__version__ import __version__


logger = logging.getLogger(core.__name__)
logger.disabled = True


class EnvVar(unittest.TestCase):
    def setUp(self) -> None:
        self.orig_varsnap = os.environ.get(core.ENV_VARSNAP, '')
        self.orig_env = os.environ.get(core.ENV_ENV, '')
        self.orig_producer_token = os.environ.get(core.ENV_PRODUCER_TOKEN, '')
        self.orig_consumer_token = os.environ.get(core.ENV_CONSUMER_TOKEN, '')
        core.CONSUMERS = []
        core.PRODUCERS = []

    def tearDown(self) -> None:
        os.environ[core.ENV_VARSNAP] = self.orig_varsnap
        os.environ[core.ENV_ENV] = self.orig_env
        os.environ[core.ENV_PRODUCER_TOKEN] = self.orig_producer_token
        os.environ[core.ENV_CONSUMER_TOKEN] = self.orig_consumer_token


class TestEnvVar(EnvVar):
    def test_env_var(self) -> None:
        os.environ[core.ENV_VARSNAP] = 'true'
        env = core.env_var(core.ENV_VARSNAP)
        self.assertEqual(env, 'true')

    def test_downcases_env_var(self) -> None:
        os.environ[core.ENV_VARSNAP] = 'TRUE'
        env = core.env_var(core.ENV_VARSNAP)
        self.assertEqual(env, 'true')

    def test_unset_var(self) -> None:
        del os.environ[core.ENV_VARSNAP]
        env = core.env_var(core.ENV_VARSNAP)
        self.assertEqual(env, '')


class TestGetSignature(unittest.TestCase):
    def assertEqualVersion(self, signature: str, expected: str) -> None:
        self.assertEqual(signature, expected % __version__)

    def test_standalone_func(self) -> None:
        signature = core.get_signature(core.env_var)
        self.assertEqualVersion(signature, 'python.%s.env_var')

    def test_class_func(self) -> None:
        signature = core.get_signature(core.Producer.serialize)
        self.assertEqualVersion(signature, 'python.%s.Producer.serialize')

    def test_instance_func(self) -> None:
        signature = core.get_signature(core.Producer.__init__)
        self.assertEqualVersion(signature, 'python.%s.Producer.__init__')


class TestLimitString(unittest.TestCase):
    def test_small_string(self) -> None:
        x = 'asdf'
        self.assertEqual(core.limit_string(x), x)

    def test_medium_string(self) -> None:
        x = 'x' * 30
        self.assertEqual(core.limit_string(x), x)

    def test_long_string(self) -> None:
        x = 'x' * 50
        limited = core.limit_string(x)
        self.assertEqual(limited[:27], 'x' * 27)
        self.assertEqual(limited[27:], '...')


class TestGetBranch(unittest.TestCase):
    def setUp(self) -> None:
        subprocess.run(['git', 'init', 'asdf'], capture_output=True)
        self.original_dir = Path.cwd()
        os.chdir('asdf')

    def tearDown(self) -> None:
        shutil.rmtree(self.original_dir / 'asdf')
        os.chdir(str(self.original_dir))

    def test_branch(self) -> None:
        self.assertEqual(core.get_branch(), 'HEAD')

    def test_no_branch(self) -> None:
        os.chdir('/')
        self.assertEqual(core.get_branch(), '')

    @patch('shutil.which')
    def test_no_git(self, mock_which: MagicMock) -> None:
        mock_which.return_value = None
        self.assertEqual(core.get_branch(), '')


class TestProducer(EnvVar):
    def setUp(self) -> None:
        super(TestProducer, self).setUp()
        os.environ[core.ENV_VARSNAP] = 'true'
        os.environ[core.ENV_ENV] = 'production'
        os.environ[core.ENV_PRODUCER_TOKEN] = 'asdf'

        self.producer = core.Producer(core.env_var)

    def test_init(self) -> None:
        target_func = MagicMock()
        producer = core.Producer(target_func)
        self.assertEqual(producer.target_func, target_func)
        self.assertIn(producer, core.PRODUCERS)

    def test_is_enabled(self) -> None:
        self.assertTrue(core.Producer.is_enabled())

        os.environ[core.ENV_VARSNAP] = 'false'
        self.assertFalse(core.Producer.is_enabled())
        os.environ[core.ENV_VARSNAP] = 'true'

        os.environ[core.ENV_ENV] = 'development'
        self.assertFalse(core.Producer.is_enabled())
        os.environ[core.ENV_ENV] = 'production'

        os.environ[core.ENV_PRODUCER_TOKEN] = ''
        self.assertFalse(core.Producer.is_enabled())
        os.environ[core.ENV_PRODUCER_TOKEN] = 'asdf'

    def test_serialize(self) -> None:
        data = core.Producer.serialize('abcd')
        self.assertGreater(len(data), 0)

    def test_serialize_known_error(self) -> None:
        def f(n: int) -> Iterator[int]:
            yield n
        with self.assertRaises(core.SerializeError):
            core.Producer.serialize(f(2))

    @patch('varsnap.core.pickle.dumps')
    def test_serialize_unknown_error(self, mock_dumps: MagicMock) -> None:
        mock_dumps.side_effect = MemoryError()
        with self.assertRaises(MemoryError):
            core.Producer.serialize('asdf')

    def test_serialize_formatted(self) -> None:
        data = core.Producer.serialize_formatted('abcd')
        self.assertEqual(data, "'abcd'")
        data = core.Producer.serialize_formatted({})
        self.assertEqual(data, '{}')
        data = core.Producer.serialize_formatted(core.Producer)
        self.assertEqual(data, "<class 'varsnap.core.Producer'>")

    @patch('requests.post')
    def test_produce_not_enabled(self, mock_post: MagicMock) -> None:
        os.environ[core.ENV_VARSNAP] = 'false'
        self.producer.produce(['a'], {'b': 'c'}, 'c')
        self.assertFalse(mock_post.called)

    @patch('requests.post')
    def test_produce(self, mock_post: MagicMock) -> None:
        self.producer.produce(['a'], {'b': 'c'}, 'c')
        self.assertEqual(mock_post.call_args[0][0], core.PRODUCE_SNAP_URL)
        data = mock_post.call_args[1]['data']
        self.assertEqual(data['producer_token'], 'asdf')
        self.assertEqual(data['signature'], core.get_signature(core.env_var))
        self.assertIn('inputs', data)
        self.assertIn('prod_outputs', data)


class TestConsumer(EnvVar):
    def setUp(self) -> None:
        super(TestConsumer, self).setUp()
        os.environ[core.ENV_VARSNAP] = 'true'
        os.environ[core.ENV_ENV] = 'development'
        os.environ[core.ENV_CONSUMER_TOKEN] = 'asdf'

        self.trial_group = core.TrialGroup(
            'project_id', 'trial_group_id', 'trial_group_url'
        )
        self.target_func = MagicMock()
        self.target_func.__qualname__ = 'magicmock'
        self.consumer = core.Consumer(self.target_func)
        self.mock_signature = inspect.signature(TestConsumer.example_func)
        self.mock_signature_variadic = inspect.signature(
            TestConsumer.example_func_variadic
        )

    @staticmethod
    def example_func(inp: str) -> str:
        return inp

    @staticmethod
    def example_func_variadic(*inp: str) -> str:
        return ' '.join(inp)

    def test_init(self) -> None:
        target_func = MagicMock()
        consumer = core.Consumer(target_func)
        self.assertEqual(consumer.target_func, target_func)
        self.assertIn(consumer, core.CONSUMERS)

    def test_is_enabled(self) -> None:
        self.assertTrue(core.Consumer.is_enabled())

        os.environ[core.ENV_VARSNAP] = 'false'
        self.assertFalse(core.Consumer.is_enabled())
        os.environ[core.ENV_VARSNAP] = 'true'

        os.environ[core.ENV_ENV] = 'production'
        self.assertFalse(core.Consumer.is_enabled())
        os.environ[core.ENV_ENV] = 'development'

        os.environ[core.ENV_CONSUMER_TOKEN] = ''
        self.assertFalse(core.Consumer.is_enabled())
        os.environ[core.ENV_CONSUMER_TOKEN] = 'asdf'

    def test_deserialize(self) -> None:
        data = core.Producer.serialize('abcd')
        output = core.Consumer.deserialize(data)
        self.assertEqual(output, 'abcd')

        data = core.Producer.serialize(EnvVar)
        output = core.Consumer.deserialize(data)
        self.assertEqual(output, EnvVar)

    def test_deserialize_known_error(self) -> None:
        with self.assertRaises(core.DeserializeError):
            core.Consumer.deserialize('abcd')

    @patch('varsnap.core.pickle.loads')
    def test_deserialize_unknown_error(self, mock_loads: MagicMock) -> None:
        mock_loads.side_effect = MemoryError('asdf')
        with self.assertRaises(MemoryError):
            core.Consumer.deserialize('abcd')

    @patch('inspect.signature')
    def test_target_func_match(self, mock_signature: MagicMock) -> None:
        mock_signature.return_value = self.mock_signature
        inputs = core.Inputs([2], {}, {})
        result = self.consumer.target_func_params_matches(inputs)
        self.assertTrue(result)

    @patch('inspect.signature')
    def test_target_func_no_match(self, mock_signature: MagicMock) -> None:
        mock_signature.return_value = self.mock_signature
        inputs = core.Inputs([2, 4], {}, {})
        result = self.consumer.target_func_params_matches(inputs)
        self.assertFalse(result)

    @patch('inspect.signature')
    def test_target_func_variadic(self, mock_signature: MagicMock) -> None:
        mock_signature.return_value = self.mock_signature_variadic
        inputs = core.Inputs([2, 4], {}, {})
        result = self.consumer.target_func_params_matches(inputs)
        self.assertTrue(result)

    @patch('requests.post')
    def test_consume_not_enabled(self, mock_post: MagicMock) -> None:
        os.environ[core.ENV_VARSNAP] = 'false'
        self.consumer.consume(self.trial_group)
        self.assertFalse(mock_post.called)

    @patch('requests.post')
    def test_consume_empty(self, mock_post: MagicMock) -> None:
        mock_post.return_value = MagicMock(content='')
        self.consumer.consume(self.trial_group)
        self.assertFalse(self.target_func.called)

    @patch('inspect.signature')
    @patch('requests.post')
    def test_consume(
        self, mock_post: MagicMock, mock_signature: MagicMock,
    ) -> None:
        mock_signature.return_value = self.mock_signature
        inputs = {
            'args': (2,),
            'kwargs': {},
            'globals': {},
        }
        data = {
            'results': [{
                'id': 'abcd',
                'inputs': core.Producer.serialize(inputs),
                'prod_outputs': core.Producer.serialize((4,)),
            }],
            'status': 'ok',
        }
        data_str = json.dumps(data)
        mock_post.return_value = MagicMock(content=data_str)
        self.target_func.return_value = (4,)
        self.consumer.consume(self.trial_group)
        self.assertEqual(self.target_func.call_count, 1)
        self.assertEqual(self.target_func.call_args[0][0], 2)
        snap_consume_request = mock_post.mock_calls[0][2]['data']
        self.assertEqual(snap_consume_request['consumer_token'], 'asdf')
        signature = core.get_signature(self.target_func)
        self.assertEqual(snap_consume_request['signature'], signature)
        trial_produce_request = mock_post.mock_calls[1][2]['data']
        self.assertEqual(
            trial_produce_request['trial_group_id'],
            'trial_group_id'
        )
        self.assertEqual(trial_produce_request['consumer_token'], 'asdf')
        self.assertEqual(trial_produce_request['snap_id'], 'abcd')
        test_outputs = core.Producer.serialize((4,))
        self.assertEqual(trial_produce_request['test_outputs'], test_outputs)
        self.assertEqual(trial_produce_request['matches'], True)

    @patch('inspect.signature')
    @patch('requests.post')
    def test_consume_catches_exceptions(
        self, mock_post: MagicMock, mock_signature: MagicMock,
    ) -> None:
        mock_signature.return_value = self.mock_signature
        inputs = {
            'args': (2,),
            'kwargs': {},
            'globals': {},
        }
        error = ValueError('asdf')
        data = {
            'results': [{
                'id': 'abcd',
                'inputs': core.Producer.serialize(inputs),
                'prod_outputs': core.Producer.serialize(error)
            }],
            'status': 'ok',
        }
        data_str = json.dumps(data)
        mock_post.side_effect = [
            MagicMock(content=data_str),
            MagicMock(content=json.dumps({'status': 'ok'})),
        ]
        self.target_func.side_effect = error
        trials = self.consumer.consume(self.trial_group)
        self.assertEqual(self.target_func.call_count, 1)
        self.assertEqual(len(trials), 1)
        self.assertTrue(trials[0].matches)


class TestVarsnap(EnvVar):
    @patch('requests.post')
    def test_no_op(self, mock_post: MagicMock) -> None:
        os.environ[core.ENV_VARSNAP] = 'false'
        mock_func = MagicMock()
        mock_func.__name__ = 'mock_func'
        test_func = core.varsnap(mock_func)
        test_func(1)
        self.assertFalse(mock_post.called)
        self.assertEqual(mock_func.call_args[0][0], 1)

    @patch('requests.post')
    def test_non_deepcopy(self, mock_post: MagicMock) -> None:
        os.environ[core.ENV_VARSNAP] = 'false'
        mock_func = MagicMock()
        mock_func.__name__ = 'mock_func'
        test_func = core.varsnap(mock_func)

        class NonCopyableObject():
            def __deepcopy__(self, memodict: Any) -> None:
                raise RecursionError
        x = NonCopyableObject()
        test_func(x)
        self.assertTrue(mock_func.call_args[0][0] == x)
        mock_func.reset_mock()
        test_func(asdf=x)
        self.assertTrue(mock_func.call_args[1]['asdf'] == x)

    @patch('varsnap.core.Consumer.consume')
    @patch('varsnap.core.Producer.produce')
    def test_consume(
        self, mock_produce: MagicMock, mock_consume: MagicMock
    ) -> None:
        if sys.version_info.major < 3:
            # TODO remove this
            return
        mock_func = MagicMock()
        mock_func.__name__ = 'mock_func'
        mock_func.return_value = 2
        varsnap_mock_func = core.varsnap(mock_func)
        result = varsnap_mock_func(1)
        self.assertEqual(result, 2)
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(mock_consume.call_count, 0)
        self.assertEqual(mock_produce.call_count, 1)
        self.assertEqual(mock_produce.call_args[0][2], 2)

    @patch('varsnap.core.Consumer.consume')
    @patch('varsnap.core.Producer.produce')
    def test_consume_exception(
        self, mock_produce: MagicMock, mock_consume: MagicMock
    ) -> None:
        if sys.version_info.major < 3:
            # TODO remove this
            return
        mock_func = MagicMock()
        mock_func.__name__ = 'mock_func'
        mock_func.side_effect = ValueError('asdf')
        varsnap_mock_func = core.varsnap(mock_func)
        with self.assertRaises(ValueError):
            varsnap_mock_func(1)
        time.sleep(0.1)  # Make sure mock_produce has enough time to be called
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(mock_consume.call_count, 0)
        self.assertEqual(mock_produce.call_count, 1)
        self.assertEqual(str(mock_produce.call_args[0][2]), 'asdf')

    @patch('varsnap.core.Producer.produce')
    def test_func_name(self, mock_produce: MagicMock) -> None:
        varsnap_func = core.varsnap(core.Producer.serialize)
        self.assertEqual(varsnap_func.__name__, 'serialize')
