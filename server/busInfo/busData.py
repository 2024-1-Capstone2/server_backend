import requests
import pprint
import json
from django.utils import timezone
import datetime
from .models import Bus, BusStop, TimeTable, City, District
from django.db.models import Count
# City, District

def test():
    # city = City.objects.all()
    # print("city")
    # print(city)
    # district = District.objects.all()
    # print("district")
    # print(district)
    bus = Bus.objects.get(number='6009')
    print("bus")
    print(f"버스 번호: {bus.number}, 지역: {bus.area}, 요금: {bus.fare}, 회사: {bus.company}")
    # time_table = TimeTable.objects.filter(bus=bus)
    # for timetable in time_table:
    #     print(f"출발 버스 정류장: {timetable.departure_bus_stop.name}, 도착 버스 정류장: {timetable.arrival_bus_stop.name}, 시간: {timetable.time}")
    # bus_stops = BusStop.objects.all()
    # print("bus_stops")
    # print(bus_stops)

def addDistrict():
    districts_english = ['Gangnam-gu', 'Nowon-gu', 'Gangseo-gu', 'Guro-gu', 'Mapo-gu', 'Jongno-gu', 'Jung-gu',
                         'Seocho-gu', 'Eunpyeong-gu', 'Songpa-gu', 'Yangcheon-gu', 'Yeongdeungpo-gu', 'Dongjak-gu',
                         'Gwanak-gu', 'Geumcheon-gu', 'Gangdong-gu', 'Yongsan-gu', 'Seongdong-gu', 'Gwangjin-gu',
                         'Seodaemun-gu', 'Dongdaemun-gu', 'Jungnang-gu', 'Seongbuk-gu', 'Gangbuk-gu', 'Dobong-gu']

    for district_name in districts_english:
        District.objects.get_or_create(name=district_name, city=City.objects.get(name='서울'))

def addCity():
    area_dict = {
        '1': '서울',
        '2': '경기',
        '3': '인천',
        '4': '강원',
        '5': '충청',
        '6': '경상',
        '7': '전라',
    }
    for area_code, area_name in area_dict.items():
        City.objects.get_or_create(name=area_name)

def addBusInfo():
    districts = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구',
                 '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']
    city, _ = City.objects.get_or_create(name='서울')
    for district_name in districts:
        district, _ = District.objects.get_or_create(name=district_name, city=city)
    return 1

def addBusStop():
    bus_stops_info_english = {
        'Gangnam-gu': ['Gangnam Station', 'Sinsa Station', 'Samsung Station'],
        'Nowon-gu': ['Nowon Station', 'Junggye Station', 'Suyu Station'],
        'Gangseo-gu': ['Gimpo Airport', 'Songjeong Station', 'Balsan Station'],
        'Guro-gu': ['Guro Station (AK Plaza)', 'Daerim Station', 'Guro Digital Complex Station'],
        'Mapo-gu': ['Hongik University Station', 'Hapjeong Station', 'Gongdeok Station (Lotte City Hotel)'],
        'Jongno-gu': ['Gwanghwamun (Four Seasons Hotel)', 'Jongno 3-ga', 'Dongdaemun History & Culture Park'],
        'Jung-gu': ['Seoul Station', 'Myeongdong Station', 'Chungmuro Station (PJ Hotel)'],
        'Seocho-gu': ['Seoul National University of Education Station', 'Yangjae Station'],
        'Eunpyeong-gu': ['Bulgwang Station', 'Yeonsinnae Station', 'Gupabal Station'],
        'Songpa-gu': ['Jamsil Station', 'Garak Market'],
        'Yangcheon-gu': ['Mokdong Station', 'Omokgyo Station', 'Sinjeongnegeori'],
        'Yeongdeungpo-gu': ['Yeongdeungpo Station (Fairfield by Marriott)', 'Yeouinaru Station', 'Dangsan Station'],
        'Dongjak-gu': ['Isu Station (Sadang Post Office)', 'Sangdo Station'],
        'Gwanak-gu': ['Sillim Station', 'Seoul National University', 'Bongcheon Station'],
        'Geumcheon-gu': ['Geumcheon-gu Office (Siheung Gaek)', 'Gasan Digital Complex Station'],
        'Gangdong-gu': ['Cheonho Station', 'Gangdong Station', 'Gil-dong Station'],
        'Yongsan-gu': ['Namsan (Grand Hyatt Seoul)', 'Yongsan Station', 'Samgakji Station'],
        'Seongdong-gu': ['Wangsimni Station (Seongdong-gu Office)', 'E-Mart Seongsu-dong'],
        'Gwangjin-gu': ['Gwangjin-gu Council (Konkuk University Station)', 'Gwangnaru Station'],
        'Seodaemun-gu': ['Sinchon Station', 'Hongje Station', 'Dongnimmun Station'],
        'Dongdaemun-gu': ['Cheongnyangni Station', 'Dongdaemun History & Culture Park Station'],
        'Jungnang-gu': ['Jungwha Station', 'Mangwoo Station'],
        'Seongbuk-gu': ['Hansung University Station', 'Gireum Station (Gireum New Town)'],
        'Gangbuk-gu': ['Mia Station', 'Suyu Station (Gangbuk-gu Office)'],
        'Dobong-gu': ['Ssangmun Station']
    }
    #
    # bus_stops_info = {
    #     '강남구': ['강남역', '신사역', '삼성역(그랜드인터컨티넬)'],
    #     '노원구': ['노원역', '중계역', '수락산역'],
    #     '강서구': ['김포공항', '송정역', '발산역'],
    #     '구로구': ['구로역(애경백화점)', '대림역', '구로디지털단지역'],
    #     '마포구': ['홍대입구역', '합정역', '공덕역(롯데시티호텔)'],
    #     '종로구': ['광화문(포시즌호텔)', '종로3가', '동대문역사문화공원'],
    #     '중구': ['서울역', '명동역', '충무로역(PJ호텔)'],
    #     '서초구': ['교대역', '양재역'],
    #     '은평구': ['불광역', '연신내역', '구파발역'],
    #     '송파구': ['잠실역', '가락시장'],
    #     '양천구': ['목동역', '오목교역', '신정교입구'],
    #     '영등포구': ['영등포역(페어필드바이메리어트)', '여의나루역', '당산역'],
    #     '동작구': ['이수역(사당우체국)', '상도역'],
    #     '관악구': ['신림역', '서울대학교', '봉천역'],
    #     '금천구': ['금천구청(시흥고개)', '가산디지털단지역'],
    #     '강동구': ['천호역', '강동역', '길동역'],
    #     '용산구': ['남산(그랜드하얏트서울호텔)', '신용산역', '삼각지역'],
    #     '성동구': ['왕십리역(성동구청)', '성수동이마트'],
    #     '광진구': ['광진구의회(건대입구역)', '광나루역'],
    #     '서대문구': ['신촌역', '홍제역', '독립문역'],
    #     '동대문구': ['청량리역', '동대문역사문화공원역'],
    #     '중랑구': ['중화역', '망우역'],
    #     '성북구': ['한성대입구', '길음역(길음뉴타운)'],
    #     '강북구': ['미아사거리역', '수유역(강북구청)'],
    #     '도봉구': ['쌍문역']
    # }

    for district_name, bus_stops in bus_stops_info_english.items():
        district = District.objects.get(name=district_name)
        for bus_stop_name in bus_stops:
            BusStop.objects.get_or_create(name=bus_stop_name, district=district)



def getBusInfo():
    area_dict = {
        '1': '서울',
        '2': '경기',
        '3': '인천',
        '4': '강원',
        '5': '충청',
        '6': '경상',
        '7': '전라',
    }

    url = 'http://apis.data.go.kr/B551177/BusInformation/getBusInfo'
    params ={'serviceKey' : 'L0N+7lJk031KQZI30ENd+bmj6SJ+bHrcs1Abwred2W9LR9HviOYOmk0iZDSzyRG0IWmHA4uGz1ZsCuQ7pBP81w==',
             'numOfRows' : '10', 'pageNo' : '1', 'area' : '1', 'type' : 'json' }

    response = requests.get(url, params=params)

    response.encoding = 'utf-8'

    data = response.json()

    for item in data['response']['body']['items']:
        bus_number = item['busnumber']
        if bus_number :
            bus = Bus.objects.get(number=bus_number)

            bus_fare = item['adultfare'].split(',')[0] if item['adultfare'] else '17000'
            bus_fare = int(bus_fare)
            bus_area = item['area'] if item['area'] else '8'
            bus_company = item['cpname'] if item['cpname'] else '인천국제공항공사'

            bus.fare = bus_fare
            bus.area = area_dict[bus_area]
            bus.company = bus_company
            bus.save()

            # for time_str in item['t1wdayt'].split(', '):
            #     try:
            #         departure_time = datetime.datetime.strptime(time_str, '%H%M').time()
            #     except ValueError:
            #         continue  # 잘못된 시간 형식인 경우 건너뛰기
            #
            #     # TimeTable 인스턴스 생성 및 저장
            #     TimeTable.objects.get_or_create(
            #         bus=bus,
            #         departure_bus_stop=BusStop.objects.get(name='인천공항1터미널'),
            #         arrival_bus_stop=BusStop.objects.get(name='Sinsa Station'),
            #         time=departure_time
            #     )
