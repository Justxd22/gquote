try: from PIL import Image, ImageFont, ImageDraw
except: print("pillow not found, use pip to install")
from textwrap import wrap as wr
from requests import get
from io import BytesIO
import json


class gquote:
    def __init__(self, base = None, headers = None, proxy = None, output = True, format = "png", fonts = None):
        self.base    = "https://zenquotes.io/api/random" if not base else base
        self.headers = headers
        self.proxy  = proxy
        self.format = format
        self.output = False
        if output:
            if type(output) is str:
                if "." in output: self.output = output
                else: raise ValueError("output path should include output format e.g: /home/xd/quote.png")
            else: self.output = "./quote.png"
        self.fonts = ["./fonts/Barkentina.ttf", "./fonts/Ubuntu-Italic.ttf"]
        if fonts and type(fonts) is list and len(fonts) >= 2: self.fonts = fonts
        
    def run(self):
        tquote = get(self.base, headers=self.headers, proxies=self.proxy)
        if tquote.status_code != 200:
            print("bad api!", tquote.status_code)
            exit(1)
        # Edit the following according to your api
        # you should give quote and author vars
        # it will do the rest!
        tquote = json.loads(tquote.text)
        quote  = tquote[0]['q']
        self.author = "~ " + tquote[0]['a'] + " ~"
        # leave these
        self.quote  = "“" + quote + "”"
        wquote = wr(self.quote, width=18)
        # new 16:9 image
        im   = Image.new("RGB", (1080,1920))
        draw = ImageDraw.Draw(im)
        # load fonts
        font  = ImageFont.truetype(self.fonts[0], 100)
        sfont = ImageFont.truetype(self.fonts[1], 40)
        # try to center text
        padding = 50; ch = 400;
        for i in wquote:
            w, h = draw.textsize(i, font=font)
            draw.text( ( (1080-w)/2, ch), i, font=font)
            ch += h + padding
        # finally draw author with diffrent font
        w, h = draw.textsize(self.author, font=sfont)
        draw.text( ( (1080-w)/2, ch+80), self.author, font=sfont)
        # export
        if self.output: im.save(self.output)
        else: # export to memory
            out = BytesIO()
            im.save(out, format=self.format, quality=100)
            return out
        
        print('saved to ', self.output)
        return self.output
