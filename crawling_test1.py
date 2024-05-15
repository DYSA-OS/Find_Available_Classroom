import time
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
    # Wait until the search button is present and click it
    search_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mainframe_childframe_form_divSearch_btnSearch"]'))
    )
    print(f'search_button : {search_button}')
    search_button.click()

    # Wait for the results to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mainframe_childframe_form_grdLessSubjtExcel_body_gridrow_0_cell_0_0GridCellTextContainerElement"]/div'))
    )

    all_elements = []

    for j in range(5):  # Adjust the range as needed for the number of rows
        row_elements = []
        for i in range(25):  # Adjust the range as needed for the number of columns
            xpath = f'//*[@id="mainframe_childframe_form_grdLessSubjtExcel_body_gridrow_{j}_cell_{j}_{i}GridCellTextContainerElement"]/div'

            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                row_elements.append(element.text if element.text.strip() else "(빈칸)")
            except Exception as e:
                print(f'Element at row {j}, column {i} not found: {e}')
                row_elements.append("(에러)")

        all_elements.append(row_elements)

    # Print the elements
    for row_index, row in enumerate(all_elements):
        print(f'Row {row_index}:')
        for col_index, value in enumerate(row):
            print(f'  Column {col_index}: {value}')

except Exception as e:
    print(e)

finally:
    # Close the browser
    driver.quit()
