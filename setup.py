#!/usr/bin/env python
import os.path
from setuptools import setup, find_packages


def auto_version_setup(**kwargs):
    pkg_name = kwargs["packages"][0]

    # Populate the "version" argument from the "VERSION" file.
    pkg_path = os.path.join(os.path.dirname(__file__), pkg_name)
    with open(os.path.join(pkg_path, "VERSION"), "r") as handle:
        pkg_version = handle.read().strip()
    kwargs["version"] = pkg_version

    # Make sure the "VERSION" file is included when we build the package.
    package_data = kwargs.setdefault("package_data", {})
    this_pkg_data = package_data.setdefault(pkg_name, [])
    if "VERSION" not in this_pkg_data:
        this_pkg_data.append("VERSION")

    setup(**kwargs)


auto_version_setup(
    name="behave_graph",
    author="Jenda Mudron",
    author_email="jenmud@gmail.com",
    maintainer="Jenda Mudron",
    maintainer_email="jenmud@optiver.com",
    url="https://github.com/jenmud/ansible-graph",
    keywords="behave graph",
    description="Generate a behave dependency graph.",
    packages=find_packages(),
    package_data={
        "behave_graph": [
            "VERSION",
        ],
    },
    install_requires=[
        "behave",
        "ruruki-eye"
    ],
    entry_points={
        "console_scripts": [
            "behave-graph = behave_graph:main",
        ],
    },
)
