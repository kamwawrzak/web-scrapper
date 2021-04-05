from asyncio import gather, Semaphore, wait_for
from aiohttp import ClientSession
import aiofiles
from bs4 import BeautifulSoup

from datetime import datetime

import requests


MAX_TASKS = 10
MAX_TIME = 2
IGNORE_TAGS = ['html', 'script', 'head', 'meta', 'input', 'title']


def get_page_content(page_url):
    """
    :param page_url: url address of desired page
    :return: BeutifulSoup object including page content
    """
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def extract_text(page_content):
    """
    :param page_content: page content received from get_page_content() function
    :return: string of comma separated texts present on the page
    """
    text = ''
    texts = page_content.find_all(text=True)
    for t in texts:
        if t != '\n' and t.parent.name not in IGNORE_TAGS:
            text += f'{t},'
    return text


def extract_images(page_content, base_url):
    """
    :param page_content: page_content: page content received from get_page_content() function
    :param base_url: base url address of the page
    :return: list of image url addresses
    """
    images = page_content.find_all('img')
    img_links = [img['src'] for img in images]
    for link in img_links:
        if link[3:] != 'http':
            img_links[img_links.index(link)] = base_url + link
    return img_links


def save_text(page_text, path='./results/texts/'):
    """
    :param page_text: string including text on the page
    :param path: optionally desired path where the file should be saved
    :return:
    """
    timestamp = str(datetime.now().timestamp()).replace('.', '_')
    filename = f'{path}{timestamp}.csv'
    with open(filename, 'wb+') as file:
        file.write(page_text)


async def save_images(images_list, path='./results/images/'):
    """
    :param images_list: list of image url addresses
    :param path: optionally desired path where the file should be saved
    :return:
    """
    tasks = []
    sem = Semaphore(MAX_TASKS)
    async with ClientSession() as session:
        for img_url in images_list:
            img_name = path + str(datetime.now().timestamp()).replace('.', '_') + '.jpeg'
            task = wait_for(download_img(img_url, sem, session, img_name), timeout=MAX_TIME)
            tasks.append(task)
        await gather(*tasks)


async def download_img(img_url, semaphore, session, download_path):
    """
    :param img_url: url address of single image
    :param semaphore: semaphore limiting amount of concurrent threads
    :param session: aiohttp session
    :param download_path: path where the image should be saved
    :return:
    """
    async with semaphore:
        async with session.get(img_url) as response:
            image = await response.read()
        if response.status == 200:
            async with aiofiles.open(download_path, 'wb+') as file:
                await file.write(image)
        else:
            raise Exception('Something went wrong.')
