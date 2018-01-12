#!/usr/bin/env python
import argparse
import json
import shlex
from subprocess import check_call, check_output
import re
import luxem


# NOTE Scanning with pacman -Qe was slow at first but sped up so I think the
# state cache is unnecessary.  Commented out for now.


def main():
    version = '0000.0000.0000'

    parser = argparse.ArgumentParser(
        description='Arch Linux declarative package management')
    parser.add_argument(
        '--conf', help='Configuration path', default='/etc/decpac.conf')
    # parser.add_argument(
    #     '--state', help='State path', default='/var/cache/decpac.cache')

    subparsers = parser.add_subparsers(title='Command', dest='_command')

    com_gen = subparsers.add_parser(
        'generate',
        description='Generate configuration from current explicitly installed packages',  # noqa
    )
    com_gen.add_argument(
        '-c', '--command',
        help='Install command',
        default='pacman --noconfirm -S',
    )
    com_gen.add_argument(
        '-f', '--force',
        help='Overwrite existing configuration',
        action='store_true',
    )

    # com_sync = subparsers.add_parser(
    subparsers.add_parser(
        'sync',
        description='Install, remove, and upgrade packages. Default command.',
    )
    # com_sync.add_argument(
    #     '-r',
    #     '--rescan',
    #     help='Ignore state cache and check what files are actually installed.',
    #     action='store_true',
    # )

    args = parser.parse_args()

    def itercurrent():
        for line in check_output(
                ['pacman', '-Qe']).decode('utf-8').splitlines():
            yield re.search('([^ ]+)', line).group(1)

    command = args._command
    if not command:
        command = 'sync'
    if command == 'generate':
        conf = dict(
            command=shlex.split(args.command),
            installed=list(itercurrent()),
        )
        with open(args.conf, 'w' if args.force else 'x') as out:
            luxem.dump(out, conf, pretty=True)
    elif command == 'sync':
        with open(args.conf, 'r') as conff:
            conf = luxem.load(conff)[0]
        state = None
        # if not getattr(args, 'rescan', False):
        #     try:
        #         with open(args.state, 'r') as statef:
        #             state = json.loads(statef.read())
        #     except FileNotFoundError as e:
        #         pass
        if not state:
            print('Scanning current package state...')
            state = dict(
                version=version,
                installed=[],
            )
            for package in itercurrent():
                state['installed'].append(package)
        add = []
        for new in conf['installed']:
            if new in state['installed']:
                continue
            add.append(new)
        if add:
            print('Installing {}'.format(add))
            # check_call(conf['command'] + add)
        else:
            print('No packages to install.')
        remove = []
        for old in state['installed']:
            if old in conf['installed']:
                continue
            remove.append(old)
        if remove:
            print('Removing {}'.format(remove))
            # check_call(['pacman', '-Rs', '--noconfirm'] + remove)
        else:
            print('No packages to remove.')
        state['installed'] = conf['installed']
        # with open(args.state, 'w') as out:
        #     json.dump(state, out, indent=4)