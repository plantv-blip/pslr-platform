# 🔮 PSLR Live Platform - Production Version

**Physical-Spiritual-Logical-Relational Framework for LLM Cognitive Bias Analysis**

대규모 언어모델(LLM)의 인지적 편향을 PSLR 네 차원으로 측정하고 시각화하는 프로덕션 플랫폼입니다.

## 📊 주요 기능

- ✅ **실시간 분석**: 5개 주요 LLM (GPT-4o, Claude, Gemini, DeepSeek, Grok) 실시간 분석
- ✅ **PostgreSQL 통합**: 모든 분석 결과 영구 저장
- ✅ **3D 시각화**: Three.js 기반 3D 인터랙티브 시각화
- ✅ **히스토리 관리**: 실험 결과 저장, 검색, 필터링
- ✅ **다국어 지원**: 12개 언어 지원
- ✅ **프로덕션 준비**: Gunicorn, PostgreSQL, Docker 지원

## 📄 논문 참조

이 플랫폼은 다음 논문의 연구 결과를 기반으로 합니다:

**"Cognitive Spectrum Analysis of Large Language Models Using PSLR Scan Methodology"**
- Author: Young (Independent AI Research)
- Date: November 2025
- Version: 1.0 - Final Integration

---

## 🚀 빠른 시작

### Option 1: Railway 배포 (추천 - 가장 쉬움)

1. **Railway 계정 생성**: https://railway.app
2. **GitHub 저장소 생성 및 푸시**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/pslr-platform.git
   git push -u origin main
   ```

3. **Railway에서 배포**:
   - Railway Dashboard → "New Project"
   - "Deploy from GitHub repo" 선택
   - 저장소 선택
   - Railway가 자동으로 PostgreSQL 생성 및 연결

4. **환경 변수 설정** (Railway Dashboard → Variables):
   ```
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=...
   SECRET_KEY=your-random-secret-key
   ```

5. **완료!** 🎉
   - URL: `https://your-project.up.railway.app`

---

### Option 2: Render 배포

1. **Render 계정 생성**: https://render.com
2. **New Web Service** → GitHub 연동
3. **설정**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --config gunicorn.conf.py`
4. **PostgreSQL 추가**: Dashboard → New → PostgreSQL
5. **환경 변수 연결**:
   ```
   DATABASE_URL=(Render가 자동 설정)
   OPENAI_API_KEY=...
   SECRET_KEY=...
   ```

---

### Option 3: Docker로 로컬 실행

```bash
# 1. 환경 변수 설정
cp .env.example .env
nano .env  # API 키 입력

# 2. Docker Compose 실행
docker-compose up -d

# 3. 브라우저에서 열기
open http://localhost:5000
```

---

### Option 4: 로컬 개발 환경

```bash
# 1. 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
cp .env.example .env
nano .env

# 4. 데이터베이스 초기화
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 5. 서버 실행
python app.py

# 6. 브라우저에서 열기
open http://localhost:5000
```

---

## 🗄️ 데이터베이스 스키마

### PSLRAnalysis 테이블
```sql
id              INTEGER PRIMARY KEY
concept         VARCHAR(200)
language        VARCHAR(10)
model           VARCHAR(50)
model_name      VARCHAR(100)
p_value         FLOAT
s_value         FLOAT
l_value         FLOAT
r_value         FLOAT
reasoning       TEXT
raw_response    TEXT
response_time   INTEGER
created_at      TIMESTAMP
metadata        JSON
```

---

## 📡 API 엔드포인트

### POST /api/analyze
단일 개념 분석 및 DB 저장

**Request:**
```json
{
  "concept": "Love",
  "model": "gpt-4o",
  "language": "en",
  "api_key": "sk-..."
}
```

**Response:**
```json
{
  "success": true,
  "id": 123,
  "concept": "Love",
  "model_name": "GPT-4o",
  "result": {
    "P": 0.45,
    "S": 0.60,
    "L": 0.35,
    "R": 0.60,
    "reasoning": "..."
  },
  "timestamp": "2025-11-25T10:00:00",
  "response_time": 1234
}
```

---

### GET /api/history
분석 히스토리 조회

**Parameters:**
- `limit`: 결과 개수 (기본: 20)
- `model`: 모델 필터 (선택)
- `concept`: 개념 검색 (선택)

**Example:**
```bash
curl "https://your-app.railway.app/api/history?limit=10&model=gpt-4o"
```

---

### GET /api/stats
플랫폼 통계

**Response:**
```json
{
  "total_analyses": 1234,
  "total_concepts": 45,
  "total_models": 5
}
```

---

### GET /health
헬스 체크

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## 🔧 환경 변수 설명

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `DATABASE_URL` | PostgreSQL 연결 URL | ✅ (Railway/Render 자동) |
| `OPENAI_API_KEY` | OpenAI API 키 | ✅ |
| `ANTHROPIC_API_KEY` | Anthropic API 키 | 선택 |
| `GOOGLE_API_KEY` | Google API 키 | 선택 |
| `DEEPSEEK_API_KEY` | DeepSeek API 키 | 선택 |
| `XAI_API_KEY` | xAI API 키 | 선택 |
| `SECRET_KEY` | Flask 시크릿 키 | ✅ |
| `FLASK_ENV` | 환경 (production/development) | 자동 |

---

## 📂 프로젝트 구조

```
pslr-platform-production/
├── app.py                  # 메인 Flask 애플리케이션
├── models.py               # SQLAlchemy 데이터베이스 모델
├── config.py               # 환경 설정
├── llm_clients.py          # LLM API 클라이언트
├── requirements.txt        # Python 의존성
├── Procfile                # Railway/Heroku 배포용
├── gunicorn.conf.py        # Gunicorn 설정
├── Dockerfile              # Docker 이미지
├── docker-compose.yml      # Docker Compose 설정
├── runtime.txt             # Python 버전
├── .env.example            # 환경 변수 템플릿
├── .gitignore              # Git 무시 파일
└── README.md               # 이 파일
```

---

## 🌍 커스텀 도메인 연결

### Railway에서 커스텀 도메인 추가

1. **도메인 구매**: Namecheap, GoDaddy 등
2. **Railway Dashboard** → Settings → Domains
3. **Add Domain** 클릭
4. **DNS 설정**:
   ```
   Type: CNAME
   Name: pslr (또는 @)
   Value: your-project.up.railway.app
   ```

---

## 🔒 보안 권장사항

1. **API 키 보호**:
   - `.env` 파일을 절대 Git에 커밋하지 마세요
   - `.gitignore`에 `.env` 추가됨 ✅

2. **SECRET_KEY 생성**:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **HTTPS 사용**:
   - Railway/Render는 자동으로 HTTPS 제공 ✅

4. **Rate Limiting** (향후 추가):
   ```bash
   pip install flask-limiter
   ```

---

## 📈 모니터링

### 로그 확인

```bash
# Railway
railway logs

# Render
# Dashboard → Logs 탭

# Docker
docker-compose logs -f web
```

---

## 🐛 트러블슈팅

### 문제: "Database connection failed"
**해결**: `DATABASE_URL` 환경 변수 확인
```bash
echo $DATABASE_URL
```

### 문제: "API key not found"
**해결**: `.env` 파일 또는 Railway 환경 변수 확인

### 문제: "Migration error"
**해결**:
```bash
flask db stamp head
flask db migrate
flask db upgrade
```

---

## 🤝 기여 방법

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📜 라이선스

MIT License

---

## 📞 문의

- 논문: [PSLR Paper v1.0](https://...)
- 이슈: GitHub Issues
- 이메일: [연구자 이메일]

---

## 🎯 다음 단계

- [ ] 논문 arXiv 제출
- [ ] PSLR Scan 웹사이트 별도 구축
- [ ] 사용자 인증 시스템
- [ ] 배치 데이터 수집 자동화
- [ ] 데이터 시각화 대시보드
- [ ] API 문서 자동 생성 (Swagger)

---

**Built with ❤️ by PSLR Research Team**
