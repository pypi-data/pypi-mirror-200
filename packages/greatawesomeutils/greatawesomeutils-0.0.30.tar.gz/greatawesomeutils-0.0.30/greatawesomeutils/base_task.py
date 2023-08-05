import math
from greatawesomeutils.config import IS_DOCKER
from greatawesomeutils.config import RETRY_ATTEMPTS_HIGH
from greatawesomeutils.enums import *
from greatawesomeutils.errors import NETWORK_ERRORS
from greatawesomeutils.lang import country_code_to_time_zone, datetime_to_str, exit_with_failed_status, get_boolean_variable, get_time_in_utc, utc_to_timezoned_datetime, sleep_forever
from greatawesomeutils.lang import exit_with_failed_status, sleep_for_n_seconds
from greatawesomeutils.lang import retry_if_is_error, wait_for_enter
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep
import json
import multiprocessing
import os
import os
import random
import requests
import signal
import time
import traceback
from .config import MASTER_API_URL
from .ip_utils import wait_till_ip_change
from .selenium import get_element_or_none, get_element_or_none_by_selector
from .selenium import get_element_or_none, get_element_or_none_by_selector
from .selenium import save_screenshot
from .selenium import save_screenshot
from .selenium import SAVE_SCREENSHOT_ERROR_FOLDER, SAVE_SCREENSHOT_SUCCESS_FOLDER
from .selenium import SAVE_SCREENSHOT_ERROR_FOLDER, SAVE_SCREENSHOT_SUCCESS_FOLDER, save_html_logs
from .selenium_driver import RANDOM, delete_cache
from .selenium_driver import delete_corrupted_files
from .selenium_driver import GOOGLE_DRIVER, UNDETECTED_DRIVER, create_driver_by_driver_type, delete_profile_path, MyChrome

exiting = False


def is_exiting():
    return exiting


def set_is_exiting():
    global exiting
    exiting = True




def execute_after_n_seconds(f, s):
    time.sleep(s)
    f()


class BotCaughtException(Exception):
    pass


PXM_ERROR_MSG = 'Bot has been caught by PerimeterX'


def is_bot_caught(driver):

    pmx = get_element_or_none(
        driver, "//*[text()='Please verify you are a human']")
    if pmx is not None:
        return True, PXM_ERROR_MSG

    clf = get_element_or_none_by_selector(driver, "#challenge-running")
    if clf is not None:
        return True, 'Bot has been caught by Cloudflare'

    return False, None


class EmailAlreadyExists(Exception):
    pass


class RetryException(Exception):
    pass


class RerunException(Exception):
    def __init__(self, after = None ):
      self.after = after


NULL = "NULL"


class BaseTask():
    sys_exit_on_crash = True
    def __init__(self, user = None):
        self.data = json.loads(os.environ.get('data')) if os.environ.get('data') is not None else {} 
        self.user = user if user is not None else json.loads(os.environ.get('user')) if os.environ.get('user') is not None else {}
        
        self.task_type = os.environ.get('task_type')
        self.MODULE_NAME = os.environ.get('MODULE_NAME', '')

        self.task_id = os.environ.get('task_id')
        self.SKIP_IP_CHECK = get_boolean_variable('SKIP_IP_CHECK') if os.environ.get('SKIP_IP_CHECK') is not None else True
        
        self.is_debug = not IS_DOCKER

        self.MASTER_API = MASTER_API_URL


    def ask_master_to_restart(self):
        data = [{
            "when": self.get_current_time_in_users_time_zone(),
            "data": {
                "task_id": self.task_id
            }
        }]

        r = requests.post(f"{self.MASTER_API}/tasks/restart/",
                        json=data)
        r.raise_for_status()
        # Wait For Process to be restarted by Master
        sleep_forever()


    def run(self, driver: MyChrome, data, user):
        pass
    
    def sign_up_success(self):
        r = requests.post(f"{self.MASTER_API}/tasks/sign-up-success/",
                          json={'task_id': self.task_id})
        r.raise_for_status()
        return True

    def save_failure_screenshot(student):
        save_screenshot(student.driver, self.user["user_id"],
                        SAVE_SCREENSHOT_SUCCESS_FOLDER, 'success')

    def assert_bot_has_not_been_caught(self):
        is_caught, message, = is_bot_caught(self.driver)

        if is_caught:
            raise BotCaughtException(message)

    def register_ip_for_task(self, ip):
        r = requests.post(f"{self.MASTER_API}/tasks/register-ip/",
                          json={'ip': ip, 'task_id': self.task_id})

        if r.status_code == 400:
            print('Ip already registered')
            return False

        r.raise_for_status()
        print('Registered Ip!')

        return True
    is_eager = False
    start_link = None
    
    register_ip = True

    def save_success_screenshot(self):
            save_screenshot(self.driver , self.user["user_id"],
                                SAVE_SCREENSHOT_SUCCESS_FOLDER, 'success')

    def begin_task(self):
            # Always use undetected in docker
        if IS_DOCKER:
            self.DRIVER_TYPE = UNDETECTED_DRIVER
        if self.SKIP_IP_CHECK:
            print(f'Skipping IP Check')
        else:
            ip = wait_till_ip_change()
            
            if self.register_ip:
                is_success = self.register_ip_for_task(ip)
                
                if not is_success:
                    self.ask_master_to_restart()
                # Skip IP check next time
            self.SKIP_IP_CHECK = True

        if not self.has_user_id():
            self.user["user_id"] = NULL

        is_sign_up_task = 'sign_up' in self.MODULE_NAME.lower()

        self.user = self.user
        self.data = self.data

        data = self.data
        user = self.user

        def do_run():
            driver = self.create_driver(self.is_eager)
            self.driver = driver
            try:
                if self.start_link is not None:
                    print('Organically getting ', self.start_link)
                    driver.organic_get(self.start_link)

                self.run(driver, data, user)
                self.save_success_screenshot()
                
                if is_sign_up_task:
                    self.sign_up_success()

                self.close(driver)
                print('Bot ran succesfully')

            except Exception as error:
                isReRun = isinstance(error, RerunException)
                
                def print_driver_url():
                    try:
                        driver_url = f'Driver Url: {driver.current_url}\n'
                        print(driver_url)
                    except:
                        pass

                if not isReRun:
                    traceback.print_exc()
                    print(error)
                
                if self.is_debug:
                    wait_for_enter('Waiting to Close')

                if not isReRun:
                    print_driver_url()
                    
                    save_screenshot(driver, user.get( "user_id", 'NULL'),
                                    SAVE_SCREENSHOT_ERROR_FOLDER, 'error')
                                    
                    save_html_logs(driver, user.get( "user_id", 'NULL'))

                self.close(driver)

                if isinstance(error, BotCaughtException):
                    print('Deletig Profile')
                    if user.get( "user_id") is not None:
                        delete_profile_path(self.user["user_id"])
                    self.ask_master_to_restart()
                elif isinstance(error, EmailAlreadyExists):
                    print('Deletig Profile')
                    if user.get( "user_id") is not None:
                        delete_profile_path(self.user["user_id"])
                    self.change_email()
                    self.ask_master_to_restart()

                if isinstance(error, RetryException):
                    self.ask_master_to_restart()
                if isReRun:
                    if self.retries < self.max_retries:
                        self.retries+=1
                        if error.after is not None:
                            sleep_for_n_seconds(error.after)

                        print('Bot is ReRunning')
                        do_run()
                    
                else:
                    if self.sys_exit_on_crash:
                        exit_with_failed_status()
        do_run()

    retries = 0
    max_retries = math.inf  
    
    def change_email(self):
        r = requests.patch(f"{self.MASTER_API}/tasks/change-email/",
                           json={'task_id': self.task_id})
        r.raise_for_status()
        return True

    DRIVER_TYPE = GOOGLE_DRIVER


    def has_user_id(self):
        return  self.user.get("user_id") != NULL and self.user.get("user_id") is not None
    FORCE_VERSION = None

    def create_driver(self, is_eager):

        def do_create_driver():
            def run():

                driver_type = self.DRIVER_TYPE
                return create_driver_by_driver_type(
                    driver_type,
                    self.user.get("user_id") if self.has_user_id() else None,
                    self.user.get("window_size", RANDOM),
                    self.user.get("user_agent", RANDOM),
                    is_eager,
                    self.FORCE_VERSION)

            driver = retry_if_is_error(
                run, NETWORK_ERRORS + [(WebDriverException, lambda: delete_corrupted_files(self.user["user_id"]) if self.has_user_id() else None )], RETRY_ATTEMPTS_HIGH)

            def call_quit(signalNumber, frame):
                if is_exiting():
                    print('Already Exiting')
                    return

                set_is_exiting()

                print('Force Exit Detected. Exiting Gracefully')
                try:
                    self.close(driver)
                except Exception:
                    print('Someting went wrong closing Driver')
                finally:
                    sleep_for_n_seconds(2)
                    exit_with_failed_status()

            signal.signal(signal.SIGINT, call_quit)
            signal.signal(signal.SIGTERM, call_quit)
            return driver

        # Basically ask master to restart if failed to start after 10 minutes
        thread = multiprocessing.Process(
            target=execute_after_n_seconds, args=(self.ask_master_to_restart, 600))
        thread.start()
        driver = do_create_driver()
        thread.terminate()
        return driver

    def close(self, driver):
        delete_cache(driver)

        print("Closing Driver")
        driver.close()
        print("Closed Driver")
        # Sleep Time Needed for Chrome User Profiles To Be Saved Properly
        sleep(2)

    def get_current_time_in_users_time_zone():
        result = datetime_to_str(utc_to_timezoned_datetime(
            get_time_in_utc(), country_code_to_time_zone(self.user["country_code"])))

        return result



def sleep_for_word_length_type(s):

    def count_words(s):
        return len(s.split(' '))

    word_len = count_words(s)

    if word_len == 1:
        sleep_for_n_seconds(random.randint(4, 7))
    else:
        start = 5 + word_len
        end = 5 + word_len * 2
        print(start, end)
        sleep_for_n_seconds(random.randint(int(start), int(end)))
