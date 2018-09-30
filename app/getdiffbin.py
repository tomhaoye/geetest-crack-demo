import PIL.Image as image

# 修改图片组
origin_bg_path = '../src/7.jpg'
origin_fbg_path = '../src/8.jpg'

merge_bg_path = '../src/merged.jpg'
merge_fbg_path = '../src/fmerged.jpg'
diff_path = '../src/diff.jpg'
large_diff_path = '../src/ldiff.jpg'
bin_path = '../src/bin.jpg'


# 混乱图片还原并灰度化
def merge_img(img_path='', target=''):
    im = image.open(img_path)
    to_image = image.new('RGB', (260, 160))
    dx = 12
    dy = 80
    x = 0
    img_map = {1: 18, 2: 17, 3: 15, 4: 16, 5: 22, 6: 21, 7: 14, 8: 13, 9: 10, 10: 9, 11: 19, 12: 20, 13: 2, 14: 1,
               15: 6, 16: 5, 17: 26, 18: 25, 19: 23, 20: 24, 21: 7, 22: 8, 23: 3, 24: 4, 25: 11, 26: 12}
    while x <= 300:
        y = 0
        while y <= 80:
            from_img = im.crop((x, y, x + dx, y + dy))
            second_line = img_map[(x / 12) if ((x / 12) % 2) else (x / 12 + 2)] - 1
            loc = ((img_map[x / 12 + 1] - 1) * 10 if y else second_line * 10, abs(y - dy))
            to_image.paste(from_img, loc)
            y += dy
        x += dx
    to_image = to_image.convert('L')
    to_image.save(target)
    return to_image


# 比对差异点
def get_diff_image(bg_path='', fbg_path='', save_path=''):
    bg_img = image.open(bg_path)
    fbg_img = image.open(fbg_path)
    img = image.new('L', (260, 160))
    for i in range(260):
        for j in range(160):
            if bg_img.getpixel((i, j)) != fbg_img.getpixel((i, j)):
                img.putpixel((i, j), bg_img.getpixel((i, j)))
            else:
                img.putpixel((i, j), 255)
    img.save(save_path)


# 记录超过阈值的差异点
def enlarge_diff_image(bg_path='', fbg_path='', save_path=''):
    bg_img = image.open(bg_path)
    fbg_img = image.open(fbg_path)
    img = image.new('L', (260, 160))
    for i in range(260):
        for j in range(160):
            if abs(bg_img.getpixel((i, j)) - fbg_img.getpixel((i, j))) > 40:
                img.putpixel((i, j), bg_img.getpixel((i, j)))
            else:
                img.putpixel((i, j), 255)
    img.save(save_path)


# 二值化
def get_bin_image(img_path=''):
    bg_img = image.open(img_path)
    table = []
    for i in range(256):
        table.append(0) if i < 160 else table.append(1)
    binary = bg_img.point(table, '1')
    binary.save(bin_path)


bg = merge_img(origin_bg_path, merge_bg_path)
fbg = merge_img(origin_fbg_path, merge_fbg_path)
get_diff_image(merge_bg_path, merge_fbg_path, diff_path)
enlarge_diff_image(merge_bg_path, merge_fbg_path, large_diff_path)
get_bin_image(large_diff_path)
