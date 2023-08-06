# Copyright 2020-2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Inner tests for the GitLab state maintainer for native Mercurial projects.

These wouldn't really qualify as unit tests, since they exert at least
Mercurial, but they are more unitary and disposable than those of
test_integration, testing the implementation details.
"""

from mercurial import (
    error,
)
import pytest
import re

from dulwich.protocol import ZERO_SHA
from heptapod.testhelpers import (
    RepoWrapper,
)
from heptapod.testhelpers.gitlab import patch_gitlab_hooks
from heptapod.gitlab import prune_reasons
from ...no_git import (
    NoGitStateMaintainer,
    RefsByType,
)
from ..utils import common_config


def test_never_prune_default_branch(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)

    config = common_config()
    config['heptapod'] = dict(native=True)
    wrapper = RepoWrapper.init(tmpdir.join('repo'), config=config)

    wrapper.write_commit('foo')
    wrapper.command('gitlab-mirror')
    handler = NoGitStateMaintainer(wrapper.repo.ui,
                                   wrapper.repo)

    def no_analyse(existing, exportable):
        # that's just not the point here
        return {}

    handler.analyse_vanished_refs = no_analyse

    with pytest.raises(error.Abort) as exc_info:
        handler.compare_exportable(
            {},
            {ZERO_SHA: {b'branch/default': prune_reasons.HeadPruneReason()}})

    assert re.search(br'prune.*default branch', exc_info.value.args[0])


def test_refs_by_type():
    head_refs = {b'refs/heads/gl-branch'}
    tag_refs = {b'refs/tags/gl-tag'}

    assert bool(RefsByType(heads=head_refs))
    assert bool(RefsByType(tags=tag_refs))

    refs = RefsByType(heads=head_refs, tags=tag_refs)
    assert set(refs) == head_refs | tag_refs
