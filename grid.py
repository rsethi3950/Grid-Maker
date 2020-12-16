from PIL import Image, ImageDraw, ImageFont
import PIL, os
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'static', 'uploads')

c=1.5
d = dict()

# fixed size of boxes 48,60,72
def makeGrid(gap, color, filename, stroke):
  dest=os.path.join(UPLOADED_PHOTOS_DEST,filename)
  initimg = Image.open(dest).convert("L")
  initimg = initimg.resize((int(initimg.width*c),int(initimg.height*c)))
  img = Image.new('RGB',(initimg.width, initimg.height))
  d["small"] = img.width//16
  d["medium"] = img.width//12
  d["large"] = img.width//8
  gap = d[gap]

  img.paste(initimg,(0,0))
  fnt = ImageFont.truetype('./Robot.ttf',30)
  drawing = ImageDraw.Draw(img)
  print('{}x{}'.format(img.width,img.height))
  x=1
  y=1
  for i in range(0, img.width, gap):
    drawing.line((i,0,i,img.height),fill=color, width=stroke)
    drawing.text((i,0),str(y),font=fnt,fill=color)
    y=y+1
  
  for j in range(0, img.height, gap):
    drawing.line((0,j,img.width,j),fill=color, width=stroke)
    drawing.text((0,j),str(x),font=fnt,fill=color)
    x=x+1
  img.save(dest)
 