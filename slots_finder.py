import json
import time
import requests
import schedule
from datetime import datetime
from playsound import playsound

"""Run code at hr:00:00 eg 11:00:00, 11:15:00.... etc"""
# Code Written by Laxman
monday_date = '17-05-2021'
pin_codes = ['464001', '464551'] # Add more pin codes if you want
#  '464661'


def find_slots():
    """Hit API and find the slots, If available Play Alarm - Laxman """
    print(f'Running at time: {datetime.now()}', end=' ')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    for pin_code in pin_codes:
        response_1 = requests.options(
            f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin_code}&date={monday_date}',
            headers=headers)
        # For cache False
        response = requests.get(
            f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin_code}&date={monday_date}',
            headers=headers)
        data = json.loads(response.text)
        centers = data.get('centers', [])
        print(centers)
        if len(centers):
            centers_age_18 = [center for center in centers for session in center.get('sessions', []) if
                              session.get('min_age_limit') == 18 and
                              session.get('available_capacity', 0)]
            print('Centers Available')
            if len(centers_age_18):
                print(f'Slots Available for 18+ on Pin Code : {pin_code}')
                playsound('car_horn_alarm.mp3')
                time.sleep(20)
            else:
                print('No Slots Available for 18+')
        else:
            print('No Slots Available')


schedule.every(5).seconds.do(find_slots)

while True:
    schedule.run_pending()
    time.sleep(1)
