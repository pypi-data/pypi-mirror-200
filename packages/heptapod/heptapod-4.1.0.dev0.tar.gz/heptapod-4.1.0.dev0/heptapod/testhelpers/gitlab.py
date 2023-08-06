# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Test support for users of heptapod.gitlab
"""
from __future__ import absolute_import
import attr
from copy import deepcopy
import logging
import shutil

from mercurial_testhelpers.repo_wrapper import (
    as_bytes,
)
from heptapod.gitlab import hooks
from hgext3rd.heptapod.branch import (
    get_default_gitlab_branch,
)

from .hg import RepoWrapper
from .git import GitRepo
logger = logging.getLogger(__name__)


def patch_gitlab_hooks(monkeypatch, records, action=None):

    def call(self, changes):
        records.append((self.name, changes))
        if action is not None:
            return action(self.name, changes)
        else:
            return 0, ("hook %r ok" % self.name).encode(), 'no error'

    def init(self, repo, encoding='utf-8'):
        self.repo = repo
        self.encoding = encoding

    monkeypatch.setattr(hooks.Hook, '__init__', init)
    monkeypatch.setattr(hooks.PreReceive, '__call__', call)
    monkeypatch.setattr(hooks.PostReceive, '__call__', call)


@attr.s
class GitLabStateMaintainerFixture:
    """Helper class to create fixtures for GitLab state maintainers.

    The pytest fixture functions themselves will have to be provided with
    the tests that use them.

    It is not the role of this class to make decisions about scopes or
    the kind of root directory it operates in.

    This provides

    - Mercurial repository test wrapper
    - GitLab notifications interception

    and is thus usable directly for native repositories.
    """
    base_path = attr.ib()
    hg_repo_wrapper = attr.ib()
    gitlab_notifs = attr.ib()

    @classmethod
    def init(cls, base_path, monkeypatch, hg_config=None,
             common_repo_name='repo',
             additional_extensions=(),
             **kw):
        if hg_config is None:
            config = {}
        else:
            config = deepcopy(hg_config)

        config.setdefault('extensions', {}).update(
            (ext, '') for ext in additional_extensions)
        config['phases'] = dict(publish=False)

        hg_repo_wrapper = RepoWrapper.init(
            base_path / (common_repo_name + '.hg'),
            config=config)
        notifs = []
        patch_gitlab_hooks(monkeypatch, notifs)
        return cls(hg_repo_wrapper=hg_repo_wrapper,
                   gitlab_notifs=notifs,
                   base_path=base_path,
                   **kw)

    def clear_gitlab_notifs(self):
        """Forget about all notifications already sent to GitLab.

        Subsequent notifications will keep on being recorded in
        ``self.gitlab_notifs``.
        """
        del self.gitlab_notifs[:]

    def activate_mirror(self):
        """Make mirroring from Mercurial to Git repo automatic.

        This is essential to get the mirroring code to run in-transaction.
        """
        self.hg_repo_wrapper.repo.ui.setconfig(
            b'hooks', b'pretxnclose.testcase',
            b'python:heptapod.hooks.gitlab_mirror.mirror')

    def delete(self):
        hg_path = self.hg_repo_wrapper.repo.root
        try:
            shutil.rmtree(hg_path)
        except Exception:
            logger.exception("Error removing the Mercurial repo at %r",
                             hg_path)

    def __enter__(self):
        return self

    def __exit__(self, *exc_args):
        self.delete()
        return False  # no exception handling related to exc_args

    def assert_default_gitlab_branch(self, expected):
        gl_branch = get_default_gitlab_branch(self.hg_repo_wrapper.repo)
        assert gl_branch == as_bytes(expected)


@attr.s
class GitLabMirrorFixture(GitLabStateMaintainerFixture):
    """Helper class to create fixtures for GitLab aware hg-git mirroring.

    Adds the Git repository to GitLabStateMaintainerFixture
    """
    git_repo = attr.ib()
    import heptapod.testhelpers.gitlab

    @classmethod
    def init(cls, base_path, monkeypatch,
             common_repo_name='repo', **kw):
        git_repo = GitRepo.init(base_path / (common_repo_name + '.git'))
        return super(GitLabMirrorFixture, cls).init(
            base_path, monkeypatch,
            common_repo_name=common_repo_name,
            additional_extensions=['hggit'],
            git_repo=git_repo,
            **kw)

    def delete(self):
        git_path = self.git_repo.path
        try:
            shutil.rmtree(git_path)
        except Exception:
            logger.exception("Error removing the Git repo at %r", git_path)

        super(GitLabMirrorFixture, self).delete()

    def assert_default_gitlab_branch(self, expected):
        assert self.git_repo.get_symref('HEAD') == 'refs/heads/' + expected
        super(GitLabMirrorFixture, self).assert_default_gitlab_branch(expected)
