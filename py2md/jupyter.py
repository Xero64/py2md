from typing import TYPE_CHECKING, List, Dict

from jupyter_client import KernelManager
from nbformat.v4 import output_from_msg
from os import devnull
from queue import Empty

if TYPE_CHECKING:
    from jupyter_client import BlockingKernelClient

class JupyterKernel():
    kernel: 'KernelManager' = None
    curdir: str = None
    client: 'BlockingKernelClient' = None
    output: List[str] = None

    def __init__(self, kernel: str, curdir: str) -> None:
        self.kernel = KernelManager(kernel_name=kernel)
        self.curdir = curdir

    def start_kernel(self):
        self.kernel.start_kernel(cwd=self.curdir, stderr=open(devnull, 'w'))

    def start_client(self):
        self.client: 'BlockingKernelClient' = self.kernel.blocking_client()
        self.client.start_channels()
        try:
            self.client.wait_for_ready()
        except RuntimeError:
            self.stop_client()
            self.stop_kernel()
            raise RuntimeError('Timeout from starting kernel.')
        self.output = []

    def run_code(self, src: str) -> None:

        msg_id = self.client.execute(src.lstrip(), store_history=False)

        while True:
            try:
                msg = self.client.get_shell_msg(timeout=None)
            except Empty:
                try:
                    exception = TimeoutError
                except NameError:
                    exception = RuntimeError
                raise exception(
                    "Cell execution timed out, see log for details.")

            if msg['parent_header'].get('msg_id') == msg_id:
                break
            else:
                # not our reply
                continue

        while True:
            try:
                msg = self.client.get_iopub_msg(timeout=4)
            except Empty:
                outstr = 'Timeout waiting for IOPub output\n'
                outstr += 'Try restarting python session and running weave again\n'
                print(outstr)
                raise RuntimeError("Timeout waiting for IOPub output")

            if msg['parent_header'].get('msg_id') != msg_id and \
                msg['msg_type'] != "stream":
                continue

            msg_type: str = msg['msg_type']
            content: str = msg['content']

            if msg_type == 'status':
                if content['execution_state'] == 'idle':
                    break
                else:
                    continue
            elif msg_type == 'execute_input':
                continue
            elif msg_type == 'clear_output':
                self.output = []
                continue
            elif msg_type.startswith('comm'):
                continue

            try:
                out = output_from_msg(msg)
            except ValueError:
                print("unhandled iopub msg: " + msg_type)
            else:
                self.output.append(out)

    def run_cell(self, cell: Dict[str, str]) -> None:
        self.output = []
        content = cell['content']
        contentsplit = content.split('\n')
        code = ''
        for line in contentsplit:
            if line.strip() != '':
                code += line + '\n'
        self.run_code(code)
        return self.output

    def stop_client(self) -> None:
        self.client.stop_channels()

    def stop_kernel(self) -> None:
        self.kernel.shutdown_kernel()

    def __repr__(self) -> str:
        return '<py2md.JupyterKernel>'
