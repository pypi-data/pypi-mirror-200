#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import os

install_requires = []

readme = open("README.rst").read()
gs_requirements_file = "requirements/requirements_google_storage.txt"

with open("CHANGELOG.rst") as change_log:
    changelog = change_log.read()

with open("requirements/requirements.txt") as reqs:
    requirements = reqs.readlines()
    install_requires.extend(requirements)

# with open("requirements/requirements_google_storage.txt") as reqs:
#     gs_requirements = reqs.readlines()
#     install_requires.extend(gs_requirements)


class CustomInstall(install):
    """Custom install step to handle python dependencies stored on
    Google Cloud Storage"""
    PYTHON_VERSION = "3.8" # See Composer Versions: https://cloud.google.com/composer/docs/concepts/versioning/composer-versions
    AIRFLOW_VERSION = "2.2.5"


    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/a/40172739/2812257
        # install is an old style class object and can't use super()
        # super(CustomInstall, self).__init__(*args, **kwargs)

        install.__init__(self, *args, **kwargs)
        self.bucket_name = os.environ.get("CLOUD_PACKAGE_DIR", 'geotab-python-packages')

        bucket_prefix = 'gs://'
        self.bucket_name=bucket_prefix+self.bucket_name
        if self.bucket_name.startswith(bucket_prefix):
            self.bucket_name = self.bucket_name.replace(bucket_prefix, '')
        print(self.bucket_name)

        
def pip_install(package_name):
    """For some reason setup.install_requires fails to work when 'install'
    is overriden in cmdclass"""
    subprocess.call([sys.executable, "-m", "pip",
                     "install", "--quiet", package_name])

setup(
    name="src/op_secrets_backend",
    version="0.1.7",
    description="Project to host op_secrets_backend",
    long_description=readme + "\n\n" + changelog,
    author="Sida Zhang",
    author_email="sidazhang@geotab.com",
    install_requires=install_requires,
    packages=find_packages(exclude=["docs", "test"]),
    package_dir={"op_secrets_backend": "src/op_secrets_backend"},
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords="op_secrets_backend",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
    ],
    cmdclass={"install": CustomInstall},
)
