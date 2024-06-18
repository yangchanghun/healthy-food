import openai
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# 환경 변수에서 OpenAI API 키와 Fine-Tuning 작업 ID를 가져옴
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
fine_tuning_job_id ="ftjob-nORJC3JbShABXpKTn3I2uAC6"

# 환경 변수가 올바르게 로드되었는지 확인
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")
print(f"fine_tuning_job_id: {fine_tuning_job_id}")

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

# Fine-Tuning 작업 상태 확인 (반복해서 체크)
while True:
    try:
        job_status = openai.FineTuningJob.retrieve(id=fine_tuning_job_id)
        status = job_status['status']
        print(f"Fine-Tuning Job Status: {status}")

        # 작업의 상태가 완료(성공 또는 실패)되었을 때 세부 정보 출력
        if status in ['succeeded', 'failed']:
            print(f"Fine-Tuning Job ID: {job_status['id']}")
            print(f"Status: {job_status['status']}")
            print(f"Model: {job_status.get('fine_tuned_model', 'N/A')}")
            print(f"Created at: {job_status['created_at']}")
            
            if 'updated_at' in job_status:
                print(f"Updated at: {job_status['updated_at']}")
            else:
                print("Updated at: N/A")

            # 오류 메시지 출력
            if status == 'failed':
                print(f"Error: {job_status.get('error', 'Unknown error')}")

            training_file_id = job_status['training_file']
            training_file_status = openai.File.retrieve(id=training_file_id)
            print(f"Training File ID: {training_file_id}")
            print(f"Training File Status: {training_file_status['status']}")
            print(f"Training File Purpose: {training_file_status['purpose']}")
            print(f"Training File Created at: {training_file_status['created_at']}")
            break
            
            

    except Exception as e:
        print(f"Error retrieving job status: {e}")
        break
