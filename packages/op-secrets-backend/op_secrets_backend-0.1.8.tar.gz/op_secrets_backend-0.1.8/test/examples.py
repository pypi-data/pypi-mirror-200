from io import StringIO
import os
from unittest.mock import Mock
import pytest
import examples_helpers
from examples_helpers import Worker, Helper, CountryPricer


def test_patch_module(mocker):
    mock_module = mocker.patch("examples_helpers.example_module")
    mock_module.return_value = "mocked_return_value"

    assert examples_helpers.example_module() == "mocked_return_value"


def test_patch_class(mocker):
    MockHelper = mocker.patch("examples_helpers.Helper")
    MockHelper.return_value.get_path.return_value = "patched_path"

    worker = Worker()
    MockHelper.assert_called_once_with("default_path")

    assert worker.get_path() != "default_path"
    assert worker.get_path() == "patched_path"


def test_patch_attribute(mocker):
    mocker.patch.object(Helper, "get_path", return_value="partial_patched_path")
    worker = Worker()
    assert worker.helper.path == "default_path"
    assert worker.get_path() == "partial_patched_path"


def test_patch_that_should_have_failed(mocker):
    # without class speccing , tests can pass when it should fail
    mock_worker = mocker.patch("examples_helpers.Worker")
    worker_instance = mock_worker.return_value
    worker_instance.none_existing_method.return_value = "testing"
    assert worker_instance.none_existing_method() == "testing"


@pytest.mark.xfail(reason="Class speccing catches none existing method", strict=True)
def test_patch_with_class_speccing(mocker):
    # with class speccing , tests will fail when it should fail
    mock_worker = mocker.patch("examples_helpers.Worker", autospec=True)
    worker_instance = mock_worker.return_value
    worker_instance.none_existing_method.return_value = "testing"
    assert worker_instance.none_existing_method() == "testing"


@pytest.mark.xfail(
    reason="Field class in CountryPricer is actually called before patching"
)
def test_patch_class_calling_another_class_fail(mocker):
    mocker.patch("examples_helpers.COUNTRIES", ["custom_country"])
    pricer = CountryPricer()
    assert pricer.get_discounted_price(100, "custom_country") == pytest.approx(80)


def test_patch_class_calling_another_class_success(mocker):
    mocker.patch("examples_helpers.CountryPricer.country.default", "custom_country")
    pricer = CountryPricer()
    assert pricer.get_discounted_price(100, "custom_country") == pytest.approx(80)


def test_mock_builtin_open_and_context_manager(mocker):
    # TODO: this test looks incorrect for showcasing patching context manager

    def length_of_opened_text():
        with open("text.txt") as f:
            contents = f.read()
        return len(contents)

    try:
        mock_open = mocker.patch("builtins.open")
    except ImportError:
        mock_open = mocker.patch("__builtin__.open")

    mock_open.return_value.__enter__.return_value = StringIO(u"12345")

    size_text = length_of_opened_text()
    mock_open.assert_called_once_with("text.txt")

    assert size_text == 5


def test_monkeypatch(monkeypatch):
    def get_cwd():
        return os.getcwd()

    def get_env_joined_path():
        return os.path.join(os.getcwd(), os.environ["MY_VAR"])

    monkeypatch.setattr("os.getcwd", lambda: "custom_path")
    monkeypatch.setenv("MY_VAR", "custom_env")

    assert get_cwd() == "custom_path"
    assert get_env_joined_path() == "custom_path/custom_env"


@pytest.fixture()
def path_context():
    return "custom_path"


@pytest.fixture()
def helper_context():
    return {
        "author": "John Smith",
        "email": "john_smith@example.com",
        "project_name": "temp_project",
    }


def test_fixture(path_context, helper_context):
    # path_context returns "custom_path"
    helper = Helper(path_context)
    assert helper.get_path() == os.path.join(os.getcwd(), "custom_path")

    # set details of helper with key,value pairs in helper_context
    helper.set_details(**helper_context)
    assert helper.details == helper_context


def test_expected_exception():
    with pytest.raises(ZeroDivisionError):
        1 / 0


@pytest.mark.xfail(reason="2 / 1 does not produce a zero division error")
def test_no_exception():
    with pytest.raises(ZeroDivisionError):
        2 / 1


def test_multipatch(mocker):
    helper = Helper("custom_path")
    mocker.patch.multiple(
        "examples_helpers.Helper",
        check_email=Mock(return_value=False),
        check_project_name=Mock(return_value=False),
    )
    assert not helper.valid_details()


def test_call_args_list(mocker):
    json_mock = Mock()

    json_mock.loads('{ "name": "John", "age":"72", "city":"Toronto" }')
    json_mock.loads('{"job": "Retired", "mood", "grumpy"}')

    expected_args = [
        mocker.call('{ "name": "John", "age":"72", "city":"Toronto" }'),
        mocker.call('{"job": "Retired", "mood", "grumpy"}'),
    ]
    assert json_mock.loads.call_args_list == expected_args
