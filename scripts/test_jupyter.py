from os.path import abspath, split
from py2web.jupyter import JupyterKernel

kernel = 'python3'

curdir = split(abspath(__file__))[0]

jk = JupyterKernel(kernel, curdir)
jk.start_kernel()
jk.start_client()

src = 'print("Hello World")\nb=3'
jk.run_code(src)

src = 'a = 2'
jk.run_code(src)

src = 'print("a = {:}".format(a))'
jk.run_code(src)

src = 'print("b = {:}".format(b))'
jk.run_code(src)

jk.stop_client()
jk.stop_kernel()

for out in jk.output:
    print(out)

pass
