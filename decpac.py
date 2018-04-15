#!/usr/bin/env python
import argparse
import shlex
from subprocess import check_call, check_output, call
import re
import luxem
import os.path
from tempfile import NamedTemporaryFile


def main():
    parser = argparse.ArgumentParser(
        description='Arch Linux declarative package management')
    parser.add_argument(
        '--conf', help='Configuration path', default='/etc/decpac.conf')
    parser.add_argument(
        '--noconfirm',
        help='Don\'t ask for confirmation; use default responses',
        action='store_true',
    )

    subparsers = parser.add_subparsers(title='Command', dest='_command')

    com_gen = subparsers.add_parser(
        'generate',
        description='Generate configuration from current explicitly installed packages',  # noqa
    )
    com_gen.add_argument(
        '-c', '--command',
        help='Install command',
    )
    com_gen.add_argument(
        '-ac', '--aurcommand',
        help='AUR install command',
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

    def iterlocal():
        for line in check_output(
                ['packman', '-Qm']).decode('utf-8').splitlines():
            yield re.search('([^ ]+)', line).group(1)

    command = args._command
    if not command:
        command = 'sync'

    if command == 'generate':
        local = set(iterlocal())
        conf = dict(
            installed=[
                luxem.Typed('aur', package) if package in local
                else package
                for package in itercurrent()
            ],
        )
        if args.command:
            conf['install_main'] = shlex.split(args.command)
        if args.aurcommand:
            conf['install_aur'] = shlex.split(args.aurcommand)
        if not args.force and os.path.exists(args.conf):
            print('decpac.conf already exists. Delete it or run with `-f`.')
            return
        with NamedTemporaryFile() as tmp:
            tmp.write(luxem.dumps(conf, pretty=True))
            check_call(['sudo', 'cp', tmp.name, args.conf])

    elif command == 'sync':
        def pname(package):
            if isinstance(package, luxem.Typed):
                return package.value
            return package

        with open(args.conf, 'r') as conff:
            conf = luxem.load(conff)[0]
        print('Scanning current package state...')
        state = dict(
            installed=set(itercurrent()),
        )
        add_main = set()
        add_aur = set()
        conf_names = set()

        # Group packages by type (normal, aur, etc)
        for package in conf['installed']:
            if isinstance(package, luxem.Typed):
                conf_names.add(package.value)
                if package.value not in state['installed']:
                    if package.name == 'main':
                        add_main.add(package.value)
                    elif package.name == 'aur':
                        add_aur.add(package.value)
                    else:
                        raise RuntimeError(
                            'Unknown package type {} for {}'.format(
                                package.name, package.value))
            else:
                conf_names.add(package)
                if package not in state['installed']:
                    add_main.add(package)

        add = add_main | add_aur
        print('Installing {}'.format(add))
        remove = state['installed'] - conf_names
        print('Removing {}'.format(remove))
        if not args.noconfirm and not input('Okay? (y/N) ') == 'y':
            print('Aborting.')
            return
        print()

        # Add new packages or re-mark mis-marked packages
        if add:
            mark = []
            for command, command_default, type_add in [
                    [
                        'install_main',
                        ['sudo', 'pacman', '--noconfirm', '-S'],
                        add_main,
                    ],
                    [
                        'install_aur',
                        None,
                        add_aur,
                    ],
                    ]:
                add_args = conf.get(command) or command_default
                _type_add, type_add = type_add, []
                for package in _type_add:
                    if call(['pacman', '-Q', package]) != 0:
                        type_add.append(package)
                    else:
                        mark.append(package)
                if type_add:
                    if not add_args:
                        raise RuntimeError(
                            'Field {} missing from decpac.conf'.format(
                                command))
                    check_call(add_args + type_add)

            # Hack for trizen which splits up packages which leads to
            # command line packages that are deps of others to be marked
            # as non-explicit.
            if mark:
                call(
                    [
                        'sudo', 'pacman', '--noconfirm', '-D', '--asexplicit'
                    ] + mark)
        else:
            print('No packages to install.')

        # Remove no longer listed packages
        if remove:
            check_call(
                [
                    'sudo', 'pacman', '-D', '--asdeps', '--noconfirm'
                ] + list(remove))
            check_call(
                ['sudo', 'pacman', '-Rsu', '--noconfirm'] + list(remove))
        else:
            print('No packages to remove.')

        print('Done')
