from jupyter_client import KernelManager
from nbformat.v4 import output_from_msg
from os import devnull
from queue import Empty

class JupyterKernel(object):
    kernel = None
    curdir = None
    client = None
    output = None
    def __init__(self, kernel: str, curdir: str):
        self.kernel = KernelManager(kernel_name=kernel)
        self.curdir = curdir
    def start_kernel(self):
        self.kernel.start_kernel(cwd=self.curdir, stderr=open(devnull, 'w'))
    def start_client(self):
        self.client = self.kernel.client()
        self.client.start_channels()
        try:
            self.client.wait_for_ready()
        except RuntimeError:
            print("Timeout from starting kernel\nTry restarting python session and running weave again")
            self.client.stop_channels()
            self.client.shutdown_kernel()
            raise
        self.output = []
    def run_code(self, src: str):
        
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
                # We've already waited for execute_reply, so all output
                # should already be waiting. However, on slow networks, like
                # in certain CI systems, waiting < 1 second might miss messages.
                # So long as the kernel sends a status:idle message when it
                # finishes, we won't actually have to wait this long, anyway.
                msg = self.client.iopub_channel.get_msg(block=True, timeout=4)
            except Empty:
                print("Timeout waiting for IOPub output\nTry restarting python session and running weave again")
                raise RuntimeError("Timeout waiting for IOPub output")

            #stdout from InProcessKernelManager has no parent_header
            if msg['parent_header'].get('msg_id') != msg_id and msg['msg_type'] != "stream":
                continue

            msg_type = msg['msg_type']
            content = msg['content']

            # set the prompt number for the input and the output
            # if 'execution_count' in content:
            #     cell['execution_count'] = content['execution_count']

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
    def run_cell(self, cell: dict):
        self.output = []
        content = cell['content']
        contentsplit = content.split('\n')
        code = ''
        for line in contentsplit:
            if line.strip() != '':
                code += line + '\n'
        self.run_code(code)
        return self.output
    def stop_client(self):
        self.client.stop_channels()
    def stop_kernel(self):
        self.kernel.shutdown_kernel()
