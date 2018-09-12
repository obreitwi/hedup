# hedup: Perform HEtzner Dns UPdates via command line

The Hetzner DNS Robot can be updated via mail. `hedup` allows you to generate
such DNS zonefile update mails, append a Let's Encrypt-ACME challenge and sign
it via GPG.

This is especially useful for automatically updating Let's Encrypt-wildcard
certificates.

**Note**: Currenty `hedup` only issues zonefile update mails, the domain has to
exist beforehand!


## Usage
```
usage: hedup [-h] [-D <domain>] [-a [<challenge> [<challenge> ...]]] [-d]
             [-f <address>] [-g <key>] [--hetzner-account <account>] [-l]

hedup: Perform HEtzner Dns UPdates via command line. Generate a DNS zonefile
update mail, append Let's Encrypt-ACME challenge, sign via GPG and send it.
The zonefiles are searched for at the following locations: *
${HOME}/.config/hedup/zonefiles * /etc/hedup/zonefiles *
${SCRIPT}/hedup/zonefiles If no arguments are specified -e.g., when run as ,
hedup will try to aquire the relevant information from the environment. This
is especially useful when run as manual-auth-hook in certbot.

optional arguments:
  -h, --help            show this help message and exit
  -D <domain>, --domain <domain>
                        Domain to update
  -a [<challenge> [<challenge> ...]], --acme-challenge [<challenge> [<challenge> ...]]
                        Which ACME-challenge to set.
  -d, --dry-run         Print mail that would be send.
  -f <address>, --from-address <address>
                        Hetzner robot account.
  -g <key>, --gpg-sign-key <key>
                        GPG key used to sign mail.
  --hetzner-account <account>
                        Hetzner robot account.
  -l, --list-domains    List all domains for which a zonefile exists.
```

## Minimal Example
1. Copy zonefile from your Hetzner Robot Konsole for `your-domain.tld` to
   `~/.config/hedup/zonefiles/your-domain.tld`.
2. To update a given ACME challenge, run::
```
  hedup -D your-domain.tld --acme-challenge "ThisIsMyACMEChallenge"
```

## Config
Please edit the included sample config file and put it in one for those
locations:

* `$HOME/.config/hedup/heduprc`
* `$HOME/.config/heduprc`
* `/etc/hedup/heduprc`


## Zonefiles

The zonefiles are searched for in the following locations:
  * `${HOME}/.config/hedup/zonefiles`
  * `/etc/hedup/zonefiles`
  * `${SCRIPT}/hedup/zonefiles`

## Copyright
Copyright (C) 2018 Oliver Breitwieser

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

