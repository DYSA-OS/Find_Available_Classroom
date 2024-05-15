from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
url = "http://all.jbnu.ac.kr/jbnu/sugang/sbjt/sbjt.html"
driver.get(url)

try:
    # 결과가 나올때 까지 기다리는데, 일단 10초로 설정
    search_button = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mainframe_childframe_form_divSearch_btnSearch"]'))
    )
    print(f'search_button : {search_button}')
    search_button.click()

    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mainframe_childframe_form_grdLessSubjtExcel_body_gridrow_1_cell_1_24GridCellTextContainerElement"]/div'))
    )
    value = element.text
    print(f'{element} element')
    print(f'{value} value')

except Exception as e:
    print(e)

finally:
    driver.quit()
