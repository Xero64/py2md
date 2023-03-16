#%%
# Import Dependencies
from os.path import abspath, split
from jupyter_client.manager import KernelManager
from nbformat.v4 import output_from_msg
from queue import Empty
from os import devnull

#%%
# Start Variables
kernel_name = 'python3'
source = './'
curdir = split(abspath(source))[0]

kernel = KernelManager(kernel_name=kernel_name)
kernel.start_kernel(cwd=curdir, stderr=open(devnull, 'w'))

client = kernel.blocking_client()
client.start_channels()

try:
    client.wait_for_ready()
except RuntimeError:
    print("Timeout from starting kernel\nTry restarting python session and running weave again")
    client.stop_channels()
    client.shutdown_kernel()
    raise
output = []

code = 'a = 10\nprint(f"a = {a:d}")'

msg_id = client.execute(code, store_history=False)

while True:
    try:
        msg = client.get_shell_msg(timeout=None)
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
        continue

while True:
    try:
        msg = client.get_iopub_msg(timeout=4)
    except Empty:
        print("Timeout waiting for IOPub output\nTry restarting python session and running weave again")
        raise RuntimeError("Timeout waiting for IOPub output")

    if msg['parent_header'].get('msg_id') != msg_id and msg['msg_type'] != "stream":
        continue

    msg_type = msg['msg_type']
    content = msg['content']

    if msg_type == 'status':
        if content['execution_state'] == 'idle':
            break
        else:
            continue
    elif msg_type == 'execute_input':
        continue
    elif msg_type == 'clear_output':
        output = []
        continue
    elif msg_type.startswith('comm'):
        continue

    try:
        out = output_from_msg(msg)
    except ValueError:
        print("unhandled iopub msg: " + msg_type)
    else:
        output.append(out)

client.stop_channels()
kernel.shutdown_kernel()

print(f'output = {output}\n')
