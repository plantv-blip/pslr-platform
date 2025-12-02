# 🚀 PSLR Platform 배포 가이드

**완전한 단계별 가이드 - 초보자도 30분 안에 배포 가능!**

---

## 📋 목차

1. [사전 준비](#사전-준비)
2. [Railway 배포 (추천)](#railway-배포-추천)
3. [Render 배포](#render-배포)
4. [Vercel 배포](#vercel-배포)
5. [커스텀 도메인 연결](#커스텀-도메인-연결)
6. [환경 변수 설정](#환경-변수-설정)
7. [트러블슈팅](#트러블슈팅)

---

## 사전 준비

### 1. GitHub 계정
- https://github.com 에서 계정 생성

### 2. API 키 준비
최소한 1개 이상의 LLM API 키 필요:

- **OpenAI**: https://platform.openai.com/api-keys
  - GPT-4o 사용 가능
  
- **Anthropic** (선택): https://console.anthropic.com/
  - Claude-3.5-Sonnet 사용 가능
  
- **Google AI** (선택): https://makersuite.google.com/app/apikey
  - Gemini-2.0-Flash 사용 가능

### 3. Git 설치
```bash
# Mac
brew install git

# Windows
# https://git-scm.com/download/win 다운로드

# Linux
sudo apt-get install git
```

---

## Railway 배포 (추천)

### 왜 Railway인가?
- ✅ 무료 티어 제공 ($5/월 크레딧)
- ✅ PostgreSQL 자동 생성
- ✅ HTTPS 자동 설정
- ✅ GitHub 자동 배포
- ✅ 클릭 몇 번으로 완료

### Step 1: GitHub에 코드 업로드

```bash
# 1. 프로젝트 폴더로 이동
cd pslr-platform-production

# 2. Git 초기화
git init

# 3. 모든 파일 추가
git add .

# 4. 첫 커밋
git commit -m "Initial commit: PSLR Platform v3.0"

# 5. GitHub에서 새 저장소 생성
# https://github.com/new

# 6. 원격 저장소 연결 (GitHub에서 제공하는 URL 사용)
git remote add origin https://github.com/yourusername/pslr-platform.git

# 7. 푸시
git branch -M main
git push -u origin main
```

### Step 2: Railway 프로젝트 생성

1. **Railway 가입**: https://railway.app
   - GitHub 계정으로 로그인 추천

2. **New Project 클릭**

3. **"Deploy from GitHub repo" 선택**

4. **저장소 선택**:
   - `yourusername/pslr-platform` 선택
   - Railway가 자동으로 저장소 스캔

5. **자동 감지 확인**:
   - Railway가 `Procfile` 감지
   - Python 프로젝트 자동 인식 ✅

### Step 3: PostgreSQL 추가

1. **프로젝트 대시보드**에서:
   - "New" 버튼 클릭
   - "Database" 선택
   - "PostgreSQL" 선택

2. **자동 연결**:
   - Railway가 자동으로 `DATABASE_URL` 환경 변수 생성 ✅
   - 앱과 DB 자동 연결 ✅

### Step 4: 환경 변수 설정

1. **앱 서비스 클릭** (PostgreSQL 아님!)

2. **"Variables" 탭 클릭**

3. **다음 변수 추가**:
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   SECRET_KEY=your-random-secret-key-here
   FLASK_ENV=production
   ```

4. **SECRET_KEY 생성 방법**:
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **선택 사항** (다른 모델 사용 시):
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=...
   DEEPSEEK_API_KEY=...
   XAI_API_KEY=...
   ```

### Step 5: 배포 확인

1. **"Deployments" 탭**에서 진행 상황 확인

2. **로그 확인**:
   - "View Logs" 클릭
   - 오류 없이 완료되면 성공 ✅

3. **URL 확인**:
   - "Settings" 탭
   - "Public Networking" 섹션
   - `https://your-project.up.railway.app` 복사

4. **브라우저에서 접속**:
   - URL 열기
   - PSLR Platform 로딩 확인 🎉

### Step 6: 데이터베이스 마이그레이션 확인

Railway가 `Procfile`의 `release` 명령을 자동 실행:
```
release: flask db upgrade
```

만약 수동 실행이 필요하면:
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 마이그레이션 실행
railway run flask db upgrade
```

---

## Render 배포

### Step 1: Render 가입
https://render.com → Sign Up

### Step 2: New Web Service
1. Dashboard → "New" → "Web Service"
2. "Connect a repository" → GitHub 연결
3. 저장소 선택

### Step 3: 설정
```
Name: pslr-platform
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --config gunicorn.conf.py
```

### Step 4: PostgreSQL 추가
1. Dashboard → "New" → "PostgreSQL"
2. Name: `pslr-db`
3. 자동 생성 완료

### Step 5: DB 연결
1. Web Service → "Environment"
2. "Add from Database" 클릭
3. `pslr-db` 선택
4. `DATABASE_URL` 자동 추가 ✅

### Step 6: 환경 변수
```
OPENAI_API_KEY=...
SECRET_KEY=...
FLASK_ENV=production
```

### Step 7: 배포
"Create Web Service" → 자동 배포 시작

---

## Vercel 배포

⚠️ **주의**: Vercel은 Serverless이므로 PostgreSQL 별도 필요

### Step 1: Vercel CLI 설치
```bash
npm install -g vercel
```

### Step 2: 배포
```bash
cd pslr-platform-production
vercel login
vercel
```

### Step 3: 외부 DB 사용
Vercel은 DB를 제공하지 않으므로:
- **Supabase**: https://supabase.com (무료 PostgreSQL)
- **Neon**: https://neon.tech (무료 PostgreSQL)

---

## 커스텀 도메인 연결

### 도메인 구매
- Namecheap: https://www.namecheap.com
- GoDaddy: https://www.godaddy.com
- Cloudflare: https://www.cloudflare.com

추천 도메인:
- `pslr.ai`
- `pslrscan.com`
- `pslr-platform.com`

### Railway에서 도메인 추가

1. **Railway Dashboard**:
   - Settings → Networking
   - "Custom Domain" 클릭

2. **도메인 입력**:
   - 예: `pslr.ai`

3. **DNS 설정**:
   Railway가 제공하는 정보로 DNS 레코드 추가:
   ```
   Type: CNAME
   Name: @ (또는 www)
   Value: your-project.up.railway.app
   ```

4. **전파 대기**:
   - 5분~24시간 (보통 10분 내)
   - https://www.whatsmydns.net 에서 확인

---

## 환경 변수 설정

### 필수 환경 변수
```bash
# 데이터베이스 (Railway/Render 자동)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Flask
SECRET_KEY=your-64-char-random-hex-string
FLASK_ENV=production

# LLM API (최소 1개)
OPENAI_API_KEY=sk-proj-...
```

### 선택 환경 변수
```bash
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
DEEPSEEK_API_KEY=...
XAI_API_KEY=...
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## 트러블슈팅

### 1. "Application failed to start"

**원인**: 환경 변수 누락

**해결**:
```bash
# Railway 로그 확인
railway logs

# 필수 변수 확인
- DATABASE_URL ✅
- SECRET_KEY ✅
- OPENAI_API_KEY ✅
```

---

### 2. "Database connection failed"

**원인**: DATABASE_URL 형식 오류

**해결**:
Railway/Render가 `postgres://`로 시작하면 자동 변환됨
```python
# config.py에서 자동 처리됨
if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
```

---

### 3. "Import error: No module named 'psycopg2'"

**원인**: PostgreSQL 드라이버 누락

**해결**:
```bash
# requirements.txt 확인
psycopg2-binary==2.9.9  # 있는지 확인
```

---

### 4. "Migration pending"

**해결**:
```bash
# Railway CLI로 수동 실행
railway run flask db upgrade
```

---

### 5. "502 Bad Gateway"

**원인**: 앱이 시작되지 않음

**해결**:
1. 로그 확인
2. 환경 변수 확인
3. `gunicorn.conf.py` 확인

---

### 6. "CORS error"

**해결**:
```bash
# 환경 변수 추가
CORS_ORIGINS=https://yourdomain.com
```

---

## 성능 최적화

### 1. Worker 수 조정
```python
# gunicorn.conf.py
workers = 4  # CPU 코어 수 × 2 + 1
```

### 2. 캐싱 추가 (Redis)
```bash
# Railway에서 Redis 추가
# New → Database → Redis

# 환경 변수 자동 추가:
REDIS_URL=redis://...
```

### 3. CDN 사용 (Cloudflare)
- DNS를 Cloudflare로 변경
- 자동 CDN 적용 ✅

---

## 모니터링

### Railway 모니터링
```bash
# 실시간 로그
railway logs --tail

# CPU/메모리 사용량
# Dashboard → Metrics 탭
```

### Sentry 연동 (선택)
```bash
pip install sentry-sdk[flask]
```

```python
# app.py
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

---

## 비용 예상

### Railway (무료 티어)
- $5/월 크레딧 제공
- 500시간 실행 시간
- 소규모 프로젝트: **무료**
- 중규모: $5-20/월

### Render (무료 티어)
- 750시간/월 무료
- 15분 비활성 시 슬립
- 프로덕션: $7/월부터

### Vercel + Supabase
- Vercel: 무료 (취미용)
- Supabase: 무료 (500MB DB)

---

## 체크리스트

배포 전:
- [ ] GitHub 저장소 생성
- [ ] API 키 준비
- [ ] `.env.example` 복사하여 `.env` 생성
- [ ] `.gitignore` 확인 (`.env` 포함)

배포 후:
- [ ] URL 접속 확인
- [ ] `/health` 엔드포인트 확인
- [ ] 테스트 분석 실행
- [ ] 히스토리 확인
- [ ] 로그 모니터링

---

## 다음 단계

1. **커스텀 도메인 연결**
2. **Google Analytics 추가**
3. **사용자 인증 구현**
4. **API Rate Limiting**
5. **자동 백업 설정**

---

**배포 성공을 축하합니다! 🎉**

문제가 있으면 GitHub Issues에 문의하세요.
