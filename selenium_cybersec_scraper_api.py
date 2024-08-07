from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def create_webdriver():
    return webdriver.Firefox()

def get_exd_detail(url, driver):
    data = dict()
    driver.get(url)

    try:
        # 電話
        telephone_element = driver.find_element(By.CLASS_NAME, 'info-tel')
        data['telephone'] = telephone_element.text
    except NoSuchElementException:
        print(f"URL: {url}, has no telephone")

    try:
        # EMAIL
        email_element = driver.find_element(By.CLASS_NAME, 'info-mail')
        data['email'] = email_element.text
    except NoSuchElementException:
        print(f"URL: {url}, has no email")

    try:
        # Description
        desc_element = driver.find_element(By.CLASS_NAME, 'ex-foreword')
        data['description'] = desc_element.text
    except NoSuchElementException:
        print(f"URL: {url}, has no Description")


    # Website
    website_elements = driver.find_elements(By.CLASS_NAME, 'border-icon')
    for website_element in website_elements:
        # 利用 element.get_attribute("屬性名稱") 取得資訊
        href = website_element.get_attribute('href')
        if href:
            for social_media_name in ['facebook', 'twitter', 'linkedin', 'instagram']:
                if social_media_name in href:
                    data[social_media_name] = href
            else:
                data['website'] = href

    return data

if __name__ == '__main__':
    test_driver = create_webdriver()
    exd_url = "https://cybersec.ithome.com.tw/2024/exhibition-page/2043"
    exd_data = get_exd_detail(
        url=exd_url,
        driver=test_driver
    )
    print(exd_data)
    test_driver.close()