import unittest
import os
import subprocess
import time
import shutil

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


class TestCreateSession(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        # TODO need to pkill python somehow =(
        #  proc.terminate is not enough
        os.remove('/tmp/test.db')

    def test_create_note(self):
        # GIVEN
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, executable_path='/tmp/geckodriver_dir/geckodriver')
        my_env = os.environ.copy()
        my_env['DB_CONNECTION_STRING'] = 'sqlite:////tmp//test.db'
        proc = subprocess.Popen("python -m share_my_notes_app", env=my_env, shell=True)
        time.sleep(1)

        # WHEN
        driver.get("http://127.0.0.1:5000/")
        assert "Share My Notes" in driver.title
        elem = driver.find_element_by_id("new-session-btn")
        elem.click()
        time.sleep(1)
        input_session_name_elem = driver.find_element_by_id("input-session-name")
        input_session_pwd_elem = driver.find_element_by_id("input-session-password")
        input_session_name_elem.send_keys("testsession1")
        input_session_pwd_elem.send_keys("mypwd")
        elem = driver.find_element_by_id("modal-ok-btn")
        elem.click()
        time.sleep(2)

        # THEN
        elem = driver.find_element_by_id("session1")
        elem = driver.find_element_by_class_name("note-title-label")
        time.sleep(2)

        # cleanup
        driver.close()
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    unittest.main()
