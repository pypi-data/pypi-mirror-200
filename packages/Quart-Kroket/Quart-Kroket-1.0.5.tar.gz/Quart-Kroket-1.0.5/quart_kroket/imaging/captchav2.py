"""
This file is called 'captchav2' because

"""
import os
import string
from uuid import uuid4
from random import random, SystemRandom

import PIL.ImageOps
from PIL import Image, ImageFilter
from captcha.image import ImageCaptcha

FONT_DEFAULT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DejaVuSansMono.ttf")


class ImageClassExample(ImageCaptcha):
    # override for different colors
    def generate_image(self, chars):
        background = (255, 255, 255, 255)
        color = (155, 28, 46, 255)
        im = self.create_captcha_image(chars, color, background)
        self.create_noise_dots(im, color)
        self.create_noise_curve(im, color)
        im = im.filter(ImageFilter.SMOOTH)
        return im


def generate_captcha(secret: str = None, font: str = FONT_DEFAULT, num_chars: int = 4, image_class: ImageCaptcha = ImageClassExample):
    """
    Returns the image data and secret string
    Args:
        secret: auto-generated if left empty
        font: Path to a font file. Defaults to 'DejaVuSansMono.ttf'
        num_chars:
        image_class: Override to get custom colors
    Returns:
    """
    if not secret:
        secret = ''.join(
            SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(num_chars))

    image = ImageClassExample(fonts=[font])
    data = image.generate(secret)

    return {
        'image': data,
        'secret': secret
    }
