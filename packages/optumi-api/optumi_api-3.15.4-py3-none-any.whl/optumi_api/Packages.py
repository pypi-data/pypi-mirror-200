##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from typing import List


class Packages(list):
    """A class for specifying the Python packages that must be installed before running a workload."""

    def __init__(self, packages: List[str] = []):
        """Constructor to initialize the package list required by the workload.

        Args:
            packages (list of str, optional): List of packages to install before running a workload. Defaults to [].
        """
        super().__init__(packages)

    def __str__(self):
        return str(self.packages)

    def __add__(self, other):
        return Packages(super.__add__(self, other))

    def __iadd__(self, other):
        return Packages(super.__iadd__(self, other))

    def __imul__(self, other):
        return Packages(super.__imul__(self, other))

    def __mul__(self, other):
        return Packages(super.__mul__(self, other))

    def __reduce__(self, other):
        return Packages(super.__reduce__(self, other))

    def __reduce_ex__(self, other):
        return Packages(super.__reduce_ex__(self, other))

    def __reversed__(self, other):
        return Packages(super.__reversed__(self, other))

    def __rmul__(self, other):
        return Packages(super.__rmul__(self, other))

    def copy(self):
        return Packages(super.copy(self, other))

    def reverse(self, key=None, reverse=False):
        return Packages(super.reverse(self, key, reverse))

    def copy(self):
        return Packages(super.copy(self, other))
