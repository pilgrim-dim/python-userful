# !/usr/bin/env python3
# -*-coding: utf-8-*-

import requests
from bs4 import BeautifulSoup
import re
import datetime
from .alert_utils import send_email


# set http request
url = 'https://www.librarything.com/ajaxinc_showbooktags.php'
params = {'all': '1', 'doit': '1', 'print': '1'}
max_of_attempt = 3

# set output
tag_file_path = '../collection/tag_no_isbn_1_0317.txt'
fw = open(tag_file_path, 'w', encoding='utf8')

# extract tags from librarything_work_id
work_id_file_path = '../collection/work_id_no_isbn_total.txt'
with open(work_id_file_path, 'r', encoding='utf8') as fr:
    for line in fr:
        line = [x.strip() for x in line.split('\t')]
        if len(line) < 3:
            continue
        book_id, book_title, librarything_work_id = line[0], line[1], line[2]
        params['work'] = librarything_work_id
        attempt, is_not_scraped = 1, True
        print('request [%s|%s]' % (book_id, librarything_work_id))
        while is_not_scraped and attempt <= max_of_attempt:
            try:
                respond = requests.post(url, params=params)
                html = respond.text
                soup = BeautifulSoup(html, 'html.parser')
                for span in soup('span', {'class': 'tag'}):
                    tag_name = span.a.string
                    if tag_name is not None:
                        tag_name = tag_name.strip()
                        tag_count = int(re.findall('\d+', span.span.string.strip())[0])
                        fw.write('%s\t%s\t%s\t%s\t%s\n' % (book_id, book_title, librarything_work_id, tag_name, tag_count))
                fw.flush()
                is_not_scraped = False
                print('>>> get tags')
            except requests.exceptions.RequestException as e:
                print('>>> fail [%d|%s]' % (attempt, e))
            except Exception as e:
                print('>>> failed [%d|unhandled exception]' % attempt)
            attempt += 1
fw.close()

# send email
send_email(
    '[tag_id_collect] program has been finished',
    'program has been finished at %s' % (datetime.datetime.now()),
    'alert.by.speechless',
    '!skrmsptjdwjs9003',
    'hellossong@gmail.com',
)
