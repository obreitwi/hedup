#!/usr/bin/env python
# encoding: utf-8


from setuptools import find_packages, setup

setup(
    name="hedup",
    version="0.2.0",
    author="Oliver Breitwieser",
    author_email="oliver.breitwieser@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    url="http://github.com/obreitwi/hedup",
    description="Set ACME challenge for Hetzner DNS via mail.",
    long_description="""\
The Hetzner DNS Robot can be updated via mail. `hedup` allows you to generate
such DNS zonefile update mails, append a Let's Encrypt-ACME challenge and sign
it via GPG. This is especially useful for automatically updating Let's
Encrypt-wildcard certificates.
""",
    entry_points={
        "console_scripts": [
            "hedup = hedup:main",
        ]
    },
    install_requires=["pyyaml"],
    setup_requires=[],
    tests_require=[],
    extras_require={}
)
