"""
Image Utils
"""

import os
import logging
from PIL import Image

logger = logging.getLogger('custom_image_utils')


class CustomImage(Image.Image):
    """
    Simple image creation API using PIL Library
    """
    default_image_path = None
    default_mode = '1'  # 1-bit pixels, black and white, stored with one pixel per byte
    default_size = (1,1) # Single Pixel
    default_color = 0  # Black
    def __init__(self, **kwargs):
        """
        creates an empty image using the settings as a placeholder
        :param kwargs: Settings (Default Image size , Default Color ...)
        """
        self.settings = kwargs
        self.image = self.create_default_image()
        self.image_path = CustomImage.default_image_path

    def create_default_image(self):
        """
        Creates an empty single pixel image and set image attribute
        """
        self.image = Image.new(CustomImage.default_mode,
                               CustomImage.default_size,
                               CustomImage.default_color)
        logger.debug('Default image created')

    def change_image_path(self, image_path):
        if self.is_valid_path(image_path) is True:
            self.image_path = image_path

    def open_image(self, image_path):
        """
        sets image attribute to an Image type
        :param image_path:
        """
        if self.is_valid_path(image_path) is True:
            self.image = Image.open(image_path)
            logger.info(f'image from {image_path} opened')

    def get_image_data(self):
        """
        Get the data from image_data attribute
        """
        self.image_data = self.image.getdata()
        logger.debug(f'Image data :\n{self.image_data}')

    def convert_image(self, mode):
        """
        Available modes:
        https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes

        """
        self.image.convert(mode)
        logger.info(f'Image converted to {mode}')

    def change_image_color(self, new_color=(0, 0, 0)):
        """
        Appends a new color to image_data
        """

        for item in self.image_data:
            if item[0] in list(range(200, 256)):
                new_image_data.append(new_color)
            else:
                new_image_data.append(item)
        logger.info(f'New color to {new_color}')

    def save_image(self, path):
        """
        Saves the image to path location
        :param path:
        """
        self.image.save(path)
        logger.debug('image saved to {}'.format(path))

    def is_valid_path(self, path):
        valid = False

        # Path exists
        if os.path.exists(path) is True:
            valid = True
        else:
            logger.info(f'{path} does not exist')
        return valid

def example():
    """
    Simple example using this class
    """
    icon = CustomImage()
    icon.open_image('ressources/eye_open.png')
    print(icon)

    # pink_color = (255, 0, 0)
    # new_image_data = change_color(data, pink_color)
    #
    # im.putdata(new_image_data)
    # im.show()
    # save_path = r"C:\Users\youss\Desktop\flower_image_altered.jpg"
    # save_image(im, save_path)


example()
