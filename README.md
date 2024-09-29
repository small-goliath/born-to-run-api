# born-to-run-api
본투런api 파이썬 버전

app
├── api # FastAPI 애플리케이션의 API 엔드포인트 및 라우터가 정의된 디렉토리
├── core # 애플리케이션의 핵심 기능 및 설정이 정의된 모듈이 위치하는 디렉토리
├── schemas # Pydantic 스키마 정의가 포함된 디렉토리로, 데이터의 유효성 검사와 API 요청 및 응답의 구조를 정의
├── tests # 테스트 파일이 위치한 디렉토리
├── __init__.py # Python에서 패키지로 인식되도록 하는 빈 __init__.py 파일
├── backend_pre_start.py # FastAPI 애플리케이션 시작 전에 실행할 코드가 정의된 파
├── initial_data.py # 애플리케이션 초기 데이터를 설정하는 스크립트 파일
├── tests_pre_start.py # 테스트 시작 전에 실행할 코드가 정의된 파일
├── main.py # FastAPI 애플리케이션의 진입점이 되는 파일로, API 라우터를 구성하고 애플리케이션을 실행
├── models.py # SQLAlchemy 모델이 정의된 파일
├── crud.py # 데이터베이스 CRUD(Create, Read, Update, Delete) 연산을 수행하는 함수가 정의된 파일
├── utils.py # 애플리케이션에서 사용되는 유틸리티 함수가 정의된 파일

.env # 환경 변수 설정이 담긴 파일
.gitignore # Git으로 추적하지 않을 파일 및 디렉토리를 지정하는 파일
backend.dockerfile # FastAPI 애플리케이션을 위한 Docker 이미지를 빌드하는 데 사용되는 Docker 파일