#!/usr/bin/env python
import argparse
import json
import shlex
from subprocess import check_call, check_output
import re
import luxem


def main():
    parser = argparse.ArgumentParser(
        description='Arch Linux declarative package management')
    parser.add_argument(
        '--conf', help='Configuration path', default='/etc/decpac.conf')

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

    subparsers.add_parser(
        'sync',
        description='Install, remove, and upgrade packages. Default command.',
    )

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
        print('Scanning current package state...')
        state = dict(
            installed=[],
        )
        for package in itercurrent():
            state['installed'].append(package)
        add = []
        for new in conf['installed']:
            if new in state['installed']:
                continue
            add.append(new)
        remove = []
        for old in state['installed']:
            if old in conf['installed']:
                continue
            remove.append(old)
        print('Installing {}'.format(add))
        print('Removing {}'.format(remove))
        if not input('Okay? y/N') == 'y':
            print('Aborting.')
            return
        if add:
            # check_call(conf['command'] + add)
            pass
        else:
            print('No packages to install.')
        if remove:
            # check_call(['pacman', '-Rs', '--noconfirm'] + remove)
            pass
        else:
            print('No packages to remove.')
        state['installed'] = conf['installed']