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
from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    """MelCTL client settings.
    """

    # MelCtl server URL
    url: str = 'https://melctl.lxp-prod.cloud.lxp.lu'

    # MelCtl authentication token
    token: str = ''

    # Public repository release URL
    public_releases_api: str = 'https://api.github.com/repos/LuxProvide/melctl-client/releases/latest'

    # Public repository access timeout in seconds
    public_releases_timeout: float = 0.5

    # Public repository check frequency in seconds
    public_releases_freq: int = 60

    class Config:
        """Configuration source.
        """

        # Path to configuration file
        env_file = str(
            Path(os.environ.get('MELCTL_CLI_CONFIG', '~/.melctl-cli.env'))
            .expanduser()
            .absolute()
        )

        # Path to secrets directory
        secrets_dir = str(
            Path(os.environ.get('MELCTL_CLI_SECRETS', '~/.melctl-secrets'))
            .expanduser()
            .absolute()
        )


settings = Settings()
