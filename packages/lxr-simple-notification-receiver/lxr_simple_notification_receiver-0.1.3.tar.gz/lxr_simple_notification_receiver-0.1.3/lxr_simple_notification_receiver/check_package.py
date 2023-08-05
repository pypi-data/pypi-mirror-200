from enum import Enum
import subprocess, sys
import pkg_resources
from distutils.version import StrictVersion
from packaging import version
PIP_INDEX_AVAIABLE_PROMPT: str = "Available versions:"
MIN_PIP_VERSION = "22.2"

import argparse
from pathlib import Path
import os

import sys, importlib
from pathlib import Path
def import_parents(level: int = 1) -> None:
    global __package__
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]
    
    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError: # already removed
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])
    importlib.import_module(__package__) # won't be needed after that

if __name__ == '__main__' and (__package__ is None or len(__package__) == 0):
    import_parents()
from . check_interpreter import check_conda_interpreter

class Platform(Enum):
    win_amd64 = "win_amd64"
    linux_x86_64 = "linux_x86_64"
    
target_platforms : list[Platform] = []
def get_root_packages() -> list[tuple[str, str]]:
    reqs = subprocess.run([sys.executable, '-m', 'pipdeptree', '--json-tree'], capture_output=True, text=True)
    import json
    tree = json.loads(reqs.stdout)
    roots = []
    for root in tree:
        pkg : str = root["key"]
        ver : str = root["installed_version"]
        roots.append((pkg, ver))
    return roots

def check_pkg_avaiable_platform(pkg: str, ver: str, target_platform: str) -> bool:
    ret: subprocess.CompletedProcess[str] = subprocess.run([sys.executable, '-m', 'pip', 'index', 'versions', '--platform', target_platform, pkg], capture_output=True, text=True)
    if ret.stdout:
        out = str(ret.stdout)
        if PIP_INDEX_AVAIABLE_PROMPT in out and ver in out:
            return True
    return False


def check_pkg_avaiable(pkg: str, ver: str) -> bool:
    return all([check_pkg_avaiable_platform(pkg, ver, platform.value) for platform in target_platforms])


def get_old_packages(reqirements_file: str) -> list[tuple[str, str]]:
    with open(reqirements_file, "r") as f:
        old_reqs = pkg_resources.parse_requirements(f)
        old_pkgs = []
        for old_req in old_reqs:
            pkg = old_req.project_name
            if(len(old_req.specs) == 0):
                raise Exception("No version specified for package: " + old_req.project_name)
            for spec in old_req.specs:
                if spec[0] == "==":
                    ver = spec[1]
            old_pkgs.append((pkg, ver))
        return old_pkgs

def update_requirements(requirements_file: str) -> None:
    pkgs = get_root_packages()
    old_pkgs = get_old_packages(requirements_file)
    ordered_pkgs = []
    for old_pkg in old_pkgs:
        if old_pkg in pkgs:
            ordered_pkgs.append(old_pkg)
            pkgs.remove(old_pkg)
    for pkg in pkgs:
        if check_pkg_avaiable(pkg[0], pkg[1]):
            print("Package: " + pkg[0] + " has been added")
            ordered_pkgs.append(pkg)
        else:
            raise Exception("Package: " + pkg[0] + " is not available for all platforms")
    # Compare the old packages with the new packages to print out the changes
    for old_pkg in old_pkgs:
        if old_pkg not in ordered_pkgs and old_pkg[0] in [pkg[0] for pkg in ordered_pkgs]:
            print("Package: " + old_pkg[0] + " has been updated to version: " + [pkg[1] for pkg in ordered_pkgs if pkg[0] == old_pkg[0]][0])
        elif old_pkg not in ordered_pkgs:
            print("Package: " + old_pkg[0] + " has been removed")
            
    with open(requirements_file, "w") as f:
        for pkg in ordered_pkgs:
            f.write("%s==%s\n" % (pkg[0], pkg[1]))

from importlib.metadata import metadata
from importlib.metadata import PackageNotFoundError
def check_pkg_installed(pkg: str, min_ver: str | None = None) -> bool:
    try:
        mt = metadata(pkg)
    except PackageNotFoundError:
        return False
    if min_ver is not None:
        ver = version.parse(mt["Version"])
        if ver < version.parse(min_ver):
            return False
    return True


if __name__ == "__main__":
    env_name = "android_automatic"
    check_conda_interpreter(env_name)
    parser = argparse.ArgumentParser(description='Update requirements.txt file')
    parser.add_argument('filename', type=str, help='the requirements.txt to be processed')
    args = parser.parse_args()
    if args.filename is None:
        parser.print_help()
        exit(1)
    else:
        unsufficient_pkgs = False
        if not check_pkg_installed("pip", MIN_PIP_VERSION):
            print("pip version is not installed or too old, please update pip to version %s or higher" % MIN_PIP_VERSION)
            unsufficient_pkgs = True
        if not check_pkg_installed("pipdeptree"):
            print("pipdeptree is not installed, please install pipdeptree")
            unsufficient_pkgs = True
        if unsufficient_pkgs:
            exit(1)
        path = Path(args.filename)
        if path.resolve():
            update_requirements(str(path))

