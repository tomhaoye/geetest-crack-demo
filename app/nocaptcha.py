import cv2
import time
from io import BytesIO
import PIL.Image as image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

origin_bg_path = '../pic/bg.jpg'
origin_fbg_path = '../pic/fbg.jpg'
merge_bg_path = '../pic/merged.jpg'
merge_fbg_path = '../pic/fmerged.jpg'

cut_image_path = '../pic/cut.jpg'
bin_bg_path = '../pic/bin_bg.bmp'
contour_bin_path = '../pic/contour.bmp'
opencv_bg_path = '../pic/opencv_bg.jpg'


def simulate():
    browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver")
    browser.implicitly_wait(5)
    wait = WebDriverWait(browser, 10)
    browser.get("http://www.geetest.com/type/")
    browser.find_elements_by_xpath("//div[@class='products-content']/ul/li")[1].click()
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "geetest_radar_tip")))
    browser.find_elements_by_class_name("geetest_radar_tip")[1].click() if len(
        browser.find_elements_by_class_name("geetest_radar_tip")) > 1 else browser.find_element_by_class_name(
        "geetest_radar_tip").click()
    time.sleep(2)
    return cut_gt_window_image(browser)


# 直接页面截取图片
def cut_gt_window_image(browser):
    image_div = browser.find_element_by_class_name("geetest_window")
    location = image_div.location
    size = image_div.size
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
        'width']
    screen_shot = browser.get_screenshot_as_png()
    screen_shot = image.open(BytesIO(screen_shot))
    captcha = screen_shot.crop((left, top, right, bottom))
    captcha = captcha.convert('RGB')
    captcha.save(cut_image_path)
    return browser


# 阈值二值化图片定位
def get_x_point(bin_img_path=''):
    tmp_x_cur = 0
    img = image.open(bin_img_path).load()
    # 缺口出现范围大概在x轴48-220,y轴15-145
    for y_cur in range(15, 145):
        b_acc = 0
        tmp_x_cur = 0
        for x_cur in range(48, 220):
            if img[x_cur, y_cur] == 0:
                if b_acc == 0:
                    tmp_x_cur = x_cur
                b_acc += 1
            else:
                if b_acc in range(36, 44):
                    return tmp_x_cur - 40 + b_acc
                else:
                    b_acc = 0
    return tmp_x_cur


# 阈值二值化
def get_bin_image(img_path='', save_path='', t_h=150, t_l=60):
    img = image.open(img_path)
    img = img.convert('L')
    table = []
    for i in range(256):
        if i in range(t_l, t_h):
            table.append(0)
        else:
            table.append(1)
    binary = img.point(table, '1')
    binary.save(save_path)


# 分割线二值化图片定位
def get_x_point_in_contour(bin_img_path=''):
    img = image.open(bin_img_path).load()
    # 滑块左边位置7px[6]处，获取滑块位置
    slider_left_x_index = 6
    slider_left = {}
    for y_cur in range(120):
        color_n = 0
        for add_to_next in range(40):
            color_n += img[slider_left_x_index, y_cur + add_to_next]
        slider_left[color_n] = y_cur
    y_start_cur = slider_left[max(slider_left)]
    # 缺口出现范围大概在x轴60-220,y轴15-145
    for x_cur in range(60, 230):
        for y_cur in range(15, 145):
            if img[x_cur, y_cur] == 255:
                if b_acc == 0:
                    tmp_x_cur = x_cur
                b_acc += 1
            else:
                if b_acc in range(36, 44):
                    print(x_cur, ' ', y_cur, ' ', b_acc)
                else:
                    b_acc = 0


# 明显分割线获取
def get_contour_image(img_path='', save_path=''):
    contour_img = image.new('L', (260, 160))
    img = image.open(img_path)
    img = img.convert('L')
    h_last_point = None
    v_last_point = None
    for x in range(260):
        for y in range(160):
            if v_last_point is not None and abs(img.getpixel((x, y)) - v_last_point) > 25:
                contour_img.putpixel((x, y), 255)
            v_last_point = img.getpixel((x, y))
    for y in range(160):
        for x in range(260):
            if h_last_point is not None and abs(img.getpixel((x, y)) - h_last_point) > 25:
                contour_img.putpixel((x, y), 255)
            h_last_point = img.getpixel((x, y))
    contour_img.save(save_path)


# 模拟滑动
def btn_slide(browser, x_offset=0):
    # 开始位置右偏6像素
    x_offset = abs(x_offset - 6 + 1)
    slider = browser.find_element_by_class_name("geetest_slider_button")
    ActionChains(browser).click_and_hold(slider).perform()
    section = x_offset
    left_time = 1
    x_move_list = get_x_move_speed(x_offset, left_time, section)
    print(x_move_list)
    print(sum(x_move_list))
    for x_move in x_move_list:
        ActionChains(browser).move_by_offset(x_move, yoffset=0).perform()
    ActionChains(browser).release().perform()
    time.sleep(2)
    browser.close()


def get_x_move_speed(distance=0, left_time=0, section=10):
    origin_speed = distance * 2
    acc_speed = origin_speed / left_time / left_time / section
    move_offset = []
    new_speed = origin_speed
    for i in range(0, section):
        new_speed = new_speed - acc_speed
        move_offset.append(round(new_speed / section))
        if sum(move_offset) >= distance:
            break
    if sum(move_offset) < distance:
        move_offset.append(distance - sum(move_offset))
    return move_offset


# opencv处理图片
def opencv_show(img_path=''):
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    grad_x = cv2.Sobel(img_gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad_y = cv2.Sobel(img_gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
    img_gradient = cv2.subtract(grad_x, grad_y)
    img_gradient = cv2.convertScaleAbs(img_gradient)

    blurred = cv2.GaussianBlur(img_gradient, (9, 9), 1.5, 9)
    (_, thresh) = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    cv2.imwrite(opencv_bg_path, closed)


t_browser = simulate()
# get_contour_image(cut_image_path, contour_bin_path)

get_bin_image(cut_image_path, bin_bg_path)
x = get_x_point(bin_bg_path)

# x = get_x_point_in_contour(contour_bin_path)
print(x - 6)
btn_slide(t_browser, x)

# opencv_show(cut_image_path)
