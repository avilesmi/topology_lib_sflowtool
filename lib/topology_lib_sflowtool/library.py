# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
topology_lib_sflowtool communication library implementation.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from topology.libraries.utils import stateprovider

from .parser import parse_pid, parse_sflowtool


path = "/tmp"


class SflowtoolState(object):
    """
    State object for sflowtool.

    :param int pid: Process id of the running sFlow collector (sflowtool).
    """
    def __init__(self, sflowtool_pid=None):
        self.sflowtool_pid = sflowtool_pid


@stateprovider(SflowtoolState)
def start(enode, state, mode, port=6343):
    """
    Start sflowtool

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str mode: sflowtool mode (detail/line)
    :param int port: sflowtool port to listen on.
    """
    assert mode is "detail" or mode is "line"

    if mode is "detail":
        cmd = [
            "sflowtool -p {port}".format(port=port)
        ]
    else:
        cmd = [
            "sflowtool -l -p {port}".format(port=port)
        ]

    cmd.append("2>&1 > {path}/sflowtool.log &".format(path=path))

    state.sflowtool_pid = parse_pid(enode(' '.join(cmd)))


@stateprovider(SflowtoolState)
def stop(enode, state):
    """
    Stop sflowtool

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :return: A dictionary as returned by \
        :func:`topology_lib_sflow.parser.parse_sflowtool`
    """

    enode("kill {pid}".format(pid=state.sflowtool_pid))

    state.sflowtool_pid = None

    return parse_sflowtool(
        enode("cat {path}/sflowtool.log".format(path=path))
    )


__all__ = [
    'start',
    'stop'
]
