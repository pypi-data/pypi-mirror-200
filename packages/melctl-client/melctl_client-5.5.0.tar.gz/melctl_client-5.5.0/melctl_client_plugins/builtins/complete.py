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


from textwrap import dedent

from melctl_client.config import settings
from melctl_client.commands import Command


class Bash(Command):
    """Generates a Bash autocomplete script.
    """
    shell = 'bash'

    def __init__(self, subparser):
        super().__init__(subparser, self.shell)

    def target(self, args):
        # Main completer
        completer = f'COMPREPLY=( $(compgen -W "{" ".join(args._completer.keys())}" -- $cur) )'
        # Commands completer
        subcompleters = [
            f'"{command}") COMPREPLY=( $(compgen -W "{" ".join(actions)}" -- $cur ) );;'
            for command, actions
            in args._completer.items()
        ]
        # Generate and print the completion script
        print(dedent(f'''\
            function _melctl_comp()
            {{
                local cur command
                COMPREPLY=()
                cur=${{COMP_WORDS[COMP_CWORD]}}
                command=${{COMP_WORDS[COMP_CWORD-1]}}
                if [ $COMP_CWORD -eq 1 ]; then
                    {completer}
                elif [ $COMP_CWORD -eq 2 ]; then
                    case "$command" in
                        {"".join(subcompleters)}
                        *);;
                    esac
                fi
                return 0
            }} && complete -F _melctl_comp melctl
        '''))


class ZSH(Bash):
    """Generates a ZSH autocomplete script.
    """
    shell = 'zsh'
