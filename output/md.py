from inspect import getfile, currentframe
from os.path import abspath, join, basename
from base64 import b64decode

class MDWriter(object):
    destfilepath = None
    destfile = None
    imgcount = None
    def __init__(self, destfilepath: str):
        self.destfilepath = destfilepath
        self.imgcount = 0
    def open_file(self):
        self.destfile = open(self.destfilepath, 'wt')
    def write_cell(self, cell: dict):
        if cell['type'] == 'code':
            self.write_codeblock(cell)
        self.write_mdblock(cell)
    def write_codeblock(self, cell: dict):
        content = cell['content']
        label = cell['label']
        self.destfile.write(f'\n# {label:s}\n')
        self.destfile.write('``` python\n')
        contentsplit = content.split('\n')
        for line in contentsplit:
            if line.strip() != '':
                self.destfile.write(f'{line:s}\n')
        self.destfile.write('```\n')
    def write_mdblock(self, cell: dict):
        results = cell['results']
        groups = []
        group = {}
        for result in results:
            if result['output_type'] == 'display_data':
                data = result['data']
                if 'text/plain' in data and len(data) == 1:
                    if 'type' in group:
                        if group['type'] == 'text/plain':
                            group['result'] += data['text/plain'] + '\n'
                    else:
                        group['type'] = 'text/plain'
                        group['result'] = data['text/plain'] + '\n'
                else:
                    if 'type' in group:
                        if group['type'] == 'text/plain':
                            groups.append(group)
                            group = {}
                    if 'text/markdown' in data:
                        group['type'] = 'text/markdown'
                        group['result'] = data['text/markdown']
                        groups.append(group)
                        group = {}
                    elif 'text/html' in data:
                        group['type'] = 'text/html'
                        group['result'] = data['text/html']
                        groups.append(group)
                        group = {}
                    if 'image/svg+xml' in data:
                        group['type'] = 'image/svg+xml'
                        group['result'] = data['image/svg+xml']
                        groups.append(group)
                        group = {}
                    elif 'image/png' in data:
                        group['type'] = 'image/png'
                        group['result'] = data['image/png']
                        groups.append(group)
                        group = {}
        if 'type' in group:
            if group['type'] == 'text/plain':
                groups.append(group)
                group = {}
        for group in groups:
            if group['type'] == 'text/plain':
                self.destfile.write('```\n')
                self.destfile.write('{:s}'.format(group['result']))
                self.destfile.write('```\n')
            elif group['type'] == 'text/markdown':
                self.destfile.write('{:s}'.format(group['result']))
            elif group['type'] == 'text/html':
                self.destfile.write('<div>\n')
                self.destfile.write('{:s}'.format(group['result']))
                self.destfile.write('</div>\n')
            elif group['type'] == 'image/svg+xml':
                self.imgcount += 1
                imgfilepath = self.destfilepath.replace('md', f'{self.imgcount}.svg')
                with open(imgfilepath, 'wt') as imgfile:
                    imgfile.write(group['result'])
                mdstr = f'![]({imgfilepath:s})\n'
                self.destfile.write(mdstr)
            elif group['type'] == 'image/png':
                self.imgcount += 1
                imgfilepath = self.destfilepath.replace('md', f'{self.imgcount}.png')
                with open(imgfilepath, 'wb') as imgfile:
                    imgfile.write(b64decode(group['result']))
                mdstr = f'![]({imgfilepath:s})\n'
                self.destfile.write(mdstr)
            else:
                self.destfile.write('{:s}'.format(group['result']))
    def close_file(self):
        self.destfile.close()
