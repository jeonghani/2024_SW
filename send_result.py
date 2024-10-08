from openai import OpenAI
import random
import requests
import json
from PIL import Image
from io import BytesIO
import base64
import os
import time

# # OpenAI API 키 설정
# openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 숫자만 추출하는 함수
def extract_int_from_string(s):
    return int(''.join(filter(str.isdigit, s)))

# 사건 상황 생성 프롬프트 함수
def generate_incident_description(place, time, weather):
    incident_prompt = f"""
    장소: {place}
    시간: {time}
    날씨: {weather}
    오늘 발생한 사건에 대한 요약을 300자 이내로 작성해줘. 모든 필드는 비어 있지 않게 채워줘.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 추리 게임 시나리오 기획자입니다."},
            {"role": "user", "content": incident_prompt}
        ]
    )
    incident_description = response.choices[0].message.content.strip()
    return incident_description

# 피해자 정보 생성 프롬프트 함수
def generate_victim_description(incident_description):
    victim_prompt = f"""
    사건 상황: {incident_description}에 맞는 피해자의 정보를 아래 형식으로 작성해줘. 모든 필드는 채워져야함.
    이름: 피해자의 이름 (필수)
    나이: 피해자의 나이 (필수)
    성별: 피해자의 성별 (필수)
    직업: 피해자의 직업 (필수)
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 추리 게임 시나리오 기획자입니다."},
            {"role": "user", "content": victim_prompt}
        ]
    )
    victim_description = response.choices[0].message.content.strip()
    victim_data = {}

    for line in victim_description.split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            victim_data[key.strip()] = value.strip()

    return victim_data

# 이미지 생성 함수
def generate_image(prompt, size):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        n=1
    )
    image_url = response.data[0].url
    print(image_url)
    img_response = requests.get(image_url)
    img = Image.open(BytesIO(img_response.content)).convert("RGBA")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return img_base64

# 필드가 비어 있으면 다시 생성하는 함수
def regenerate_field(prompt_template, existing_data, required_fields):
    while not all(existing_data.get(field) for field in required_fields):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 추리 게임 시나리오 기획자입니다."},
                {"role": "user", "content": prompt_template}
            ]
        )
        response_data = response.choices[0].message.content.strip()
        for line in response_data.split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                existing_data[key.strip()] = value.strip()

# 초기 설정
places = ["대학교 캠퍼스 도서관 앞", "도시의 19층짜리 건물의 IT기업 사무실", "큰 사거리에 위치한 대형마트",
          "풀과 나무가 많고 산책길이 있는 공원", "한 시골의 작은 동네 병원", "스산한 분위기의 공동묘지",
          "사람들의 발걸음이 많이 닿는 놀이공원", "수도권에 위치한 공룡 박물관", "이상하게 상어가 많은 아쿠아리움",
          "이제는 아무도 찾지 않는 폐건물", "신도시에 새로 지어진 아파트", "화물 컨테이너로 가득 찬 항구",
          "출국하는 사람들로 붐비는 공항", "촬영을 위해 준비 중인 방송국", "영화가 끝나고 관객이 다 나간 영화관"]
times = ["오전", "낮", "밤", "새벽"]
weather_conditions = ["비바람이 몰아치는 태풍이 부는 날", "햇빛이 너무 쨍쨍한 여름 날",
                      "입김이 나게 시리도록 추운 날", "불쾌하게 찝찝할만큼 습도가 높은 여름 날",
                      "하루종일 추적추적 비가 오는 날", "나들이 가기 딱 좋게 맑은 날",
                      "쨍쨍하다가 갑자기 소나기가 오는 날", "발자국도 금방 사라질듯이 눈이 오는 날",
                      "앞이 잘 보이지 않을 정도로 안개가 깔린 날", "마른 하늘에 우박이 갑자기 떨어지는 날"]

# 랜덤 선택
place = random.choice(places)
when = random.choice(times)
weather = random.choice(weather_conditions)

# 사건 상황 생성
story_line = generate_incident_description(place, when, weather)

# 피해자 정보 생성
victim_data = generate_victim_description(story_line)
victim_age = extract_int_from_string(victim_data['나이'])
story_line_with_victim = f"피해자 정보:\n이름: {victim_data['이름']}\n나이: {victim_age}\n성별: {victim_data['성별']}\n직업: {victim_data['직업']}\n\n{story_line}"

# 이미지 생성 프롬프트
image_prompt = f"{place}에서 {when} 동안, {weather} 날씨의 분위기를 반영한 장면. 이미지에 텍스트가 포함되어서는 안됩니다."
main_background_image = generate_image(image_prompt, "1024x1024")

# 응답 데이터 형식 수정
response_data = {
    "weather": weather,
    "time": when,
    "place": place,
    "mainBackgroundImage": main_background_image,
    "storyLine": story_line_with_victim,
    "victimName": victim_data['이름'],
    "victimAge": victim_age,
    "victimGender": victim_data['성별'],
    "victimOccupation": victim_data['직업']
}

# 디버깅을 위해 요청 보내기 전에 데이터를 출력합니다.
print("Sending the following payload:")
print(json.dumps(response_data, indent=4, ensure_ascii=False))

# HTTP 요청 헤더 설정
headers = {
    'Content-Type': 'application/json; charset=utf-8'
}

# 최종 엔드포인트에 payload 전송
final_url = "http://43.202.161.19:8080/api/resource/story"  # 최종 엔드포인트 URL
try:
    final_response = requests.post(final_url, data=json.dumps(response_data, ensure_ascii=False).encode('utf-8'), headers=headers)
    final_response.raise_for_status()
    print("Final request to http://43.202.161.19:8080/api/resource/story")
    print(final_response.status_code)
    # print(final_response.json())
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
    if err.response.content:
        print("Response content:", err.response.content.decode())
except Exception as err:
    print(f"Other error occurred: {err}")

# 용의자 생성 및 API 전송
suspects = []

def generate_and_send_suspect(i):
    suspect_prompt = f"""
    사건 상황: {response_data['storyLine']}에 맞는 용의자 {i+1}의 정보를 아래 형식으로 작성해줘.
    이름: 용의자의 이름
    나이: 용의자의 나이
    성별: 용의자의 성별
    직업: 용의자의 직업
    상태: 용의자의 현재 상황
    특이사항: 용의자와 피해자 {response_data['victimName']} ({response_data['victimAge']}세, {response_data['victimGender']}, {response_data['victimOccupation']})의 관계를 용의자의 말투로 100자 이내로 설명
    증거물품: 용의자가 남긴 증거물품
    증거물 설명: 증거물품에 대한 설명
    """

    retry_attempts = 3  # 시도 횟수를 늘립니다.
    for attempt in range(retry_attempts):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 추리 게임 시나리오 기획자입니다."},
                    {"role": "user", "content": suspect_prompt}
                ]
            )

            suspect_info = response.choices[0].message.content.strip()
            suspect_data = {}

            for line in suspect_info.split('\n'):
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    suspect_data[key.strip()] = value.strip()

            # 필드가 비어있을 경우 재생성
            required_suspect_fields = ["이름", "나이", "성별", "직업", "상태", "특이사항", "증거물품", "증거물 설명"]
            regenerate_field(suspect_prompt, suspect_data, required_suspect_fields)

            # 모든 필드가 채워졌는지 확인
            if not all(suspect_data.get(field) for field in required_suspect_fields):
                raise ValueError(f"Some fields are missing in suspect {i+1}")

            # 이미지 생성
            img_prompt = f"""
            하단의 내용을 반영하여 인물 1인의 정면 컬러사진을 현실에 실제 있는 인물처럼 생성 :
            1) 인물 정보이지만 이 텍스트를 포함해서는 안됩니다.
            - Name : {suspect_data.get("이름")}
            - Age: {suspect_data.get("나이")} years old
            - Gender: {suspect_data.get("성별")}
            - Occupation: {suspect_data.get("직업")}
            2) 인물 얼굴은 이미지의 정중앙에 배치, 얼굴 크기는 이미지의 1/9
            3) 배경은 흐릿하게 처리하고, 인물만 명확하게 보여주세요.
            4) 얼굴 특징을 실제 있는 인물처럼 현실적으로 표현하세요.
            5) 이미지에 텍스트를 포함하지 마세요.
            """
            suspect_image = generate_image(img_prompt, "1024x1024")

            evidence_img_prompt = f"""
            다음 물품을 실제 있는 물건으로 구현해줘:
            물품: {suspect_data.get("증거물품")}
            설명: {suspect_data.get("증거물 설명")}
            - 물건 1개만 명확하게 보여주세요.
            """
            evidence_image = generate_image(evidence_img_prompt, "1024x1024")

            suspect_payload = {
                "suspectName": suspect_data.get("이름"),
                "suspectAge": extract_int_from_string(suspect_data.get("나이")),
                "suspectGender": suspect_data.get("성별"),
                "suspectOccupation": suspect_data.get("직업"),
                "suspectSpeciality": suspect_data.get("상태"),
                "suspectTrait": suspect_data.get("특이사항"),
                "suspectImage": suspect_image,
                "evidenceName": suspect_data.get("증거물품"),
                "evidenceInfo": suspect_data.get("증거물 설명"),
                "evidenceImage": evidence_image
            }

            # 모든 필드가 채워진 경우에만 리스트에 추가
            if all(suspect_payload.values()):
                suspects.append(suspect_payload)

            # HTTP 요청 헤더 설정
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }

            # 최종 엔드포인트에 payload 전송
            final_url = "http://43.202.161.19:8080/api/resource/suspect"
            try:
                final_response = requests.post(final_url, data=json.dumps(suspect_payload, ensure_ascii=False).encode('utf-8'), headers=headers)
                final_response.raise_for_status()
                print(f"Final request for suspect {i+1} to {final_url}")
                print(final_response.status_code)
                # print(final_response.json())
                break  # 성공하면 루프 탈출

            except requests.exceptions.HTTPError as err:
                print(f"HTTP error occurred: {err}")
                if err.response.content:
                    print("Response content:", err.response.content.decode())
                if attempt < retry_attempts - 1:
                    print(f"Retrying... ({attempt+1}/{retry_attempts})")
                    time.sleep(5)  # 5초 대기 후 재시도

        except Exception as e:
            print(f"Error generating suspect {i+1}: {e}")
            if "Your request was rejected as a result of our safety system" in str(e):
                print(f"Skipping suspect {i+1} due to safety system restrictions.")
            if attempt < retry_attempts - 1:
                print(f"Retrying... ({attempt+1}/{retry_attempts})")
                time.sleep(5)  # 5초 대기 후 재시도

# 용의자 4명 생성 및 전송
while len(suspects) < 4:
    generate_and_send_suspect(len(suspects))

# 범인 결과 생성
culprit_prompt = f"""
다음 용의자 중 한 명이 범인입니다. 용의자 정보를 읽고 범인을 골라 아래 형식을 작성. 모든 필드는 채워져야함.
범인 : 범인의 이름
이유1 : 범인인 이유 150자 이내로 설명
이유2 : 범인인 이유 150자 이내로 설명
사건의 전말 : 사건에 대한 전말을 150자 이내로 설명
범인의 한마디 : 범인이 마지막으로 남길 한마디를 100자 이내로 작성
"""

culprit_prompt += "\n용의자 정보:\n"
for i, suspect in enumerate(suspects):
    culprit_prompt += f"{i+1}. 이름: {suspect['suspectName']}, 나이: {suspect['suspectAge']}, 성별: {suspect['suspectGender']}, 직업: {suspect['suspectOccupation']}, 특이사항: {suspect['suspectTrait']}, 증거물품: {suspect['evidenceName']}, 증거물 설명: {suspect['evidenceInfo']}\n"

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "당신은 추리 게임 시나리오 기획자입니다."},
        {"role": "user", "content": culprit_prompt}
    ]
)

culprit_response = response.choices[0].message.content.strip()
culprit_data = {}
for line in culprit_response.split('\n'):
    if ': ' in line:
        key, value = line.split(': ', 1)
        culprit_data[key.strip()] = value.strip()

culprit_name = culprit_data.get('범인')
culprit_info = next((suspect for suspect in suspects if suspect['suspectName'] == culprit_name), None)

if culprit_info:
    culprit = {
        "name": culprit_info['suspectName'],
        "age": culprit_info['suspectAge'],
        "gender": culprit_info['suspectGender'],
        "occupation": culprit_info['suspectOccupation']
    }
else:
    culprit = {
        "name": culprit_name,
        "age": "unknown",
        "gender": "unknown",
        "occupation": "unknown"
    }

victim = {
    "name": response_data['victimName'],
    "age": response_data['victimAge'],
    "gender": response_data['victimGender'],
    "occupation": response_data['victimOccupation']
}

def create_reason_prompt(reason, culprit, victim):
    prompt = f"""
    이유: {reason}
    범인: {culprit['name']} (나이: {culprit['age']}, 성별: {culprit['gender']}, 직업: {culprit['occupation']})
    피해자: {victim['name']} (나이: {victim['age']}, 성별: {victim['gender']}, 직업: {victim['occupation']})
    이 정보를 바탕으로 사건의 이유와 관련된 물품 1개를 실제 있는 물건으로 구현해줘.
    """
    return prompt

reason1_prompt = create_reason_prompt(culprit_data.get('이유1'), culprit, victim)
reason1_image_url = generate_image(reason1_prompt, "1024x1024")

reason2_prompt = create_reason_prompt(culprit_data.get('이유2'), culprit, victim)
reason2_image_url = generate_image(reason2_prompt, "1024x1024")

all_story = f"{response_data['weather']}\n{response_data['time']}\n{response_data['place']}\n{response_data['storyLine']}\n{culprit_data.get('사건의 전말')}"

result_data = {
    "criminal": culprit_data.get('범인'),
    "criminalSaying": culprit_data.get('범인의 한마디'),
    "caseBackground": culprit_data.get('사건의 전말'),
    "resultContent1": culprit_data.get('이유1'),
    "resultContent2": culprit_data.get('이유2'),
    "resultImage1": reason1_image_url,
    "resultImage2": reason2_image_url,
    "allStory": all_story  # 전달된 전체 스토리
}

# 최종 엔드포인트에 결과 데이터 전송
result_url = "http://43.202.161.19:8080/api/resource/result"  # 최종 엔드포인트 URL
try:
    result_response = requests.post(result_url, data=json.dumps(result_data), headers=headers)
    result_response.raise_for_status()
    print("Final request to http://43.202.161.19:8080/api/resource/result")
    print(result_response.status_code)
    # print(result_response.json())
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except Exception as err:
    print(f"Other error occurred: {err}")