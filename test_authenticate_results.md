============================= test session starts ==============================
platform linux -- Python 3.8.10, pytest-8.3.4, pluggy-1.5.0 -- /home/flynn/git/helloai/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/flynn/git/Agent-X
plugins: anyio-4.5.2
collecting ... collected 5 items

X/test_authenticate.py::TestAuthenticate::test_authenticate_v1 PASSED    [ 20%]
X/test_authenticate.py::TestAuthenticate::test_authenticate_v2 PASSED    [ 40%]
X/test_authenticate.py::TestAuthenticate::test_grok_ai_auth PASSED       [ 60%]
X/test_authenticate.py::TestAuthenticate::test_missing_environment_variables FAILED [ 80%]
X/test_authenticate.py::TestAuthenticate::test_open_ai_auth PASSED       [100%]

=================================== FAILURES ===================================
_____________ TestAuthenticate.test_missing_environment_variables ______________

self = <test_authenticate.TestAuthenticate testMethod=test_missing_environment_variables>
mock_getenv = <MagicMock name='getenv' id='140661172884864'>

    @patch("os.getenv")
    def test_missing_environment_variables(self, mock_getenv):
        """Test that missing environment variables raise appropriate errors."""
        def getenv_mock(key):
            if key in ["API_KEY", "OPENAI_API_KEY"]:
                return None
            return "value"
    
        mock_getenv.side_effect = getenv_mock
    
        with self.assertRaises(ValueError) as v1_error:
>           authenticate_v1()
E           AssertionError: ValueError not raised

X/test_authenticate.py:79: AssertionError
=========================== short test summary info ============================
FAILED X/test_authenticate.py::TestAuthenticate::test_missing_environment_variables
========================= 1 failed, 4 passed in 0.50s ==========================
