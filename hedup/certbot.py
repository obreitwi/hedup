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
    def add_parser_arguments(cls, add, default_propagation_seconds=300):  # pylint: disable=arguments-differ
        # adjust default_propagation_seconds to the recommended value
        super(Authenticator, cls).add_parser_arguments(
              add, default_propagation_seconds=default_propagation_seconds)

    def _setup_credentials(self):
        self.hedup_config = hedup.read_config()

    @property
    def _clean_hedup_config(self):
        return copy.deepcopy(self.hedup_config)

    def perform(self, achalls): # pylint: disable=missing-docstring
        self._setup_credentials()
        self._attempt_cleanup = True

        config = self._clean_hedup_config

        responses = []

        for achall in achalls:
            domain = achall.domain
            validation_domain_name = achall.validation_domain_name(domain)
            validation = achall.validation(achall.account_key)

            if "domain" in config\
                    and config["domain"] != validation_domain_name:
                # finalize update of this domain (user should specify all
                # updates for a given domain together)
                hedup.upate_dns(config)
                config = self._clean_hedup_config

            if "domain" not in config:
                config["domain"] = validation_domain_name
                config["acme-challenge"] = [validation]

            elif config["domain"] == validation_domain_name:
                # still the same domain to validate
                config["acme-challenge"].append(validation)

            responses.append(achall.response(achall.account_key))

        if len(config["acme-challenge"]) > 0:
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
        hedup.update_dns(self._clean_hedup_config)
