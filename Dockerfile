FROM python:3.10.14

# 작업 디렉토리
WORKDIR /app

# 패키지 설치
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 프로젝트 소스 코드를 컨테이너 내로 복사
COPY . /app/

# 포트
EXPOSE 8000

# 서버 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "LocalSharing.wsgi:application"]