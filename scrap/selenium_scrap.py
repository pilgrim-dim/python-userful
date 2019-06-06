# !/usr/bin/env python3
# -*-coding: utf-8-*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from scrap.alert_utils import send_email
import datetime


# set selenium
driver_path = '../driver/geckodriver.exe'
driver_timeout = 15
driver_until = EC.presence_of_element_located((By.CLASS_NAME, 'item'))
driver = webdriver.Firefox(executable_path=driver_path)

# set searching
url_format = 'https://www.librarything.com/search.php' \
             '?search=%s' \
             '&searchtype=newwork_titles' \
             '&sortchoice=0'
max_of_attempt = 3

# set output
work_id_file_path = '../result/work_id_no_isbn.txt'
fw = open(work_id_file_path, 'w', encoding='utf8')

# book search from query list file
book_file_path = '../collection/work_id_no_isbn_not_searched.txt'
with open(book_file_path, 'r', encoding='utf8') as fr:
    for line in fr:
        line = [x.strip() for x in line.split('\t')]
        book_id, book_title, book_isbn, book_author = line[0], line[1], line[2], line[3]
        if book_isbn is '':
            query = book_title
        else:
            query = book_isbn.split(';')[0]
        print('query [%s|%s|%s]' % (book_id, book_title, query))
        url = url_format % query
        attempt, is_not_scraped, librarything_work_id = 1, True, ''
        while is_not_scraped and attempt <= max_of_attempt:
            try:
                driver.get(url)
                element = WebDriverWait(driver=driver, timeout=driver_timeout).until(driver_until)
                for paragraph in driver.find_elements_by_css_selector('p.item'):
                    anchors = paragraph.find_elements_by_tag_name('a')
                    title = anchors[0].text
                    author = anchors[1].text
                    href = anchors[0].get_attribute('href')
                    if book_author.split()[0].replace(',', '').lower() in author.lower():
                        librarything_work_id = href.split('/')[-1].strip()
                        is_not_scraped = False
                        print('>>> searched')
                        fw.write('%s\t%s\t%s\t%s\t%s\n' % (
                        book_id, book_title, book_isbn, book_author, librarything_work_id))
                        fw.flush()
                        break
            except (TimeoutException, NoSuchElementException) as e:
                print('>>> failed [%d|%s]' % (attempt, e.msg))
            except Exception as e:
                print('>>> failed [%d|unhandled exception]' % attempt)
            attempt += 1
fw.close()
driver.quit()

# send email
send_email(
    '[work_id_collect] program has been finished',
    'program has been finished at %s' % (datetime.datetime.now()),
    'alert.by.speechless',
    'password',
    'email@gmail.com',
)

