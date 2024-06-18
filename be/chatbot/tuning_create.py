import openai
import os
from dotenv import load_dotenv
# .env 파일에서 환경 변수 로드
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# 환경 변수에서 OpenAI API 키와 Fine-Tuning 작업 ID를 가져옴
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