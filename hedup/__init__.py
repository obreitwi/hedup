#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (C) 2018 Oliver Breitwieser
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
    hedup: Perform HEtzner Dns UPdates via command line.

    Generate a DNS zonefile update mail, append Let's Encrypt-ACME challenge,
    sign via GPG and send it.

    The zonefiles are searched for at the following locations:
    * ${HOME}/.config/hedup/zonefiles
    * /etc/hedup/zonefiles
    * ${SCRIPT}/hedup/zonefiles

    If no arguments are specified -e.g., when run as , hedup will try to aquire
    the relevant information from the environment. This is especially useful
    when run as manual-auth-hook in certbot.
"""

from __future__ import print_function

from argparse import RawTextHelpFormatter

from . import core

import argparse
import time


def main():
    config = core.read_config(parse_arguments())
    if config["list_domains"]:
        core.list_domains(config)
    elif config["domain"] is not None:
        core.update_dns(config)
    else:
        # auto-mode for manual-auth-hook call from certbot
        core.retrieve_certbot_config(config)
        core.update_dns(config)
        print("Sleeping post update for {}s…".format(
              config["post_update_wait_secs"]))
        time.sleep(config["post_update_wait_secs"])
        print("…done!")


def parse_arguments():
    parser = argparse.ArgumentParser(
            description=globals()["__doc__"],
            formatter_class=RawTextHelpFormatter
        )

    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("-D", "--domain", metavar="<domain>",
                     help="Domain to update")

    parser.add_argument("-a", "--acme-challenge", metavar="<challenge>",
                        help="Which ACME-challenge to set.", nargs="*")

    parser.add_argument("-d", "--dry-run", action="store_true",
                        help="Print mail that would be send.")

    parser.add_argument("-f", "--from-address", metavar="<address>",
                        help="Hetzner robot account.")

    parser.add_argument("-g", "--gpg-sign-key", metavar="<key>",
                        help="GPG key used to sign mail.")

    parser.add_argument("--hetzner-account", metavar="<account>",
                        help="Hetzner robot account.")

    grp.add_argument("-l", "--list-domains", action="store_true",
                     help="List all domains for which a zonefile exists.")

    return parser.parse_args()


if __name__ == "__main__":
    main()
