import requests
from time import sleep
from tqdm import tqdm
from PIL import Image
import os
import shutil
from urllib.request import urlopen
from bs4 import BeautifulSoup


class RFBRBooksDownloader:
    def __init__(self, **kwargs):
        self.__initial_url = kwargs['book_url']

        self.__output_pdf_name = kwargs.get('output_pdf_name', 'book')
        self.__delete_temporary_images = kwargs.get('delete_temporary_images', True)
        self.__requests_pause = kwargs.get('requests_pause', 0.1)

        self.__work_url = self.__get_work_url_from_initial_url()
        self.__res_dir = '/'.join([os.getcwd(), self.__output_pdf_name])
        self.__ext = self.__work_url.split('.')[-1]

    def __create_res_dir(self):
        if os.path.exists(self.__res_dir):
            shutil.rmtree(self.__res_dir)
            sleep(1.0)
        os.mkdir(self.__res_dir)

    def __get_work_url_from_initial_url(self):
        object_id = self.__initial_url.split('o_')[1].split('#')[0]
        return 'http://www.rfbr.ru/rffi/djvu_page?objectId=' + object_id + '&width=1000&page=0&cache=cache.png'

    def __get_max_page(self):
        soup = BeautifulSoup(str(urlopen(self.__initial_url).read()), 'lxml')
        return int(soup.get_text().split('readerInitialization(')[1].split(',')[0])

    @staticmethod
    def __generate_url_for_current_page(url, page, split_word='page='):
        url_list = url.split(split_word)
        return url_list[0] + split_word + str(page) + url_list[1][1:]

    def __save_images_to_pdf(self, images):
        pil_images = []
        for image in images:
            pil_images.append(Image.open(image))
        try:
            pil_images[0].save('/'.join([self.__res_dir,  self.__output_pdf_name + '.pdf']), 'PDF', resolution=100.0,
                               save_all=True, append_images=pil_images[1:])
        except:
            raise Exception('Exception in function save_images_to_pdf.')
        print('pdf-document successfully saved!')

    @staticmethod
    def __delete_images(images):
        try:
            for image in images:
                os.remove(image)
        except:
            raise Exception('Exception in function delete_images.')
        print('cache successfully deleted!')

    def process(self):
        try:
            self.__create_res_dir()
        except:
            raise Exception('Exception when creating res_dir.')
        print('res_dir successfully created!')

        images = []
        for page in tqdm(range(self.__get_max_page() + 1), desc='downloading'):
            current_url = self.__generate_url_for_current_page(self.__work_url, page)
            image_name = self.__res_dir + '/%04d.' % page + self.__ext
            images.append(image_name)
            with open(image_name, 'wb') as f:
                content = requests.get(current_url).content
                f.write(content)
            sleep(self.__requests_pause)

        self.__save_images_to_pdf(images)

        if self.__delete_temporary_images:
            self.__delete_images(images)

        print('done!')
