##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

import json

from .Provider import Provider

from optumi_core.exceptions import (
    OptumiException,
)

from typing import List


class Providers(list):
    """A class for retrieving the full list of potential cloud providers."""

    def __init__(self, files: List[Provider] = []):
        """Constructor for an object that represents all providers or a specific subset of providers.

        Args:
            files (list of Provider, optional): List of Provider objects. Defaults to [].
        """
        super().__init__(files)

    @classmethod
    def list(cls):
        """Obtain the list of all cloud providers.

        Returns:
            list of Provider: The list of providers supported by Optumi.
        """

        providers = Providers()

        user_information = json.loads(optumi.core.get_user_information(True).text)

        for provider in user_information["providers"]:
            provider = Provider(*Provider.reconstruct(provider))
            providers.append(provider)

        return providers

    def __add__(self, other):
        return Providers(super.__add__(self, other))

    def __iadd__(self, other):
        return Providers(super.__iadd__(self, other))

    def __imul__(self, other):
        return Providers(super.__imul__(self, other))

    def __mul__(self, other):
        return Providers(super.__mul__(self, other))

    def __reversed__(self, other):
        return Providers(super.__reversed__(self, other))

    def __rmul__(self, other):
        return Providers(super.__rmul__(self, other))

    def copy(self):
        return Providers(super.copy(self, other))

    def reverse(self, key=None, reverse=False):
        return Providers(super.reverse(self, key, reverse))

    def copy(self):
        return Providers(super.copy(self, other))
