from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import time
import langdetect
from collections import Counter


def test_lang():
    url = "https://coinmarketcap.com/"
    chrome_options = Options()
    chrome_driver = "chromedriver.exe"
    os.chmod(chrome_driver, 755)
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
    
    browser.get(url)
    i = 0
    d = []

    while True:
        print("sleep")
        time.sleep(4)
        print("click bar")
        browser.find_element_by_class_name("sc-10o4ja6-0").click()
        print("find languages")
        languages = browser.find_elements_by_class_name("bcehcf")[-1].find_elements_by_class_name("iwCxTx")
        if i == len(languages):
            break
        _text = languages[i].text
        print("click on language")
        languages[i].click()
        time.sleep(4)
        print("find text")
        texts = []
        texts.append(browser.find_element_by_class_name("Heading-sc-1q9q90x-0").text)

        texts += [x.text for x in browser.find_element_by_class_name("dOnegn").find_elements_by_class_name("dzHJPm")]
        texts += [x.text for x in browser.find_element_by_class_name("cmc-table").find_elements_by_class_name("stickyTop")]
        print("detect language")
        langs = []
        for text in texts:
            try:
                langs.append(langdetect.detect(text))
            except:
                continue
        c = Counter(langs)
        d.append({"name": _text, "counter": dict(c)})
        print({"name": _text, "counter": c})

        i += 1

    assert all([x['name'].split(' ')[-1].lower() == x['counter'].most_common(1)[0][0] for x in d]), f"Didn't match: {[x for x in d if x['name'].split(' ')[-1].lower() != x['counter'].most_common(1)[0][0] ]}\n "
    
    return d