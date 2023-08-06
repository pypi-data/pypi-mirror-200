import os

import requests
import parsel


def print_hello_world():
    print("Hello, world!")


def create_directory(save_path: str):
    """
    To create the folder to save something.
    :param save_path: The path to save object.
    :return: The save path.
    """
    save_path = save_path
    if not os.path.exists(save_path):
        os.mkdir(save_path)
        print(f"The Path[{save_path}] is creating successful")
        return save_path


def get_page_html(url: str, headers: str):
    """
    To get the page html by requests.
    :param url: The way to get page html.
    :param headers: The demand of page html.
    :return: The source page html.
    """
    response = requests.get(url=url, headers=headers)
    print("The status_code:", response.status_code)
    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        html = response.text
        return html


def parse_html(html: str):
    """
    To parse the require of the result.
    :param html: The page html.
    :return: The Selector object.
    """
    selector = parsel.Selector(html)
    return selector


def get_image_content(save_path: str, image_name: str, image_content):
    """
    The get the image,and save them to the local.
    :param save_path: The position to save the image.
    :param image_name: The name of image.
    :param image_content: The data of image.
    :return: None
    """
    with open(save_path + image_name, mode="wb") as fp:
        fp.write(image_content)
        print(f"The Image[{image_name}] have been saved.")
