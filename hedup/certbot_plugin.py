#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (C) 2018-2019 Oliver Breitwieser
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

from __future__ import print_function

import copy
import logging
import zope.interface

from certbot import interfaces
from certbot.plugins import dns_common
from time import sleep

import hedup.core as hedup

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """Hedup (Hetzner DNS Updater) Authenticator."""

    description = "Perform dns-01 challenge via Hetzner mail updater."

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds=360):  # pylint: disable=arguments-differ
        # adjust default_propagation_seconds to the recommended value
        super(Authenticator, cls).add_parser_arguments(
              add, default_propagation_seconds=default_propagation_seconds)

    def _setup_credentials(self):
        self.hedup_config = hedup.read_config()

    @property
    def _clean_hedup_config(self):
        return copy.deepcopy(self.hedup_config)

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ("Updates Hetzner DNS via email. Zonefiles and gpg keys need "
                "to be setup in advance. See "
                "https://github.com/obreitwi/hedup for details.")

    def perform(self, achalls):  # pylint: disable=missing-docstring
        self._setup_credentials()
        self._attempt_cleanup = True

        config = self._clean_hedup_config

        responses = []

        for achall in achalls:
            domain = achall.domain
            validation = achall.validation(achall.account_key)

            if config.get("domain", None) is not None \
                    and config["domain"] != domain:
                # finalize update of this domain (user should specify all
                # updates for a given domain together)
                hedup.update_dns(config)
                config = self._clean_hedup_config

            if config.get("domain", None) is None:
                config["domain"] = domain
                config["acme_challenge"] = [validation]

            elif config.get("domain", None) == domain:
                # still the same domain to validate
                config["acme_challenge"].append(validation)

            responses.append(achall.response(achall.account_key))

        if len(config.get("acme_challenge", [])) > 0:
            # there are outstanding dns updates
            hedup.update_dns(config)

        # DNS updates take time to propagate and checking to see if the update has occurred is not
        # reliable (the machine this code is running on might be able to see an update before
        # the ACME server). So: we sleep for a short amount of time we believe to be long enough.
        logger.info("Waiting %d seconds for DNS changes to propagate",
                    self.conf('propagation-seconds'))
        sleep(self.conf('propagation-seconds'))

        return responses

    def _cleanup(self, domain, validation_domain_name, validation):  # pragma: no cover
        config = self._clean_hedup_config
        config["domain"] = domain
        hedup.update_dns(config)
