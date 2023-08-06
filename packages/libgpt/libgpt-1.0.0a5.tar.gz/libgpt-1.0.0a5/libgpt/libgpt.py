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

def ChatGPT(request, chromedriver=None, chromepath=None):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    if chromedriver and chromepath:
        driver = uc.Chrome(options=chrome_options, executable_path=chromedriver, chrome_path=chromepath)
    elif chromedriver:
        driver = uc.Chrome(options=chrome_options, executable_path=chromedriver)
    elif chromepath:
        driver = uc.Chrome(options=chrome_options, chrome_path=chromepath)
    else:
        driver = uc.Chrome(options=chrome_options)

    driver.get("https://freegpt.one/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", "//textarea[@class='w-full resize-none focus:ring-0 focus-visible:ring-0 p-0 pr-7 m-0 border-0 bg-transparent dark:bg-transparent']")))
    text = "You have been given a question. Answer the question in the language of the question. Nothing extra. At the end of your answer you need to write ':::::end::::::', even if you didn't answer the question.\n" +  request
    e = text.split("\n")
    e = [x for x in e if x != '']
    text = text.replace("\n", (Keys.SHIFT +  Keys.ENTER));
    search_box = driver.find_element("xpath", "//textarea[@class='w-full resize-none focus:ring-0 focus-visible:ring-0 p-0 pr-7 m-0 border-0 bg-transparent dark:bg-transparent']")
    for i in range(0, len(e)):
        if i != len(e)-1:
            search_box.send_keys(e[i])
            search_box.send_keys(Keys.SHIFT +  Keys.ENTER)
        elif i == len(e)-1:
            search_box.send_keys(e[i])
            search_box.send_keys(Keys.ENTER)
    time.sleep(10)
    element = driver.find_element("xpath", "(//div[@class='w-full border-b border-black/10 dark:border-gray-900/50 text-gray-800 dark:text-gray-100 group bg-gray-50 dark:bg-[#444654]'])[last()]")
    while True:
        result = element.text
        if len(result) == 0:
            driver.close()
            return None
            break;
        if ":::::end::::::" in result:
            break;
    driver.close()
    result = result.replace(":::::end::::::", "")
    result = result.replace("Copy code", "")
    return result
