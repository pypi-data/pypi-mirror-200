import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class synoChat:
    def __init__(self, username, password,msg_user,msg_text):
        self.username = username
        self.password = password
        self.msg_user = msg_user
        self.msg_text = msg_text

    def url_input(self):
        options = self.webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get("https://chat.infodev.com.np/#/signin")
        # printing title of webpage
        print(self.driver.title)
        # maximize the browser window
        self.driver.maximize_window()


    def login(self):
        self.driver.implicitly_wait(6)
        # searh is the input field for username
        self.search = self.driver.find_element(By.TAG_NAME, "input")
        self.search.send_keys(self.username)
        # RETURN is the enter key
        self.search.send_keys(Keys.RETURN)


        # search is the password field
        self.search = self.driver.find_element("name", "current-password")
        self.search.send_keys(self.password)
        self.search.send_keys(Keys.RETURN)
        # waiting for website to load
        print("Login successful")
        time.sleep(5)
    
    def drive_error(self):
        try:
            button = self.driver.find_element(By.XPATH, '//*[@id="ext-gen852"]').click()

        except:
            print('Button clicked')

    def search_name(self):
        print('inside search')
        self.driver.implicitly_wait(5)
        add_button = self.driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/div[3]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div[4]/div[1]/span/button')
        add_button.click()
        self.driver.implicitly_wait(2)
        print("Search button clicked")


        # finding the person in search
        search_bar = self.driver.find_element(
            By.XPATH, '/html/body/div[8]/div[16]/div[2]/div[2]/div[2]/div[1]/input')
        search_bar.click()
        search_bar.send_keys(f'{self.msg_user}')
        time.sleep(2)
        self.driver.implicitly_wait(10)
        # search.send_keys(Keys.RETURN)
        print("Input name filled")
        time.sleep(2)

        # selecting the person
        person = self.driver.find_element(
            By.XPATH, '/html/body/div[8]/div[16]/div[3]/div/div[1]/div[1]/div/div/div')
        person.click()
        print('Person Selected')

        # selecting the chat button
        chat = self.driver.find_element(
            By.XPATH, '/html/body/div[8]/div[16]/div[3]/div/div[2]/div[2]/span/button')
        chat.click()
        print('Chat button Pressed')
        time.sleep(1)

    def send_msg(self):
        # message is the message box
        time.sleep(2)
        message = self.driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/div[3]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div/div[2]/div[1]/div[1]')
        # message.click()
        message.send_keys(f'{self.msg_text}')
        message.send_keys(Keys.RETURN)
        print('Message send successfully')

    def login_only(self):
        self.url_input()
        self.login()

    def synoMsg(self):
        self.url_input()
        self.login()
        self.drive_error()
        self.search_name()
        self.send_msg()

