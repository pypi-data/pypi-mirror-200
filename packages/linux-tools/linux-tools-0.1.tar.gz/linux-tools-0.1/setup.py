#!/usr/bin/env python3
# Copyright (c) 2023 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

import pathlib

import setuptools


setuptools.setup(
    name="linux-tools",
    description="Various command line utilities for Linux written in python",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text("utf-8"),
    long_description_content_type="text/markdown",
    license="BSD-3-Clause",
    version="0.1",
    author="Robin Jarry",
    author_email="robin@jarry.cc",
    url="https://sr.ht/~rjarry/linux-tools/",
    packages=setuptools.find_packages("."),
    entry_points="""
    [console_scripts]
    irqstat = linux_tools.irqstat:main
    netgraph = linux_tools.netgraph:main
    """,
)
