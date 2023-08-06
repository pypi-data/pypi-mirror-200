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


import time
import json
import yaml
import logging
import tabulate
import requests
import traceback

from pygments import highlight
from pygments.lexers import JsonLexer, YamlLexer
from pygments.formatters import TerminalFormatter

from .config import settings
from . import __version__


class Command:
    """Generic command.
    """

    log_levels = ['debug', 'info', 'warning', 'error', 'critical']

    def __init__(self, subparser, action: str, headers = 'keys', wait: bool = True, *args, **kwargs):
        """
        :param subparser: Argparse's subparser instance
        :param action: Command line action
        :param headers: Table output headers
        :param wait: Wait for API call to completes
        """
        self.parser = subparser.add_parser(action)
        self.parser.set_defaults(func=self)
        # ---
        self.headers = headers
        self.wait = wait
        # ---
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'melctl-client/{__version__}'
        })
        self.session.verify = False
        requests.packages.urllib3.disable_warnings() # type: ignore[attr-defined]
        # ---
        self.logger = logging.getLogger()
        self.log_fmt = logging.Formatter('[%(levelname)s] %(asctime)s | %(message)s')
        self.log_handler = logging.StreamHandler()
        self.log_handler.setFormatter(self.log_fmt)
        self.logger.handlers = [self.log_handler]
        # ---
        # Log level
        self.parser.add_argument('-l', '--log-level', type=str,
            default='warning', choices=self.log_levels, help='Log level')
        # API server
        self.parser.add_argument('-u', '--url', type=str,
            default=settings.url, help='API server URL')
        # Authentication token
        self.parser.add_argument('-a', '--auth', dest='auth', type=str,
            default=settings.token, help='Authentication token')
        # Version
        self.parser.add_argument('-v', '--version', type=str,
            default='latest', help='API version')
        # Task completion wait switches
        self.parser.add_argument('--wait', dest='wait',
            action='store_true', default=self.wait, help='Wait for task to complete')
        self.parser.add_argument('--nowait', dest='wait',
            action='store_false', default=self.wait, help='Do not wait for task to complete')
        # Task completion wait frequency and timeout
        self.parser.add_argument('--wait-frequency', dest='wait_frequency',
            type=int, default=1, help='Tasks waiting frequency in seconds')
        self.parser.add_argument('--wait-timeout', dest='wait_timeout',
            type=int, default=60, help='Tasks waiting timeout in seconds')
        # Output format
        self.parser.add_argument('-o', '--output-format', dest='outform',
            type=str.lower, default='table', help='Output format', choices=[
                'table', 'json', 'yaml', 'wide', 'keys', 'raw'
            ])
        # Output color
        self.parser.add_argument('--nocolor', dest='nocolor', action='store_true',
            default=False, help='Disable colored output')
        # Table output format
        self.parser.add_argument('--tablefmt', dest='tablefmt', type=str.lower,
            default='simple', choices=tabulate._table_formats.keys(), # type: ignore[attr-defined]
            help='Table format')
        # Dump exception
        self.parser.add_argument('-t', '--traceback', dest='traceback',
            action='store_true', default=False, help='Show exceptions traceback')
        # Dump error
        self.parser.add_argument('--format-error', dest='format_error',
            action='store_true', default=False, help='Format and output error')

    def format_table(self, args, data):
        """Formats output as a table.
        """
        # ---
        # Select headers
        # - Asynchronous task result: print the task ID
        # - Synchronous or finished task result: use command headers
        if isinstance(data, dict) and len(data) == 1 and 'taskId' in data:
            headers = 'keys'
        else:
            headers = self.headers
        # ---
        # Format data as a list
        if not isinstance(data, (list, tuple, set)):
            _data = [data, ]
        else:
            _data = data
        # ---
        # (re)format data to make it pretty-printable 
        if isinstance(headers, (list, set, tuple)) and len(_data) > 0:
            fields = []
            # List of dicts
            if isinstance(_data, (list, tuple, set)) and isinstance(_data[0], dict):
                for d in _data:
                    fields.append([d.get(field) for field in headers])
        else:
            fields = _data
        # ---
        # Print data as table.
        print(tabulate.tabulate(fields, headers=headers, tablefmt=args.tablefmt))

    def format_wide(self, args, data):
        """Formats output as a wide table (all fields)
        """
        self.headers = 'keys'
        self.format_table(args, data)

    def format_json(self, args, data):
        """Formats output as a JSON string.
        """
        if args.nocolor is True:
            print(json.dumps(data, indent=2))
        else:
            print(highlight(
                json.dumps(data, indent=2),
                JsonLexer(),
                TerminalFormatter()
            ))

    def format_yaml(self, args, data):
        """Formats output as a YAML string.
        """
        if args.nocolor is True:
            print(yaml.safe_dump(data, indent=2))
        else:
            print(highlight(
                yaml.safe_dump(data, indent=2),
                YamlLexer(),
                TerminalFormatter()
            ))

    def format_raw(self, args, data):
        print(data)
        return data

    def format(self, args, data):
        """Formats output.
        """
        if data is not None:
            return {
                'table': self.format_table,
                'json': self.format_json,
                'yaml': self.format_yaml,
                'wide': self.format_wide,
                'keys': self.format_wide,
                'raw': self.format_raw
            }[args.outform](args, data)

    def format_error(self, args, error: Exception):
        """Format and print an error.

        :param args: Parsed command line arguments
        :param error: Exception
        """
        data = {
            'error': str(error)
        }
        if args.traceback:
            data['traceback'] = traceback.format_exc()
        # Format and print
        self.format(args, data)

    def wait_task(self, task_id: str, frequency: int, timeout: int):
        """Waits for a task to completes.

        :param task_id: Task ID
        :param frequency: Check frequency
        :param timeout: Check timeout
        """
        timer = 0
        self.logger.info(f'Waiting for task "{task_id}" to complete (timeout: {timeout})')
        while timer <= timeout:
            req = self.session.get(f'{self.url}/tasks/results/{task_id}')
            jsdata = req.json()
            if jsdata is None: 
                time.sleep(frequency)
            else:
                break
            timer += 1
        return jsdata

    def __call__(self, args):
        """Runs and wraps the command entry point.

        :param args: Parsed command line arguments
        """
        try:
            # Setup logger
            self.logger.setLevel(args.log_level.upper())
            # Setup URL, authentication and default headers
            self.url = f'{args.url}/{args.version}'
            self.auth = args.auth
            self.session.headers.update({
                'Authorization': f'Bearer {self.auth}'
            })
            # Runs command
            data = self.target(args)
            self.logger.debug(f'Response data: {data}')
            # Process asynchronous result
            if isinstance(data, dict) and len(data) == 1 and 'taskId' in data:
                self.logger.warning(f'Now tracking asynchronous task: {data["taskId"]}')
                # Wait for task completion
                if args.wait == True:
                    data = self.wait_task(
                        data['taskId'],
                        args.wait_frequency,
                        args.wait_timeout
                    )
                    return self.format(args, self.render(args, data))
                # Print taskID
                else:
                    return self.format(args, data)
            # Process synchronous result
            else:
                return self.format(args, self.render(args, data))
        except Exception as error:
            if args.traceback:
                self.logger.exception(error)
            else:
                self.logger.error(str(error))
            if args.format_error:
                self.format_error(args, error)

    def target(self, args):
        """Command entry point.

        :param args: Parsed command line arguments
        """
        raise NotImplementedError
    
    def render(self, args, data):
        """Renders (post-process) command result after completion.

        :param args: Parsed command line arguments.
        :param data: Received data
        """
        return data
    
    def handle_status(self, args, req: requests.Response):
        """Automatically handles a MelCtl API return.
        """
        try:
            req.raise_for_status()
        except Exception as error:
            try:
                jsdata = req.json()
            except Exception as e2:
                print(e2)
                jsdata = {}
            # Enforce table fields
            self.headers = 'keys'
            # Print error
            self.format(args, jsdata)
            raise error

class SimpleCommand(Command):
    """Generic command, easier to extend.
    """

    def __init__(self, subparser, action: str, method: str, urn: str,
                    *args, **kwargs):
        super().__init__(subparser, action, *args, **kwargs)
        self.method = method.upper()
        self.urn = urn
    
    def target(self, args):
        """Command entry point.

        :param args: Parsed command line arguments
        """
        req = self.session.request(
            self.method,
            f'{self.url}/{self.urn.format_map(args.__dict__)}')
        req.raise_for_status()
        return req.json()
