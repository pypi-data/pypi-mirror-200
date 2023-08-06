import os

from django.test import TestCase

# from netdoc import models, utils

TEST_DIRECTORY= os.path.dirname(os.path.realpath(__file__))

class QuestionModelTests(TestCase):
    def setUp(self):
        # Load data
        # utils.import_log(TEST_DIRECTORY)

        print(TEST_DIRECTORY) # /home/andrea/src/netdoc/netdoc/tests/netmiko_cisco_ios/lab1

    def test_test(self):
        self.assertIs(False, False)
