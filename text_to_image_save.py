import os
import requests
import base64
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
if not STABILITY_API_KEY:
    raise ValueError("Missing Stability API key.")

def generate_images(text, style=None):
    engine_id = 'stable-diffusion-v1-6'
    api_host = 'https://api.stability.ai'
    api_key = STABILITY_API_KEY
    
    # 요청 본문 작성 - JSON 형식
    request_body = {
        "text_prompts": [
            {
                "text": text,
            },
        ],
        "cfg_scale": 7,
        "steps": 30,
        "samples": 1,
    }
    if style:
        request_body["style_preset"] = style
    
    # API 요청 보내기
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        json=request_body,
    )
    
    # 응답 상태 코드 확인
    if response.status_code != 200:
        raise Exception(f"Non-200 response: {response.text}")
    
    response_json = response.json()
    
    # 이미지 데이터 추출 및 변환
    generated_image_base64 = response_json['artifacts'][0]['base64']
    
    # base64 디코딩하여 파일로 저장
    image_data = base64.b64decode(generated_image_base64)
    file_path = 'generated_image.png'
    with open(file_path, 'wb') as f:
        f.write(image_data)
    
    return file_path

# 함수 사용 예제
text_prompt = "write here"
style_preset = "refer docs"
generated_image_path = generate_images(text_prompt, style_preset)
print(f"Generated image saved to: {generated_image_path}")
