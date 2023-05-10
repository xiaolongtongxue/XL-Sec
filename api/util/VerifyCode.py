import base64
import random
import os
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageFilter

"""
该文件是为了解决验证码图片的生成而专门设置在这里的，具体用法就像这样：
verification_code, image_base64 = generate_verification_code_image(size=(130, 55), length=4)
该函数返回的第一个参数的内容为验证码的内容，第二个内容则为生成图片的base64的值，直接就可以拿去加载用
相关参数：size表示的是生成的验证码的尺寸，length表示验证码的长度
"""


def generate_verification_code_image(size=(130, 50), length=4):
    image_code = Image.new('RGB', size=size, color=(
        220, 230, 240))  # random_color())
    font = ImageFont.truetype(os.path.abspath(os.path.dirname(__file__)) + '/ttf/times.ttf', size=40)
    draw = ImageDraw.Draw(image_code)
    code = random_string(length)
    for i, value in enumerate(code):
        draw.text((5 + random.randint(4, 7) + 25 * i, 1 + random.randint(2, 8) + 2 * i), text=value,
                  fill=random_color(), font=font)
    # 绘制干扰直线
    for j in range(random.randint(5, 8)):
        x1 = random.randint(0, 130)
        y1 = random.randint(0, 25)
        x2 = random.randint(0, 130)
        y2 = random.randint(25, 50)
        draw.line(((x1, y1), (x2, y2)), fill=random_color())
    for k in range(random.randint(5, 8)):
        start = (-50, -50)  # 起始位置在外边看起来才会像弧线
        end = (130 + 10, random.randint(0, 50 + 10))
        draw.arc(start + end, 0, 360, fill=random_color())
    for m in range(130):
        for n in range(50):
            number = random.randint(1, 100)
            if number > 90:
                draw.point((m, n), fill=random_color())
    image_code = image_code.filter(ImageFilter.SMOOTH)
    return code, image_to_base64(image_code)


def image_to_base64(image_code: Image.Image, fmt='png') -> str:
    output_buffer = BytesIO()
    image_code.save(output_buffer, format=fmt)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return f'data:image/{fmt};base64,' + base64_str


def random_string(length=32):
    string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(string) for _ in range(length))


def random_color():
    r, g, b = random.randint(0, 200), random.randint(
        0, 200), random.randint(0, 200)
    if r * 0.299 + g * 0.578 + b * 0.114 < 150:
        return r, g, b
    else:
        return random_color()


if __name__ == '__main__':
    pass
    # verification_code, image_base64 = generate_verification_code_image(
    #     size=(130, 65), length=4)
    # print(verification_code)
    # print(image_base64)

    # # session[
    # #     'verification_code'] = verification_code  # 多人访问时，验证码会存在各自的session里，不会发生后访问的人的验证码覆盖前面的人的验证码。若放在redis缓存里，写cache.set('verification_code',verification_code,timeout=120)会发生前面说的覆盖的情况，因每次存入redis的键值对的键相同
    # buffer = BytesIO()
    # image.save(buffer, "PNG")  # 将Image对象转为二进制存入buffer。因BytesIO()是在内存中操作，所以实际是存入内存
    # buf_bytes = buffer.getvalue()  # 从内存中取出bytes类型的图片
    # print(type(buf_bytes))
    # print(buf_bytes.decode())
    # response = make_response(buf_bytes)
