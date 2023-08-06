# BSD 3-Clause License
# 
# Copyright (c) 2023, LuxProvide S.A.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__email__      = 'jean-philippe.clipffel@lxp.lu'
__author__     = 'Jean-Philippe Clipffel <jean-philippe.clipffel@lxp.lu>'
__license__    = 'BSD-3-Clause'
__copyright__  = 'Copyright (c) 2023 LuxProvide S.A.'
__maintainer__ = 'Jean-Philippe Clipffel'


import os
import re
import sys

import time
import requests
from pathlib import Path
from setuptools.extern.packaging import version
from argparse import Namespace

from .config import settings
from . import __version__


class Hinter:
    """Base hinter class.
    """

    # Hint messages colors control codes
    level_colors: dict = {
        "reset": "\033[0m",
        "info": "\033[32m",
        "warning": "\033[33m",
        "problem": "\033[31m",
    }

    # Regex to match localhost
    localhost_rex: re.Pattern = re.compile(r'^(127\.|localhost).*')

    def hint_files(self, args: Namespace):
        """Check the configuration file status.

        :param args: Parsed arguments
        """
        if not os.path.isfile(settings.Config.env_file):
            yield (
                'warning',
                f'Configuration file "{settings.Config.env_file}" not found',
            )

    def hint_variables(self, args: Namespace):
        """Check the configuration values.

        :param args: Parsed arguments
        """
        # URL format
        msg_url = (
            'warning',
            '''URL (-u, --url or config's "url") should not point to localhost or 127.0.0.1''',
        )
        if len(args.url) > 0 and self.localhost_rex.match(args.url):
            yield msg_url
        elif len(args.url) < 1 and self.localhost_rex.match(settings.url):
            yield msg_url
        # JWT content
        if len(args.auth) < 1 or len(settings.token) < 1:
            yield (
                'warning',
                '''Token (-a, --auth or secret "token") does not look like a valid JWT''',
            )

    def hint_version(self, args: Namespace):
        """Check MelCtl client version.
        """
        current_time = int(time.time())
        last_check_time = current_time
        last_check_file = Path(settings.Config.secrets_dir, 'version_check_time')
        try:
            # Get and set last version check time
            if not os.path.isfile(last_check_file):
                with open(last_check_file, 'w') as fd:
                    fd.write(str(last_check_time))
            # Get and check last version
            else:
                with open(last_check_file, 'r') as fd:
                    last_check_time = int(fd.read())
                # Ignore check if version has been controlled recently
                if last_check_time + settings.public_releases_freq > current_time:
                    return
                # Update last check time
                with open(last_check_file, 'w') as fd:
                    fd.write(str(current_time))
            # Get public version
            jsdata = requests.get(
                settings.public_releases_api,
                timeout=settings.public_releases_timeout).json()
            public_version = jsdata['tag_name']
            # Yield version messages
            if version.parse(__version__) < version.parse(public_version):
                yield (
                    'warning',
                    f'MelCtl is outdated: current version ({__version__}) < public version ({public_version})'
                )
            elif version.parse(__version__) > version.parse(public_version):
                yield (
                    'info',
                    f'MelCtl is a bleeding edge release: current version ({__version__}) > public version ({public_version})'
                )
        except Exception as error:
            yield (
                'warning',
                f'''Cloud not check latest version at {settings.public_releases_api}: {str(error)}'''
            )

    def print_hint(self, args: Namespace, level: str, msg: str):
        """Print a hint.

        :param args: Parsed arguments
        :param level Hint level:
        :param msg: Hint content
        """
        if args.nocolor:
            print(f"{level.upper()}: {msg}", file=sys.stderr)
        else:
            print(
                f'{self.level_colors[level]}'
                f'{level.upper()}: {msg}'
                f'{self.level_colors["reset"]}',
                file=sys.stderr,
            )

    def __call__(self, args: Namespace):
        """Run all hints.

        :param args: Parsed arguments
        """
        _hinted = False
        for hinter in [
            self.hint_files,
            self.hint_variables,
            self.hint_version
        ]:
            try:
                for level, msg in hinter(args):
                    _hinted = True
                    self.print_hint(args, level, msg)
            except Exception as error:
                _hinted = True
                self.print_hint(
                    args,
                    'problem',
                    f'Failed to run hinter {hinter.__name__}: {str(error)}',
                )
                if args.traceback:
                    self.print_hint(
                        args, 'problem', 'Dumping exception as -t|--traceback is set'
                    )
                    raise
        if _hinted:
            print('', file=sys.stderr)
