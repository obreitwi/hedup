#!/usr/bin/env python
# encoding: utf-8


from setuptools import find_packages, setup

setup(
    name="hedup",
    version="0.3.0",
    author="Oliver Breitwieser",
    author_email="oliver@breitwieser.eu",
    packages=find_packages(),
    package_data={
        "hedup": ["heduprc.defaults"],
    },
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
        ],
        "certbot.plugins": [
            "dns = hedup.certbot_plugin:Authenticator"
        ]
    },
    install_requires=[
        "pyyaml",
        "acme>=0.21.1",
        "certbot>=0.21.1",
        "zope.interface"
    ],
    setup_requires=[],
    tests_require=[],
    extras_require={}
)
