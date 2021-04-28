import requests
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO
import pytesseract
import os


def get_image(url):
    r = requests.get(url)
    return Image.open(BytesIO(r.content))


def get_image_from_shoob(url):
    i = get_image(url)
    return i.crop((21, 360, 280, 427))


def get_image_file(filename):
    i = Image.open(filename)
    return i


def process(img):
    p = img.load()
    l, r = img.size[0], -1
    for i in range(img.size[0]):
        cnt = 0
        for j in range(img.size[1]):
            if p[i, j] == 0:
                cnt += 1
            if cnt > 2:
                break
        if cnt >= 3:
            r = max(i, r)
            l = min(i, l)
        # print(i,j,p[i,j])
    return img.crop((max(l - 5, 0), 0, min(r + 5, img.size[0]), img.size[1]))

def process2(img):
  img2 = ImageOps.invert(img)
  k = img2.filter(ImageFilter.ModeFilter(size=5))
  l = k.filter(ImageFilter.GaussianBlur(radius=9))
  m = Image.composite(img2,k,l).convert('L')
  return ImageOps.invert(m)

def init_tesseract():
  os.system('install-pkg tesseract-ocr')
  os.environ['TESSDATA_PREFIX'] = "/home/runner/QuizBot/tessdata"

if __name__ == '__main__':
    img = get_image_file('826498439936344115.png').convert('1').convert('L')
    i = process(img)
    img2 = ImageOps.invert(i)
    # img2 = i
    # img2 = invert(i)
    # i = j.filter(ImageFilter.MinFilter).filter(ImageFilter.MaxFilter).filter(ImageFilter.MaxFilter).filter(ImageFilter.MinFilter)
    # print(pytesseract.image_to_string(j))
    # j = j.filter(ImageFilter.MinFilter)
    # print(pytesseract.image_to_string(j))
    # j = j.filter(ImageFilter.MaxFilter)
    # print(pytesseract.image_to_string(j))
    # j = j.filter(ImageFilter.MaxFilter)
    # print(pytesseract.image_to_string(j))
    # j = j.filter(ImageFilter.MinFilter)
    # print(pytesseract.image_to_string(j))
    # j.save('zzz.png')
    # j = i
    # j = j.filter(ImageFilter.MaxFilter)
    # j = img2.filter(ImageFilter.ModeFilter(size=3))
    k = img2.filter(ImageFilter.ModeFilter(size=5))
    # l = img2.filter(ImageFilter.ModeFilter(size=7))
    # .filter(
    #     ImageFilter.Kernel((3, 3), (3, 0, 3, 0, 1, 0, 3, 0, 3), 13, 0))
    # .filter(ImageFilter.Kernel((5, 5),
    # (1/10, 1/10, 1/10, 1/10, 1/10,
    # 0, 0, 0, 0,0,
    # 0, 0, 0, 0,0,
    # 0, 0, 0, 0,0,
    # 1/10, 1/10, 1/10, 1/10, 1/10), 1, 0))
    # .filter(ImageFilter.Kernel((3, 3),(0,0,0,1/6, 1/6, 1/6, 1/6, 1/6, 1/6), 1, 0))
    # .filter(ImageFilter.MedianFilter(size=3)).filter(ImageFilter.MedianFilter(size=3)).filter(ImageFilter.MedianFilter(size=3))
    # .filter(ImageFilter.MinFilter)
    # print(pytesseract.image_to_string(img2))
    # img2 = j
    # img2 = Image.blend(j,k,0.5)
    # img3 = Image.blend(k,l,0.5)
    # img4 = Image.blend(img2,img3,0.5)
    # img5 = invert(img4)
    # img5 = invert(k)
    # k = k.filter(ImageFilter.BoxBlur(2))
    l = k.filter(ImageFilter.GaussianBlur(radius=9))
    

    
    # m = ImageOps.invert(k)
    m = Image.composite(img2,k,l).convert('L')
    z = ImageOps.invert(m)
    z.save('zzz.png')
    # j = i.filter(ImageFilter.MinFilter).filter(ImageFilter.MaxFilter).filter(ImageFilter.MaxFilter).filter(ImageFilter.MinFilter)
    print('OCR')
    print(pytesseract.image_to_string(z))
    # j.save('zzz1.png')


def image_to_bin(im):
    img_byte_arr = BytesIO()
    im.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
