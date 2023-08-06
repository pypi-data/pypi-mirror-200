#!/usr/bin/env python
# *_* coding: utf-8 *_*

"""calc kernel module"""

from ipykernel.kernelbase import Kernel
from pexpect import replwrap

notallowed = ["quit", "exit", "help", "man"]

calcwrapper = replwrap.REPLWrapper("calc -d", "; ", None)

class janscalckernel(Kernel):
    """calc kernel class hooks into the calc repl via ipykernel"""
    implementation = 'IPython'
    implementation_version = '8.12.0'
    language = 'calc'
    language_version = '2.14.1.0'
    language_info = {
        'name': 'calc',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "calc'ing for you since 1984..."

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            if code in notallowed:
                solution = f'"{code}" is not allowed in the calc kernel'
            else:
                solution = calcwrapper.run_command(code)
                solution = solution.strip()
                solution = solution.replace(";","")
            stream_content = {'name': 'stdout', 'text': solution}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
