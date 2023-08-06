import sys
import subprocess
import logging
import os

PACKAGE_DIR = os.environ.get("CLOUD_PACKAGE_DIR")
CHANGELOG = "CHANGELOG.rst"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_artefact_repo(package_name: str, version: str) -> bool:
    """
    Checks if the package versions exists in the artefact repository.

    Args:
        package_name (str): The name of the package.
        version (str): The package version.

    Returns:
        bool: True if package version exists, False otherwise.
    """
    try:
        blobs = subprocess.check_output(
            ["gsutil", "ls", f"{PACKAGE_DIR}/{package_name}"]
        ).decode("utf8")

        blobs_no_package_name = blobs.replace(package_name, "")

        if version not in blobs_no_package_name:
            raise subprocess.CalledProcessError(returncode=1, cmd='null')
        logger.warning(
            f"v{version} already exists in the artefact repo! - "
            "Bumpversion before releasing."
        )
        return True
    except subprocess.CalledProcessError:
        logger.warning(f"v{version} does not exist in the artefact repo.")
        return False


def check_changelog(version: str) -> bool:
    """
    Checks if package version exists in the CHANGELOG.

    Args:
        version (str): The package version.

    Returns:
        bool: True if version exists in the CHANGELOG, False otherwise.
    """
    for line in open(CHANGELOG):
        if version in line:
            logger.info(f"v{version} exists in the CHANGELOG!")
            return True
    logger.warning(
        f"v{version} does not yet exist in the CHANGELOG! - "
        "Update the CHANGELOG before releasing."
    )
    return False


def check_git_tag(version: str) -> bool:
    """
    Returns a set of versions from a package's git tags.

    Args:
        version (str): The package version.

    Return:
        bool: True if local git tag exists for version, False otherwise.
    """
    try:
        tags = subprocess.check_output(["git", "tag"]).decode("utf8")
        if version not in tags:
            raise subprocess.CalledProcessError(returncode=1, cmd='null')
        logger.info(f"Git tag v{version} exists!")
        return True
    except subprocess.CalledProcessError:
        logging.warning(
            f"Git tag v{version} does not yet exist. - "
            "Update Git tag before releasing."
        )
        return False


def release_ready(package_name: str, version: str) -> bool:
    """
    Checks if package is ready for release and throws an error if not.

    Args:
        package_name (str): The name of the package.
        version (str): The package version being checked.

    Returns:
        bool: Returns True if package version is ready for release.

    Raises:
        Exit code 64: Package version is not ready for release.
    """
    if (
        check_changelog(version)
        and check_git_tag(version)
        and not check_artefact_repo(package_name, version)
    ):
        logger.info(f"v{version} is ready for release!")
        return True  # return value for testing
    else:
        logger.warning(f"v{version} is not ready for release!")
        sys.exit(64)


def image_tags(package_version: str, project_id: str, package_name: str) -> bool:
    """
    Checks if package already has images with current tag released

    Args:
        package_version (str): The version tag of the package being checked.
        project_id (str): The project that the package is in.
        package_name (str): The name of the package.

    Returns:
        bool: Returns False if current package version has already been released.

    Raises:
        Exit code 64: Image tag already exists.
    """
    output = (
        subprocess.check_output(
            f"gcloud container images list-tags --filter=tags:{package_version} --format=json gcr.io/{project_id}/{package_name}",  # noqa: E501
            shell=True,
        )
        .decode("utf8")
        .strip()
    )

    if output != "[]":
        print(f"Tag {package_version} already exists!")
        sys.exit(64)
    else:
        return False
