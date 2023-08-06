# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
try:
    from pkg_resources import packaging
except ImportError:  # pragma no cover
    # one day, `packaging` might not be vendored in `pkg_resources` any more
    import packaging

import heptapod


def test_package_version():
    # the Version class accepts only PEP440 compliant version strings
    packaging.version.Version(heptapod.__version__)
