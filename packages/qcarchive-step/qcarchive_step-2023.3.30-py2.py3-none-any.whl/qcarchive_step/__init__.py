# -*- coding: utf-8 -*-

"""
qcarchive_step
A SEAMM plug-in for QCArchive
"""

# Bring up the classes so that they appear to be directly in
# the qcarchive_step package.

from .qcarchive import QCArchive  # noqa: F401, E501
from .qcarchive_parameters import QCArchiveParameters  # noqa: F401, E501
from .qcarchive_step import QCArchiveStep  # noqa: F401, E501
from .tk_qcarchive import TkQCArchive  # noqa: F401, E501

from .metadata import metadata  # noqa: F401

# Handle versioneer
from ._version import get_versions

__author__ = "Paul Saxe"
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
