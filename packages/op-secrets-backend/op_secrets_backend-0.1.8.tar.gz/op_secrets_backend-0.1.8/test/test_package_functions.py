"""
Tests for `package_functions`
"""

from unittest.mock import patch, mock_open
import unittest
import unittest.mock as mock
import package_functions as pf


class DuplicatePackageVersion(unittest.TestCase):
    @patch("subprocess.check_output", return_value=b"v0.1.0")
    def test_check_git(self, mock_check_output):
        test_tag_true = "0.1.0"
        test_tag_false = "9999.999.99"
        assert pf.check_git_tag(test_tag_true) is True
        assert pf.check_git_tag(test_tag_false) is False
        mock_check_output.assert_called_with(["git", "tag"])

    def test_check_changelog(self):
        test_version = "9999.999.99"
        test_first_version = "0.1.0"
        assert pf.check_changelog(test_version) is False
        assert pf.check_changelog(test_first_version) is True

    def test_check_artefact_repo(self):
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = (
                b"hello_world-0.1.0-py2.py3-none-any.whl\n"
                + b"hello_world-0.1.0.tar.gz\n"
                + b"hello_world-0.1.1-py2.py3-none-any.whl\n"
                + b"hello_world-0.1.1.tar.gz\n"
            )
            assert pf.check_artefact_repo("hello_world", "0.1.0") is True
            assert pf.check_artefact_repo("hello_world", "9999.999.99") is False

    def test_check_artefact_repo_with_version_in_package_name(self):
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = (
                b"hello-2.1.1-world-py2.py3-none-any.whl\n"
                + b"hello-2.1.1-world-0.1.0.tar.gz\n"
                + b"hello-2.1.1-world-0.1.1-py2.py3-none-any.whl\n"
                + b"hello-2.1.1-world-0.1.1.tar.gz\n"
            )
            assert pf.check_artefact_repo("hello-2.1.1-world", "0.1.0") is True
            assert pf.check_artefact_repo("hello-2.1.1-world", "2.1.1") is False

    def test_release_ready_false(self):
        test_version = "9999.999.99"
        with self.assertRaises(SystemExit) as cm:
            pf.release_ready("hello_world", test_version)
        self.assertEqual(cm.exception.code, 64)

    @patch("builtins.open", new_callable=mock_open)
    def test_release_ready_true(self, mock_open):
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(["3000", "9999.999.99"])
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = [
                b"v9999.999.99",
                b"hello_world-0.1.0.tar.gz",
            ]
            assert pf.release_ready("hello_world", "9999.999.99") is True

    @patch("subprocess.check_output", return_value='[]'.encode())
    def test_duplicate_tags(self, mock_check_output):
        package_version = "9999.999.99"
        project_id = "geotab-bi"
        package_name = "hello_world"

        pf.image_tags(package_version, project_id, package_name)
        mock_check_output.assert_called_with(
            f"gcloud container images list-tags --filter=tags:{package_version} --format=json gcr.io/{project_id}/{package_name}",  # noqa: E501
            shell=True,
        )

    @patch("subprocess.check_output", return_value='[]'.encode())
    def test_duplicate_tags_false(self, mock_check_output):
        package_version = "9999.999.99"
        project_id = "geotab-bi"
        package_name = "hello_world"
        assert pf.image_tags(package_version, project_id, package_name) is False

    @patch("subprocess.check_output", return_value='not_[]'.encode())
    def test_duplicate_tags_true(self, mock_check_output):
        package_version = "0.1.0"
        project_id = "geotab-bi"
        package_name = "hello_world"
        with self.assertRaises(SystemExit) as cm:
            pf.image_tags(package_version, project_id, package_name)
        self.assertEqual(cm.exception.code, 64)
