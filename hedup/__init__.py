#!/usr/bin/env python
# encoding: utf-8
#
"""
    hedup: Perform HEtzner Dns UPdates via command line.

    Generate a DNS zonefile update mail, append Let's Encrypt-ACME challenge,
    sign via GPG and send it.

    The zonefiles are searched for at the following locations:
    * ${HOME}/.config/hedup/zonefiles
    * /etc/hedup/zonefiles
    * ${SCRIPT}/hedup/zonefiles
"""

from __future__ import print_function

import argparse
import os
import os.path as osp
import subprocess as sp
import tempfile
import yaml

ROBOT_ADDRESS = "robot@robot.first-ns.de"


class Which(object):
    """
        Wrap config
    """
    def __init__(self, path, *args):
        if osp.isabs(path):
            self.executable = path
        else:
            try:
                self.executable = sp.check_output(["which", path]).strip()
            except sp.CalledProcessError:
                raise IOError("Could not find executable: {}".format(path))
        self.additional_args = list(args)

    def __call__(self, *args, **kwargs):
        return sp.Popen([self.executable] + self.additional_args + list(args),
                        **kwargs)


def cat_zonefile(config, outfile):
    for folder in get_folders_zonefiles(config):
        filename = osp.join(folder, config["domain"])
        if osp.isfile(filename):
            break

    with open(filename, "r") as f:
        list(map(outfile.write, map(lambda s: s.encode(), f.readlines())))


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.description = globals()["__doc__"]

    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("-D", "--domain", metavar="<domain>",
                     help="Domain to update")

    parser.add_argument("-a", "--acme-challenge", metavar="<challenge>",
                        help="Which ACME-challenge to set.")

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


def read_config(args):
    """
        Read config and update args
    """
    config_file_order = [
            "/etc/hedup/heduprc",
            osp.expandvars("${HOME}/.config/heduprc"),
            osp.expandvars("${HOME}/.config/hedup/heduprc"),
        ]

    config = {}

    for filename_config in config_file_order:
        try:
            with open(filename_config, "r") as f:
                config.update(yaml.load(f))
        except IOError:
            pass

    # update arguments with values from config
    for key in filter(lambda s: not s.startswith("_"), dir(args)):
        value = getattr(args, key, None)
        # user supplied variables overwrite rcfiles
        if value is not None or key not in config:
            config[key] = value

    return config


def write_preamble(config, outfile):
    lines = [
            "user: {}".format(config["hetzner_account"]),
            "job: ns",
            "task: upd",
            "domain: {}".format(config["domain"]),
            "primary: yours",
            "zonefile: /begin"
        ]

    for line in lines:
        outfile.write(line.encode() + b"\n")


def write_epilog(config, outfile):
    outfile.write(b"/end\n")


def write_acme_challenge(config, outfile):
    if config["acme_challenge"] is not None:
        outfile.write("_acme-challenge 300 IN TXT \"{}\"\n".format(
                      config["acme_challenge"]).encode())


def get_folders_zonefiles(config):
    """
        Search and return folder for zonefiles. The order is:

        1. $HOME/.config/hedup/zonefiles
        2. /etc/hedup/zonefiles
        3. ./zonefiles
    """
    search_order = [
            osp.expandvars("$HOME/.config/hedup/zonefiles"),
            "/etc/hedup/zonefiles",
            osp.join(osp.dirname(osp.abspath(__file__)), "zonefiles"),
        ]
    return search_order


def list_domains(config):
    for folder in get_folders_zonefiles(config):
        if not osp.isdir(folder):
            continue
        print("")
        print("Available domains in folder: {}".format(folder))
        print("")
        for domain in os.listdir(folder):
            print(domain)


def escape_spaces(msg):
    if " " in msg:
        return "\"{}\"".format(msg)
    else:
        return msg


def update_dns(config):
    with tempfile.TemporaryFile() as tmp:
        write_preamble(config, tmp)

        cat_zonefile(config, tmp)
        write_acme_challenge(config, tmp)

        write_epilog(config, tmp)

        tmp.seek(0)

        gpg_prog = Which(config.get("gpg_binary", "gpg"))
        mail_prog = Which(config.get("mail_binary", "mail"))

        gpg = gpg_prog("-o", "-", "-u", config["gpg_sign_key"],
                       "--clearsign",
                       stdin=tmp, stdout=sp.PIPE)

        mail_args = ["-s", "DNS Update", "-r", config["from_address"],
                     ROBOT_ADDRESS]

        if config["dry_run"]:
            print("{} {} <<EOF".format(
                mail_prog.executable.decode(),
                " ".join(map(escape_spaces, mail_args))))
            print(gpg.communicate()[0].decode())
            print("EOF")
        else:
            mail = mail_prog(mail_args, stdin=gpg.stdout)
            mail.wait()


def main():
    config = read_config(parse_arguments())
    if config["list_domains"]:
        list_domains(config)
    elif config["domain"] is not None:
        update_dns(config)
    else:
        print("Must specify either --domain or --list-domains.")


if __name__ == "__main__":
    main()
