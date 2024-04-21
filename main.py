import os
import requests
from datetime import datetime

API_ENDPOINT ="https://trackapi.nutritionix.com/v2/natural/exercise"

APP_ID = os.environ.get('NUTRITIONIX_APP_ID')
API_KEY = os.environ.get('NUTRITIONIX_API_KEY')
YOUR_USERNAME = os.environ.get('NUTRITIONIX_API_USERNAME')
YOUR_PASSWORD = os.environ.get('NUTRITIONIX_API_PASSWD')
exercise_text = input("Tell me which exercise you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": "male",
    "weight_kg": 86,
    "height_cm": 186,
    "age": 21,
}
print(API_KEY)
response = requests.post(url=API_ENDPOINT, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

sheety_endpoint = os.environ.get('SHEETY_ENDPOINT')
sheet_response = requests.post(sheety_endpoint, json=sheet_inputs, auth=(
      YOUR_USERNAME,
      YOUR_PASSWORD,
  )
)
print(sheet_response.text)

