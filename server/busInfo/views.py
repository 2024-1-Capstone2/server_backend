from django.shortcuts import render

from django.http import HttpResponse
from .models import BusInfo
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
import warnings
from django.templatetags.static import static
warnings.filterwarnings('ignore')

# Create your views here.
def index(request):
    return HttpResponse("장고 시작")

def bus_info_image(request):
    return render(request, 'bus_info_image.html')

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

    return render(request, 'bus_info.html', {'bus_info_list': bus_info_list})