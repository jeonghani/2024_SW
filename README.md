# 2024_SW
매일 자정 github Actions로 send_result.py 파일 자동 실행

- .github/workflows/daily-run.yml : 자동화 설정 파일
- requirements.txt : 설치 필요한 패키지 명시
  - openai
  - requests
  - pillow
- send_result.py : 추리 게임에 필요한 리소스 생성 파이썬 파일
