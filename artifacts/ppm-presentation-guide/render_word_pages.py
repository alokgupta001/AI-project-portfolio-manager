from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
pdf = pdfium.PdfDocument(str(ROOT / 'word-layout.pdf'))
OUT = ROOT / 'render'
OUT.mkdir(exist_ok=True)
print('Pages', len(pdf))
texts = []
for i in range(len(pdf)):
    page = pdf[i]
    text = page.get_textpage().get_text_range()
    texts.append(text)
    img = page.render(scale=1.65).to_pil().convert('RGB')
    img.save(OUT / f'page-{i+1}.png')
    print(i+1, 'words', len(text.split()), text[:100].replace('\r',' ').replace('\n',' '))
    page.close()
(OUT / 'rendered-text.txt').write_text('\n\n'.join(texts), encoding='utf-8')
for start in range(0, len(pdf), 3):
    canvas = Image.new('RGB', (1800, 890), '#CFD4DB')
    for j in range(start, min(start+3, len(pdf))):
        im = Image.open(OUT / f'page-{j+1}.png')
        im.thumbnail((580, 840))
        canvas.paste(im, ((j-start)*600+10, 28))
        ImageDraw.Draw(canvas).text(((j-start)*600+10, 8), f'Page {j+1}', fill='black')
    canvas.save(OUT / f'overview-{start//3+1}.png')
