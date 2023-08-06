import undetected_chromedriver as uc
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

class libgpt:

    def __init__(self, chromedriver=None, chromepath=None):
        self.chrome_options = uc.ChromeOptions()
        self.chrome_options.add_argument("--headless")
        if chromedriver and chromepath:
            self.driver = uc.Chrome(options=self.chrome_options, executable_path=chromedriver, chrome_path=chromepath)
        elif chromedriver:
            self.driver = uc.Chrome(options=self.chrome_options, executable_path=chromedriver)
        elif chromepath:
            self.driver = uc.Chrome(options=self.chrome_options, chrome_path=chromepath)
        else:
            self.driver = uc.Chrome(options=self.chrome_options)

    def chat(self, request):
        f"""
        This function uses Chrome browser and freegpt.one for free ChatGPT api.
        No pay needed, no account. Only internet, basic coding skills and your imagination
        Parameters:
            :request (str) - your request
        Returns:
            :result (str) - the response from the ChatGPT
        Features:
            \n works like new string
            absolutely free
        Warings:
            May be buggy asf
            Not working on colaboratory
            Doesn't save your chat history
        """
        self.driver.get("https://freegpt.one/")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(("xpath", "//textarea[@class='w-full resize-none focus:ring-0 focus-visible:ring-0 p-0 pr-7 m-0 border-0 bg-transparent dark:bg-transparent']")))
        text = request + "\nAt the end of your answer write ':::::end::::::'"
        e = text.split("\n")
        e = [x for x in e if x != '']
        text = text.replace("\n", (Keys.SHIFT +  Keys.ENTER));
        search_box = self.driver.find_element("xpath", "//textarea[@class='w-full resize-none focus:ring-0 focus-visible:ring-0 p-0 pr-7 m-0 border-0 bg-transparent dark:bg-transparent']")
        for i in range(0, len(e)):
            if i != len(e)-1:
                search_box.send_keys(e[i])
                search_box.send_keys(Keys.SHIFT +  Keys.ENTER)
            elif i == len(e)-1:
                search_box.send_keys(e[i])
                search_box.send_keys(Keys.ENTER)
        time.sleep(10)
        element = self.driver.find_element("xpath", "(//div[@class='w-full border-b border-black/10 dark:border-gray-900/50 text-gray-800 dark:text-gray-100 group bg-gray-50 dark:bg-[#444654]'])[last()]")
        while True:
            result = element.text
            if len(result) == 0:
                self.driver.close()
                return None
                break;
            if ":::::end::::::" in result:
                break;
        self.driver.close()
        result = result.replace(":::::end::::::", "")
        result = result.replace("Copy code", "")
        return result
