# hedup: Perform HEtzner Dns UPdates via command line.

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

The zonefiles are searched for at the following locations:
  * `${HOME}/.config/hedup/zonefiles`
  * `/etc/hedup/zonefiles`
  * `${SCRIPT}/hedup/zonefiles`

