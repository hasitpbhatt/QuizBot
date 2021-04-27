import requests
from PIL import Image
from io import BytesIO

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
            if p[i, j] == 17:
                cnt += 1
            if cnt > 2:
                break
        if cnt >= 3:
            r = max(i, r)
            l = min(i, l)
    return img.crop((max(l - 5, 0), 0, min(r + 5, img.size[0]), img.size[1]))


if __name__ == '__main__':
    img = get_image_file('826498439936344115.png').convert('L')
    process(img).save('zzz.png')


def image_to_bin(im):
    img_byte_arr = BytesIO()
    im.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
