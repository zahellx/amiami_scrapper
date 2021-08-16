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
import project.utils.utilidades as utilidades

class Main():
    def run(self):
        self.db_manager = DatabaseManager(figure.Figure)
        df_preowned = self.get_amiami_preowned()

        df_db_figures = self.db_manager.get_all_df()


        preowned = df_preowned.to_numpy()
        db_figures = df_db_figures.to_numpy()


        print('df_preowned - df_db_figures')
        print(utilidades.compare_df(preowned, db_figures))
        
        self.db_manager.clean_table()
        self.db_manager.insert_df(df_preowned)


    def get_amiami_preowned(self):
    self.AMIAMI_PREOWNED_URI = 'https://www.amiami.com/eng/search/list/?s_st_condition_flg=1&s_sortkey=preowned&s_cate_tag=1'

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        options.add_argument("--enable-javascript")
        driver = webdriver.Firefox(options=options)
        driver.get(self.AMIAMI_PREOWNED_URI)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

        columns = ['name', 'image', 'price', 'brand']
        df_figures = pd.DataFrame(columns=columns)
        pages = self.get_num_pages(driver)
        start = time.time()
        for page in range(1, pages):
            driver.get(f'{self.AMIAMI_PREOWNED_URI}&pagecnt={page}')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'newly-added-items__item')))
            # body = driver.execute_script("return document.body")
            try: 
                figures_cont = driver.find_elements_by_class_name('newly-added-items__item')
                for figure in figures_cont:
                    img = figure.find_element_by_class_name('newly-added-items__item__image_item').find_element_by_tag_name("img").get_attribute("src")
                    name = figure.find_element_by_class_name('newly-added-items__item__name').text
                    brand = figure.find_element_by_class_name('newly-added-items__item__brand').text
                    price = figure.find_element_by_class_name('newly-added-items__item__price').text.split(' ')[0]
                    # print(f'{img}')
                    # print(f'{name}')
                    # print(f'{brand}')
                    # print(f'{price}\n')
                    
                    df_figures.loc[-1] = [name, img, price, brand]
                    df_figures.index = df_figures.index + 1
                    df_figures = df_figures.sort_index()
            except:
                print(page)
        print(df_figures.to_markdown())
            
        end = time.time()
        print(end - start)
        driver.close()
        return df_figures

    def get_num_pages(self, driver):
        pages_cont = driver.find_elements_by_class_name('pager-list')
        pages = pages_cont[0].find_elements_by_tag_name("li")
        last_page = pages[len(pages) - 1].text
        return int(last_page)
        # print(last_page)


if __name__ == "__main__":
    got = Main()
    got.run()