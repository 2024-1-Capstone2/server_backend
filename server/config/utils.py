# config/utils.py

from rest_framework import serializers

def get_recognition_result(endpoint):
    # 인식 결과를 가져오는 테스트용 함수
    recognition_results = {
        'ticket/region': {'isRecognized': True, 'isLocationChosen': True, 'upperLocation': '서울'},
        'ticket/small-region': {'isRecognized': True, 'isLocationChosen': True, 'lowerLocation': '용산구'},
        'ticket/bus-stop': {'isRecognized': True, 'isBusStopChosen': True, 'busStopName': '신용산역'},
        'ticket/bus': {'isRecognized': True, 'busId': '506', 't1FirstSchedule': '06:00', 't1LastSchedule': '23:00', 't2FirstSchedule': '06:30', 't2LastSchedule': '23:30', 'fare': 1200},
        'ticket/schedule': {'isRecognized': True, 'isScheduleChosen': True, 'boardingTime': '08:12', 'busLevel': '2F', 'busStopId': '4A'},
        'ticket/cnt': {'isRecognized': True, 'isFareChosen': True, 'adult': 1, 'student': 0, 'child': 0, 'totalFare': 1200},
        'ticket/purchase': {'isRecognized': True},

        'refund/ticket': {'isRecognized': True},
        'refund/question': {'isRecognized': True},
        'general/question': {'isRecognized': True},
        'general/re-question': {'isRecognized': True},
        'general/info-desk': {'location': '4F:1A'},
        'busInfo/boarding-id': {'isRecognized': True, 'isValid': True, 'boardingId': '4F'},
        'busInfo/gate': {'isRecognized': True, 'isValid': True, 'busStop': 12},
        'busInfo/schedule': {'isRecognized': True, 'isValid': True, 'busId': 5009,
                              'schedule': ['12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30',
                               '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00',
                               '10:30', '11:00', '11:30']},
        'busInfo/schedule-number': {'isRecognized': True, 'isValid': True, 'busId': 5009,
                              'schedule': ['12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30',
                               '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00',
                               '10:30', '11:00', '11:30']},
    }
    return recognition_results.get(endpoint, '결과 없음')

class RecognitionResultSerializer(serializers.Serializer):
    response = serializers.DictField(
        child=serializers.JSONField()
    )