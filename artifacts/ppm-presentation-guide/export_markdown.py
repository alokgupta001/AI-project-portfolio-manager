from pathlib import Path
import re
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

root = Path(__file__).resolve().parents[2]
source = root / 'artifacts/ppm-presentation-guide/build_document.py'
output = root / 'enterprise-ppm/docs/06-user-guides/PROJECT_PRESENTATION_GUIDE.md'
# Reuse the saved authoring content in memory without opening or changing Word.
namespace = {'__file__': str(source), '__name__': '__markdown_export__'}
authoring = source.read_text(encoding='utf-8').split('OUT.parent.mkdir', 1)[0]
exec(compile(authoring, str(source), 'exec'), namespace)
doc = namespace['doc']

def formatted(paragraph):
    chunks = []
    for run in paragraph.runs:
        text = run.text
        if not text:
            continue
        stripped = text.strip()
        if not stripped:
            chunks.append(text)
            continue
        prefix = text[:len(text) - len(text.lstrip())]
        suffix = text[len(text.rstrip()):]
        if run.bold:
            chunks.append(prefix + '**' + stripped + '**' + suffix)
        elif run.italic:
            chunks.append(prefix + '*' + stripped + '*' + suffix)
        else:
            chunks.append(text)
    result = ''.join(chunks).strip()
    for label in ['Presentation sentence', 'Information to enter', 'Why it is needed', 'Example', 'Long term value', 'Current capability', 'Example question']:
        result = result.replace('**' + label + '** ', '**' + label + ':** ', 1)
    return result

def cell_text(cell):
    return '<br>'.join(formatted(p) for p in cell.paragraphs if p.text.strip()).replace('|', '\\|')

blocks = []
for child in doc.element.body:
    if child.tag == qn('w:p'):
        para = Paragraph(child, doc)
        if not para.text.strip():
            continue
        style = para.style.name
        if style == 'Title':
            blocks.append('# ' + para.text)
        elif style == 'Subtitle':
            blocks.append('*' + para.text + '*')
        elif style == 'Heading 1':
            blocks.append('## ' + para.text)
        elif style == 'Heading 2':
            blocks.append('### ' + para.text)
        elif style == 'List Bullet':
            blocks.append('- ' + formatted(para))
        elif re.match(r'^\d+\. ', para.text):
            blocks.append(para.text)
        else:
            blocks.append(formatted(para))
    elif child.tag == qn('w:tbl'):
        table = Table(child, doc)
        rows = [[cell_text(c) for c in row.cells] for row in table.rows]
        lines = ['| ' + ' | '.join(rows[0]) + ' |', '| ' + ' | '.join(['---'] * len(rows[0])) + ' |']
        lines.extend('| ' + ' | '.join(row) + ' |' for row in rows[1:])
        blocks.append('\n'.join(lines))

# Keep adjacent Markdown list items together while separating other blocks.
text = ''
previous_list = None
for block in blocks:
    list_type = 'bullet' if block.startswith('- ') else 'number' if re.match(r'^\d+\. ', block) else None
    text += ('\n' if list_type and previous_list == list_type else '\n\n') if text else ''
    text += block
    previous_list = list_type
text += '\n'
output.write_text(text, encoding='utf-8')
print(output)
print(f'{len(text.split())} words; {len(text.splitlines())} lines')
