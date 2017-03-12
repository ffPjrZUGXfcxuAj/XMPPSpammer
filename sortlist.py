#!/usr/bin/python3
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Copyright 2017 Diane Trout
#

from __future__ import print_function

import argparse
import collections
import os
import sys

JID = collections.namedtuple('JID', ['username', 'domain'])


def main(cmdline=None):
    parser = make_parser()
    args = parser.parse_args(cmdline)

    with open(args.filename, 'rt') as instream:
        old_name_domain = sorted(split_jids(instream), key=jid_key)

    new_jids = '\n'.join((merge_jid(j) for j in old_name_domain))
    if args.stdout:
        print(new_jids)
    else:
        backup_name = args.filename + '~'
        if os.path.exists(backup_name):
            os.unlink(backup_name)
        os.rename(args.filename, backup_name)

        with open(args.filename, 'wt') as outstream:
            outstream.write(new_jids)
            outstream.write(os.linesep)

    return 0


def make_parser():
    parser = argparse.ArgumentParser("Read, sort, and by default overwrite a list of Jabber IDs")
    parser.add_argument('filename', help='filename to sort')
    parser.add_argument('--stdout', action='store_true', default=False,
                        help="print sorted list instead of overwriting file")
    return parser


def split_jids(stream):
    for jid in stream:
        try:
            jid = jid.strip()
            user_index = jid.index('@')
        except ValueError:
            print('Unable to parse "{}"'.format(jid))
            continue

        resource_index = jid.find('#')
        if resource_index == -1:
            resource_index = None

        parsed = JID(jid[0:user_index], jid[user_index+1:resource_index])

        yield parsed


def merge_jid(jid):
    return jid.username + '@' + jid.domain


def jid_key(jid):
    return [jid.domain, jid.username]


if __name__ == '__main__':
    sys.exit(main())
