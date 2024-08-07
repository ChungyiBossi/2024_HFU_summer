from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
url = "https://www.apple.com/tw/store?afid=p238%7CsbXAMjDsL-dc_mtid_18707vxu38484_pcrid_698838307185_pgrid_12618487502_pntwk_g_pchan__pexid__&cid=aos-tw-kwgo-brand--slid---product-"
driver.get(url)

search_element  = driver.find_element(By.ID, "globalnav-menubutton-link-search")
search_element.click()

search_input_element = driver.find_element(By.CLASS_NAME, "globalnav-searchfield-input")
search_input_element.send_keys("IPhone 16")
search_input_element.send_keys(Keys.RETURN)


time.sleep(15)

driver.close()