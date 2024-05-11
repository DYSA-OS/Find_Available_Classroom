from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 드라이버 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 웹사이트 열기
driver.get('http://all.jbnu.ac.kr/jbnu/sugang/sbjt/sbjt.html')

# 페이지가 완전히 로드될 때까지 기다리기 (필요에 따라 대기 시간 조정)
driver.implicitly_wait(10)

# 버튼 찾기 (ID를 사용하는 예제)
button = driver.find_element(By.ID, "mainframe_childframe_form_divSearch_btnSearchTextBoxElement")

# 버튼 클릭
button.click()

# XPath를 사용하여 요소 찾기
element = driver.find_element(By.XPATH, '//*[@id="mainframe_childframe_form_grdLessSubjtExcel_body_gridrow_0_cell_0_0GridCellTextContainerElement"]/div')
# 요소의 텍스트 가져오기
text = element.text
print(text)

# 드라이버 종료
driver.quit()
