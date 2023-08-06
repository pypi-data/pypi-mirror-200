import asyncio
import unittest
from src.util_hj3415 import noti


class UtilsTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mail(self):
        noti.mail_to('util_hj3415', 'test')

    def test_telegram(self):
        import os
        noti.telegram_to(botname='manager',
                         text=f'>>> python {os.path.basename(os.path.realpath(__file__))} test')
        for name in ['manager', 'dart', 'eval', 'cybos']:
            noti.telegram_to(botname=name, text='test')