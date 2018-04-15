#!/usr/bin/env python3
import subprocess
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('version')
parser.add_argument('-f', '--force', action='store_true')
args = parser.parse_args()
if not args.force and subprocess.call(['git', 'diff-index', '--quiet', 'HEAD']) != 0:  # noqa
    raise RuntimeError('Working directory must be clean.')
if not re.match('\\d+\\.\\d+\\.\\d+', args.version):
    args.error('version must be in the format N.N.N')
with open('setup.py', 'r') as source:
    oldsetup = source.read()
with open('setup.py', 'w') as dest:
    dest.write(re.sub(
        '^GEN_version = .*$',
        'GEN_version = \'{}\''.format(args.version),
        oldsetup,
        flags=re.M))
subprocess.check_call([
    'git', 'commit', 'setup.py', '--allow-empty', '-m', 'Version {}'.format(
        args.version)
])
subprocess.check_call(['git', 'tag', 'v{}'.format(args.version)])
subprocess.check_call(['git', 'push'])
subprocess.check_call(['git', 'push', '--tags'])
subprocess.check_call(['python', 'setup.py', 'sdist'])
dist = 'dist/{}-{}.tar.gz'.format(
    re.search('^READ_name = \'(.*)\'$', oldsetup, flags=re.M).group(1),
    args.version
)
subprocess.check_call(['twine', 'upload', dist, '--user', 'rendaw'])
