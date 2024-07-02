# obab-server

O-BAB의 백엔드 부분을 담당하는 리포지토리입니다. 이 프로젝트는 Python과 Django를 기반으로 서버 및 DB를 구축하였습니다.

<br/>

## 사용 기술 스택

| **분야**        | **기술 스택**                                                                                   |
|-----------------|-------------------------------------------------------------------------------------------------|
| **백엔드**      | Python 3.11.6, Django 5.0.3, DRF 3.14.0                                                         |
| **DB**          | PostgreSQL, Redis (계획)                                                                       |
| **Infra**       | AWS (계획 중), Route 53, SSL/TLS                                                                |
| **API**         | Kakao API, Google API, Naver API, OPENAI API                                                    |
| **기타**        |                                                                              |

<br/>

## Getting Started

### 필수 사항

시작하기 전에 시스템에 다음이 설치되어 있는지 확인하십시오:
- Python

### PostgreSQL 데이터베이스 생성

#### macOS

```bash
brew services start postgresql
psql postgres
create database obab;
```

#### Windows

```bash
# PostgreSQL 다운로드 및 설치
https://www.postgresql.org/download/windows/

# 설치가 완료되면 pgAdmin을 실행합니다.
# Databases에 obab 데이터베이스를 생성합니다.
```

### 프로젝트 시작

1. **저장소를 클론합니다:**

```bash
git clone https://github.com/O-BAB/obab-server.git
cd obab-server
```

2. **가상 환경을 만듭니다:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **프로젝트 종속성을 설치합니다:**

```bash
pip install -r requirements.txt
```

4. **데이터베이스 마이그레이션을 실행합니다:**

```bash
python manage.py makemigrations --settings=obab_server.settings.local_settings
python manage.py migrate --settings=obab_server.settings.local_settings
```

5. **프로젝트를 실행합니다:**

```bash
python manage.py runserver --settings=obab_server.settings.local_settings
```

6. **웹 브라우저를 열고 [http://localhost:8000](http://localhost:8000) 에 접속하여 애플리케이션을 확인합니다.**

<br/>

## 프로젝트 구조

<a href="https://github.com/O-BAB/obab-server/blob/develop/tree.txt">프로젝트 구조</a>
