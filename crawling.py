import time
import csv
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

# Maximize the browser window
driver.maximize_window()

def click_scroll_button(times):
    for _ in range(times):
        try:
            scroll_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mainframe_childframe_form_grdLessSubjtExcel_vscrollbar_incbutton"]'))
            )
            scroll_button.click()
            time.sleep(1)  # 스크롤 후 잠시 대기
        except Exception as e:
            print(f'Scroll button click failed: {e}')
            return False
    return True

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
    info = [6, 10, 20, 21, 22]  # 필요한 정보
    previous_first_row = None  # 이전 첫 번째 행 데이터를 저장할 변수

    while True:
        for j in range(24):  # j는 0부터 23까지 반복
            row_elements = []
            row_found = False

            for i in info:  # 필요한 컬럼들
                xpath = f'//*[@id="mainframe_childframe_form_grdLessSubjtExcel_body_gridrow_{j}_cell_{j}_{i}GridCellTextContainerElement"]/div'
                element = None

                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    row_found = True
                    row_elements.append(element.text if element.text.strip() else "(빈칸)")
                except Exception as e:
                    print(f'Element at row {j}, column {i} not found: {e}')
                    row_elements.append("(에러)")

            if row_found:
                # 중복 데이터 확인: 이전 첫 번째 행과 현재 첫 번째 행이 같으면 스킵
                if previous_first_row == row_elements:
                    print(f'Duplicate row found at {j}, skipping...')
                    continue

                all_elements.append(row_elements)
                previous_first_row = row_elements  # 이전 첫 번째 행 데이터를 업데이트

        # 아래 버튼 24번 클릭 시도
        if not click_scroll_button(24):
            print('No more data, scroll button is not clickable')
            break

    # 출력해서 확인
    for row_index, row in enumerate(all_elements):
        print(f'Row {row_index}:')
        for col_index, value in enumerate(row):
            print(f'  Column {col_index}: {value}')

    # CSV 파일로 저장
    csv_file = "output.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["subject", "professor", "lecture_type", "time", "room"])  # 헤더 추가
        writer.writerows(all_elements)
    print(f"Data saved to {csv_file}")

except Exception as e:
    print(e)

finally:
    # Close the browser
    driver.quit()
