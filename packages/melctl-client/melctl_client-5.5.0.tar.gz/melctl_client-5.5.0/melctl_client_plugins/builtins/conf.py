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

from melctl_client.config import settings
from melctl_client.commands import Command


class Show(Command):
    """Shows client configuration.
    """

    def __init__(self, subparser):
        super().__init__(subparser, 'show', headers=('url', 'env_file', 'secrets_dir'))

    def target(self, args):
        conf = dict([(k, v) for k, v in settings])
        conf.update({
            'env_file': settings.Config.env_file,
            'secrets_dir': settings.Config.secrets_dir
        })
        return conf


class Init(Command):
    """Creates a new, default configuration
    """

    noset = ('token',)

    def __init__(self, subparser):
        super().__init__(subparser, 'init')

    def target(self, args):
        results = []
        # Configuration file
        results.append({'path': settings.Config.env_file})
        if not os.path.exists(settings.Config.env_file):
            with open(settings.Config.env_file, 'w') as fd:
                for k, v in settings:
                    if k not in self.noset:
                        if isinstance(v, (int, float)):
                            fd.write(f'{k}={v}')
                        elif isinstance(v, str):
                            fd.write(f'{k}="{v}"')
                        fd.write(os.linesep)
            results[-1]['status'] = 'File created'
        else:
            results[-1]['status'] = 'File already exists, no change made'
        # Secrets directory
        results.append({'path': settings.Config.secrets_dir})
        if not os.path.isdir(settings.Config.secrets_dir):
            os.mkdir(settings.Config.secrets_dir)
            results[-1]['status'] = 'Directory created'
        else:
            results[-1]['status'] = 'Directory already exists, not change made'
        # ---
        return results
