from .models import BusInfo
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
import warnings
warnings.filterwarnings('ignore')

'''
    이 함수는 특정 웹사이트에서 버스 정보를 크롤링하여 저장하는 기능을 수행합니다.
    
    매개변수:
    - request: Django의 HTTP 요청 객체. 이 예제에서는 사용되지 않습니다.
    
    크롤링 프로세스:
    1. Selenium의 Chrome WebDriver를 사용하여 헤드리스 모드로 크롬 브라우저를 실행합니다.
    2. 대상 웹사이트로 이동합니다.
    3. 필요한 정보(출발지, 도착지, 시간 등)를 선택하거나 입력하여 검색합니다.
    4. 검색 결과 페이지에서 필요한 버스 정보(시간, 회사, 등급, 요금 등)를 추출합니다.
    5. 추출된 정보를 리스트에 저장합니다.
    
    예외 처리:
    - NoSuchElementException: 웹 페이지에서 특정 요소를 찾을 수 없는 경우, 크롤링 프로세스를 중단합니다.
    
    결과:
    - bus_info_list: 크롤링한 버스 정보를 담은 리스트. 각 항목은 시간, 회사, 등급, 성인 요금, 어린이 요금, 학생 요금, 남은 좌석 정보를 포함합니다.
    
    참고: 
    - 크롤링 결과가 너무 빈약해서 OpenAPI를 사용하여 데이터를 가져오게 되었다.
'''

def crawl_and_save_bus_info(request):
    # 크롤링한 정보 담을 리스트
    bus_info_list = []

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    da = Alert(driver)

    url = 'https://txbus.t-money.co.kr/otck/trmlInfEnty.do'
    driver.get(url)

    # 크롤링 코드 (동일)
    driver.find_element(By.XPATH, '//*[@id="deprArea"]').click()
    sleep(0.3)
    driver.find_element(By.XPATH, '//*[@id="special_areaList01"]/li[3]/a').click()
    sleep(0.3)
    driver.find_element(By.XPATH, '//*[@id="arvlArea"]').click()
    sleep(0.3)
    driver.find_element(By.XPATH, '//*[@id="areaList02"]/li[10]/a').click()
    sleep(0.3)
    da.accept()
    sleep(0.3)
    da.accept()
    sleep(0.3)
    driver.find_element(By.XPATH, '//*[@id="onewayInfo"]/div/p[2]/a').click()
    sleep(0.3)
    da.accept()
    sleep(0.2)

    for i in range(1, 10, 2):
        try:
            timeUrl = driver.find_element(By.XPATH,
                                          '//*[@id="contents"]/div[2]/div/div[3]/div/div[4]/table/tbody/tr[' + str(
                                              i) + ']/td[1]/div')
            compUrl = driver.find_element(By.XPATH,
                                          '//*[@id="contents"]/div[2]/div/div[3]/div/div[4]/table/tbody/tr[' + str(
                                              i) + ']/td[2]/div/a/strong')

            gradeUrl = driver.find_element(By.XPATH,
                                           '//*[@id="contents"]/div[2]/div/div[3]/div/div[4]/table/tbody/tr[' + str(
                                               i) + ']/td[3]/div').text
            adultfeeUrl = driver.find_element(By.XPATH,
                                              '//*[@id="contents"]/div[2]/div/div[3]/div/div[4]/table/tbody/tr[' + str(
                                                  i) + ']/td[4]/div').text
            childfeeUrl = driver.find_element(By.XPATH,
                                              '//*[@id="contents"]/div[2]/div/div[3]/div/div[4]/table/tbody/tr[' + str(
                                                  i) + ']/td[5]/div').text
            studentfeeUrl = driver.find_element(By.XPATH,
                                                '//*[@id="contents"]/div[2]/div/div[3]/div/div[4]/table/tbody/tr[' + str(
                                                    i) + ']/td[6]/div').text
            try:
                leftUrl = driver.find_element(By.XPATH,
                                              '//*[@id="contents"]/div[2]/div/div[3]/div/div[4]/table/tbody/tr[' + str(
                                                  i) + ']/td[7]/div/a/strong').text
            except NoSuchElementException:
                leftUrl = '0석/ 00석'

        except NoSuchElementException:
            break

        time = timeUrl.text
        company = compUrl.text
        grade = gradeUrl
        adultfee = adultfeeUrl
        childfee = childfeeUrl
        studentfee = studentfeeUrl
        left = leftUrl[:-6]

        temp = [time, company, grade, adultfee, childfee, studentfee, left]
        print(temp)
        bus_info_list.append(temp)

    print(bus_info_list)