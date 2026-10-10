from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageOps, ImageDraw
root=Path(__file__).resolve().parent
pdf=pdfium.PdfDocument(str(root/'guide-layout.pdf'))
out=root/'render'; out.mkdir(exist_ok=True)
print('Pages',len(pdf))
for i,page in enumerate(pdf):
    text=page.get_textpage().get_text_range()
    print(i+1, text[:85].replace('\r',' ').replace('\n',' '), 'characters',len(text))
    im=page.render(scale=1.5).to_pil().convert('RGB')
    im.save(out/f'page-{i+1}.png')
for start in range(0,len(pdf),3):
    canvas=Image.new('RGB',(1800,890),'#ccd1d5')
    for j in range(start,min(start+3,len(pdf))):
        im=Image.open(out/f'page-{j+1}.png'); im.thumbnail((590,850))
        canvas.paste(im,((j-start)*600+5,25))
        ImageDraw.Draw(canvas).text(((j-start)*600+8,5),f'Page {j+1}',fill='black')
    canvas.save(out/f'overview-{start//3+1}.png')
