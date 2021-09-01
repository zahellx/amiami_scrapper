from selenium import webdriver  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from project.database.db_manager import DatabaseManager
import time
from project.database.models import figure
import numpy as np
from project.database.models.figure import Figure
import time

class Scrapper():
    def run(self):
        self.db_manager = DatabaseManager(figure.Figure)
        preowned_figures = self.get_amiami_preowned()
        db_figures = self.db_manager.get_all()

        new_figures = list(set(preowned_figures) - set(db_figures))
        
        self.db_manager.clean_table()
        self.db_manager.insert_multiple(preowned_figures)
        return new_figures


    def get_amiami_preowned(self):
        self.AMIAMI_PREOWNED_URI = 'https://www.amiami.com/eng/search/list/?s_st_condition_flg=1&s_sortkey=preowned&s_cate_tag=1'

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        options.add_argument("--enable-javascript")
        driver = webdriver.Firefox(options=options)
        driver.get(self.AMIAMI_PREOWNED_URI)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

        pages = self.get_num_pages(driver)
        start = time.time()
        all_figures = []
        # pages = 5
        for page in range(1, pages):
            page_figures = self.get_pag_figures(driver, page)
            all_figures.extend(page_figures)
        end = time.time()
        print(end - start)
        driver.close()
        return all_figures

    def get_num_pages(self, driver):
        try:
            pages_cont = driver.find_elements_by_class_name('pager-list')
            pages = pages_cont[0].find_elements_by_tag_name("li")
            last_page = pages[len(pages) - 1].text
            return int(last_page) + 1
        except:
            # print(f'Ha fallado la obtencion del numero de paginas')
            time.sleep(5)
            return self.get_num_pages(driver)

    def get_pag_figures(self, driver, page):
            figures = []
            driver.get(f'{self.AMIAMI_PREOWNED_URI}&pagecnt={page}')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'newly-added-items__item')))
            try: 
                figures_cont = driver.find_elements_by_class_name('newly-added-items__item')
                for figure in figures_cont:
                    img = figure.find_element_by_class_name('newly-added-items__item__image_item').find_element_by_tag_name("img").get_attribute("src")
                    name = figure.find_element_by_class_name('newly-added-items__item__name').text
                    brand = figure.find_element_by_class_name('newly-added-items__item__brand').text
                    url = figure.find_element_by_class_name('newly-added-items__item__nomore').href
                    try:
                        price = figure.find_element_by_class_name('newly-added-items__item__price').text.split(' ')[0]
                    except:
                        price = 0
                    figures.append(Figure(name, img, price, brand, url))
                return figures
            except Exception as error:
                time.sleep(5)
                return self.get_pag_figures(driver, page)
                

    def test(self):
        self.db_manager = DatabaseManager(figure.Figure)
        self.db_manager.run_pruebas_multiple()
        pass

# if __name__ == "__main__":
#     got = Scrapper()
#     got.run()