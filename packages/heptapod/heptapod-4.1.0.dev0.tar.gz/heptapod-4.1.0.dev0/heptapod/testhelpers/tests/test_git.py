# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import subprocess
from ..git import GitRepo


def test_branches(tmpdir):
    server = tmpdir / 'server.git'
    # server_repo is bare, hence we cannot commit directly in there
    server_repo = GitRepo.init(server)

    client = tmpdir / 'client'
    subprocess.call(('git', 'init', str(client)))
    subprocess.call(('git', 'remote', 'add', 'origin', str(server)),
                    cwd=str(client))
    subprocess.call(('git', 'config', 'user.name', 'John Doe'),
                    cwd=str(client))
    subprocess.call(('git', 'config', 'user.email', 'jdoe@heptapod.example'),
                    cwd=str(client))

    (client / 'foo').write('foo')
    subprocess.call(('git', 'add', 'foo'), cwd=str(client))

    subprocess.call(('git', 'commit', '-m', 'init commit', '--no-gpg-sign'),
                    cwd=str(client))
    subprocess.call(('git', 'push', 'origin', 'master'), cwd=str(client))

    assert server_repo.branch_titles() == {b'master': b'init commit'}

    # correct commit SHA is read from server repo
    sha = server_repo.get_branch_sha('master')
    client_log = subprocess.check_output(['git', 'log', '--oneline', sha],
                                         cwd=str(client))
    assert client_log.split(b' ', 1)[-1].strip() == b'init commit'

    # Testing more commit and branch methods
    assert server_repo.commit_hash_title('master') == [sha.encode(),
                                                       b'init commit']
    assert server_repo.get_branch_sha(b'master') == sha
