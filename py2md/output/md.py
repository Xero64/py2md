from typing import TextIO, Dict

from base64 import b64decode

class MDWriter():
    destfilepath: str = None
    destfile: 'TextIO' = None
    imgcount: int = None

    def __init__(self, destfilepath: str) -> None:
        self.destfilepath = destfilepath
        self.imgcount = 0

    def open_file(self) -> None:
        self.destfile = open(self.destfilepath, 'wt', encoding='utf-8')

    def write_cell(self, cell: Dict[str, str],
                   inline: bool=False,
                   nocode: bool=False,
                   nohead: bool=False) -> None:
        if cell['type'] == 'code':
            self.write_codeblock(cell, nocode, nohead)
        self.write_mdblock(cell, inline)

    def write_codeblock(self, cell: Dict[str, str],
                        nocode: bool=False,
                        nohead: bool=False) -> None:
        if not nohead:
            label = cell['label']
            self.destfile.write(f'\n# {label:s}\n')
        if not nocode:
            content = cell['content']
            self.destfile.write('``` python\n')
            contentsplit = content.split('\n')
            for line in contentsplit:
                if line.strip() != '':
                    self.destfile.write(f'{line:s}\n')
            self.destfile.write('```\n')

    def write_mdblock(self, cell: Dict[str, str],
                      inline: bool=False) -> None:
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
            elif result['output_type'] == 'stream':
                if 'text' in result:
                    group['type'] = 'text'
                    group['result'] = result['text']
                    groups.append(group)
                    group = {}
            elif result['output_type'] == 'error':
                if 'evalue' in result:
                    group['type'] = 'error'
                    group['result'] = result['evalue']
                    groups.append(group)
                    group = {}
        if 'type' in group:
            if group['type'] == 'text/plain':
                groups.append(group)
                group = {}
        for group in groups:
            if group['type'] == 'text/plain' or \
                group['type'] == 'text' or group['type'] == 'error':
                self.destfile.write('\n```\n')
                self.destfile.write('{:s}'.format(group['result']))
                self.destfile.write('\n```\n')
            elif group['type'] == 'text/markdown':
                self.destfile.write('{:s}'.format(group['result']))
            elif group['type'] == 'text/html':
                self.destfile.write('<div>\n')
                self.destfile.write('{:s}'.format(group['result']))
                self.destfile.write('</div>\n')
            elif group['type'] == 'image/svg+xml':
                if inline:
                    grpres: str = group['result']
                    svgtext: str = grpres.replace('\r\n', '\n')
                    svgbeg = svgtext.find('<svg ')
                    svgtext = '\n' + svgtext[svgbeg:] + '\n'
                    self.destfile.write(svgtext)
                else:
                    self.imgcount += 1
                    repstr = f'{self.imgcount}.svg'
                    imgfilepath = self.destfilepath.replace('md', repstr)
                    with open(imgfilepath, 'wt', encoding='utf-8') as imgfile:
                        imgfile.write(group['result'])
                    mdstr = f'![]({imgfilepath:s})\n'
                    self.destfile.write(mdstr)
            elif group['type'] == 'image/png':
                if inline:
                    pngtext = group['result']
                    outtext = '\n<img alt="" src="data:image/png;base64,'
                    outtext += pngtext + '" />\n'
                    self.destfile.write(outtext)
                else:
                    self.imgcount += 1
                    repstr = f'{self.imgcount}.png'
                    imgfilepath = self.destfilepath.replace('md', repstr)
                    with open(imgfilepath, 'wb') as imgfile:
                        imgfile.write(b64decode(group['result']))
                    mdstr = f'![]({imgfilepath:s})\n'
                    self.destfile.write(mdstr)
            else:
                self.destfile.write('{:s}'.format(group['result']))

    def close_file(self) -> None:
        self.destfile.close()

    def __repr__(self) -> str:
        return '<py2md.MDWriter>'
