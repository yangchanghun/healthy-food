import openai
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv('./chatbot/.env')

# 환경 변수에서 OpenAI API 키를 가져옴
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

# 파일 경로 설정
file_path = 'C:/nonoo/workspace_dj/healthy-food/be/chatbot/train.jsonl'

# 파일 업로드
response = openai.File.create(
    file=open(file_path, 'rb'),
    purpose='fine-tune'
)

# 업로드된 파일 ID 확인
file_id = response['id']
print(f"Uploaded file ID: {file_id}")

# 업로드된 파일 ID를 사용하여 파인튜닝 작업 생성
fine_tune_response = openai.FineTuningJob.create(
    training_file=file_id,
    model="gpt-3.5-turbo"
)

# 결과 출력
print(fine_tune_response)
