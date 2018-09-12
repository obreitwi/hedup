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
  hedup --domain sample-domain.eu --acme-challenge "ThisIsMyACMEChallenge"
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

