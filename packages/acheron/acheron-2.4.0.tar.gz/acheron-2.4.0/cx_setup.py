#!/usr/bin/env python3
import datetime
import glob
import os.path
import re
import setuptools
import shutil
import subprocess
import sys

import botocore
import cx_Freeze


is_64bit = sys.maxsize > (2 ** 32)

cwd = os.path.abspath(os.path.dirname(__file__))
version = subprocess.check_output([sys.executable, "setup.py", "--version"],
                                  cwd=cwd, universal_newlines=True).strip()

# strip out any part of the version that isn't numeric
version = re.match(r'\d+([.]\d+)*', version).group(0)

if sys.platform == "win32":
    if is_64bit:
        build_key = "win64"
    else:
        build_key = "win32"
        raise Exception("32-bit builds no longer supported!")
else:
    build_key = "unknown"


# use git to find the branch name and commit hash
try:
    branch = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], universal_newlines=True,
        cwd=cwd).strip()
    commit = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], universal_newlines=True, cwd=cwd).strip()
except Exception:
    # git probably isn't installed
    branch = ""
    commit = ""
build_date = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
with open(os.path.join(cwd, "build_info.txt"), "w", encoding="utf-8") as f:
    f.write("{}\n{}\n{}\n{}\n".format(branch, commit, build_key, build_date))

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

includefiles = [("build_info.txt", "build_info.txt"),
                ('install_extras/acheron.bmp', 'acheron.bmp'),
                ("acheron/acheron.ico", "acheron.ico"),
                ('install_extras/acheron_64bit.iss', 'acheron.iss'),
                ('LICENSE.txt', 'LICENSE.txt'),
                ('acheron/html', 'html')]

boto_prefix = os.path.abspath(os.path.dirname(botocore.__file__))
boto_includefiles = [
    (boto_prefix + "/cacert.pem", "botodata/cacert.pem"),
    (boto_prefix + "/data/_retry.json", "botodata/_retry.json"),
    (boto_prefix + "/data/endpoints.json", "botodata/endpoints.json"),
    (boto_prefix + "/data/sdk-default-configuration.json",
     "botodata/sdk-default-configuration.json"),
    (boto_prefix + "/data/s3", "botodata/s3")]
includefiles.extend(boto_includefiles)


includes = [
    "html.parser",  # boto3
    "boto3.s3",  # boto3
    "boto3.s3.inject",  # boto3
]

excludes = [
    "firmutil",
    "matplotlib",
    "PIL",
    "pyqtgraph.examples",
    "PySide",
    "PySide2",
    "pysideuic",  # pulled in by pyqtgraph, not needed
    "scipy",
    "shiboken",
    "shiboken2",
    "tkinter",
    "unittest",
]

packages = []


class BdistInnoCommand(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _find_iscc(self):
        paths = []
        program_files_keys = ['PROGRAMW6432', 'PROGRAMFILES',
                              'PROGRAMFILES(X86)']
        program_files_dirs = []
        for key in program_files_keys:
            try:
                path = os.environ[key]
                if path:
                    program_files_dirs.append(path)
            except KeyError:
                pass
        for program_files in program_files_dirs:
            paths.append(os.path.join(program_files, "Inno Setup 6"))
        paths.append(os.environ['PATH'])  # not extend; it's a string
        path = os.pathsep.join(paths)
        return shutil.which("iscc", path=path)

    def run(self):
        build = self.get_finalized_command("build")
        build.run()
        iscc = self._find_iscc()
        if not iscc:
            raise Exception("Could not find ISCC.exe!")

        iss_files = glob.glob(os.path.join(build.build_exe, "*.iss"))
        if not iss_files:
            raise Exception("No iss file in build directory!")
        elif len(iss_files) > 1:
            raise Exception("Too many iss files in build directory!")

        iss_file = iss_files[0]

        dist_dir = "dist"

        subprocess.check_call([iscc, "/DVERSION=" + version, "/O" + dist_dir,
                               iss_file], cwd=cwd)


if sys.platform == "win32":
    cmdclass = {'bdist_inno': BdistInnoCommand}
else:
    cmdclass = {}


cx_Freeze.setup(
    name="acheron",
    version=version,
    author="Suprock Technologies, LLC",
    author_email="inquiries@suprocktech.com",
    description="Plotting and recording program for Asphodel devices",
    options={"build_exe": {"includes": includes,
                           "excludes": excludes,
                           "packages": packages,
                           "include_files": includefiles,
                           "zip_include_packages": ['*'],
                           'zip_exclude_packages': [
                               'asphodel',
                               'certifi',
                               'hyperborea',
                               'numpy',
                               'pyqtgraph',
                               # 'PySide6',
                               'shiboken6',
                            ],
                           "include_msvcr": True,
                           "replace_paths": [("*", "")]}},
    executables=[cx_Freeze.Executable(script="cx_shim_run.py", base=base,
                                      target_name="acheron.exe",
                                      icon="acheron/acheron.ico")],
    cmdclass=cmdclass,
)
