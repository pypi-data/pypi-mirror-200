# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Thu Jan 19 16:09:01 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:aa0026/cmdb.git $
#

from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __package__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:  # pragma: no cover
    # Can't unit test this for now since I do not know how to temporarily
    # remove a distribution during runtime. Help. Also, is this even
    # worth it?
    __version__ = "unknown"
