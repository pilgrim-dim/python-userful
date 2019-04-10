# !/usr/bin/python3
# -*-coding: utf-8-*-

import smtplib
import datetime


def send_email(subject, text, from_address, password, to_address):
    """
    구글 계정으로 이메일 보내기. (구글 계정의 보안 설정이 '보안 수준이 낮은 앱 허용'으로 설정되어 있어야 함)
    :param subject:이메일 제목
    :param text:내용
    :param from_address:보내는 이메일 주소
    :param password:로그인 비밀번호
    :param to_address:받는 이메일 주소
    :return:
    """
    msg = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (from_address, to_address, subject, text)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(user=from_address, password=password)
    server.sendmail(from_addr=from_address, to_addrs=to_address, msg=msg)
    server.close()


'''
send_email(
    '[work_id_collect] program has been finished',
    'program has been finished at %s' % (datetime.datetime.now()),
    'alert.by.speechless',
    '!skrmsptjdwjs9003',
    'hellossong@gmail.com',
)
'''
