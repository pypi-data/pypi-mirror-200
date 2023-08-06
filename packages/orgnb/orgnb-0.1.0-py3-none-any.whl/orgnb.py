#!/usr/bin/env python

import base64, re, os

"""
Convert org mode file as jupyter notebook.
"""

# The following does not transform code blocks into code cells
# output = pypandoc.convert_file(sys.argv[1],
#                                to='ipynb',
#                                format='org')


def parse_headlines_org_file(headlines, file_handle):
    """
    Extract headlines from `file_handle`.

    Parameters:
    ----------
    - headlines : list of headlines
    - file_handle : input org mode file

    Return:
    ------
    - list of headlines
    """
    state = True
    text = []
    for line in file_handle:
        line = line.strip('\n')
        if line.startswith('* '):
            headline = line.split('* ')[1]
            state = False
            for selected_headline in headlines:
                if headline == selected_headline:
                    state = True
                    break
        if state:
            text.append(line)

    return text


def parse_org_file(file_handle):
    """
    Extract code and text blocks from `file_handle`.

    Parameters:
    ----------
    - file_handle : input org mode file

    Return:
    ------
    - list of blocks
    - list of block types
    """
    cells, cells_type, block = [], [], []
    state = None
    for line in file_handle:
        line = line.strip('\n')
        if line.startswith('#+begin'):
            # We store the current block as text
            # unless all lines are empty
            non_empty = sum([len(_) > 0 for _ in block])
            if non_empty > 0:
                cells.append(block)
                cells_type.append('text')
            # Reading a new code block
            if line.startswith('#+begin'):
                state = line[8: ]  # strip #+begin
                if len(line.split()) > 1:
                    state = line.split()[1]
                
            block = []

        elif line.startswith('#+end'):
            # We store the current block as code
            assert state != 'text'
            if state == 'example' or state == 'quote':
                block.insert(0, '```')
                block.append('```')
            cells.append(block)
            cells_type.append(state)
            # Reading a new text block. If there are consecutive code
            # blocks, empty text blocks are removed.
            state = 'text'
            block = []

        elif ':ARCHIVE:' in line or line.startswith('#+') or line.startswith(':'):
            # Skip results blocks
            pass

        else:
            # This is a text block
            if state is None:
                block = []
                state = 'text'
            block.append(line)

    return cells, cells_type


def convert_to_text(cells, cells_type, file_out, dir_inp):
    """
    Write cells to stdout

    Parameters:
    ----------
    - cells : list of cells
    - cells_type : list of types of cells (text or code)
    """
    for e, t in zip(cells, cells_type):
        if t == 'text':
            print('\n'.join(e))
        else:
            line = '-' * 64
            print(line[:-len(t)] + t)
            print('\n'.join(e))
            print('-' * 64)


def attach_images(block, dir_inp):
    """
    Attach images in markdown broken links like (`![](...)`) as
    attachments and fix the link.
    """
    new_block = []
    attachments = {}
    for line in block.split('\n'):
        if line.startswith('![]'):
            match = re.search(r'!\[\]\((\S*)\)', line)
            file_path = match.group(1)
            line = f'![{file_path}](attachment:{file_path})'
            full_path = os.path.join(dir_inp, file_path)
            # image = "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
            image = base64.encodestring(open(full_path, "rb").read()).decode().replace('\n', '')
            attachments[file_path] = {'image/png': image}
        new_block.append(line)
    block = '\n'.join(new_block)
    return block, attachments


def convert_to_nb(cells, cells_type, file_out, dir_inp, include=None, exclude=None):
    """
    Convert list of cells to jupyter notebook format

    Parameters:
    ----------
    - cells : list of cells
    - cells_type : list of types of cells (text or code)
    - file_out : path to output notebook file
    """
    import nbformat
    nb = nbformat.v4.new_notebook()
    for e, t in zip(cells, cells_type):
        if (include and t not in include) or (exclude and t in exclude):
            continue
        if t == 'text':
            # This is a text block
            from pypandoc import convert_text
            block = '\n'.join(e)
            block = convert_text(block, 'markdown-simple_tables+grid_tables', 'org')
            block, attachments = attach_images(block, dir_inp)
            nb['cells'].append(nbformat.v4.new_markdown_cell(source=block, attachments=attachments))
        elif t == 'python':
            # This is a python code block
            block = '\n'.join(e)
            nb['cells'].append(nbformat.v4.new_code_cell(source=block))
        elif t == 'sh':
            # This is a shell block, we add ! to the beginning of the lines
            block = '\n'.join(['! '+ line for line in e])
            nb['cells'].append(nbformat.v4.new_code_cell(source=block))
        else:
            # This includes example and quote blocks
            block = '\n'.join(e)
            nb['cells'].append(nbformat.v4.new_markdown_cell(source=block))

    nbformat.write(nb, file_out)


def main(debug=False, include='', exclude='ditaa', *files):
    convert = convert_to_nb
    if debug:
        convert = convert_to_text
        
    for file_inp in files:
        if debug:
            file_out = '/dev/stdout'
        else:
            file_out = file_inp[:-4] + '.ipynb'
        with open(file_inp) as fh:
            cells, cells_type = parse_org_file(fh)
            convert(cells, cells_type, file_out, os.path.dirname(fh.name), include, exclude)

def cli():
    import argh
    argh.dispatch_command(main)

            
if __name__ == '__main__':
    import argh
    argh.dispatch_command(main)
