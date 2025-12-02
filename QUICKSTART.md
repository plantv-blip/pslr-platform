# ⚡ PSLR Platform 초간단 배포 (30분)

## 🎯 목표: 30분 안에 라이브 URL 확보

---

## Step 1: 파일 다운로드 (1분)

이미 완료! ✅

---

## Step 2: GitHub 업로드 (5분)

```bash
# 1. GitHub에서 새 저장소 생성
# https://github.com/new
# 이름: pslr-platform

# 2. 터미널에서 실행
cd pslr-platform-production

git init
git add .
git commit -m "PSLR Platform v3.0"
git branch -M main
git remote add origin https://github.com/당신계정명/pslr-platform.git
git push -u origin main
```

---

## Step 3: Railway 배포 (10분)

### 3-1. Railway 가입
https://railway.app → "Login with GitHub"

### 3-2. 프로젝트 생성
1. "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. `pslr-platform` 선택
4. 자동 배포 시작 ✅

### 3-3. PostgreSQL 추가
1. 프로젝트 대시보드에서 "New" 클릭
2. "Database" → "PostgreSQL" 선택
3. 자동 연결 완료 ✅

---

## Step 4: API 키 설정 (5분)

### 4-1. OpenAI API 키 발급
https://platform.openai.com/api-keys
→ "Create new secret key" → 복사

### 4-2. Railway에 환경 변수 추가
1. 앱 서비스 클릭 (PostgreSQL 아님!)
2. "Variables" 탭
3. 다음 추가:

```
OPENAI_API_KEY=sk-proj-당신의키
SECRET_KEY=아무거나-긴-랜덤-문자열-32자-이상
FLASK_ENV=production
```

**SECRET_KEY 생성**:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Step 5: 배포 확인 (5분)

### 5-1. URL 확인
Railway Dashboard → Settings → Public Networking
→ `https://pslr-platform-production-xxx.up.railway.app`

### 5-2. 접속 테스트
브라우저에서 URL 열기

### 5-3. 헬스 체크
```bash
curl https://your-url.up.railway.app/health
```

응답:
```json
{"status":"healthy","database":"connected"}
```

---

## Step 6: 첫 분석 실행 (5분)

1. **브라우저에서 플랫폼 열기**

2. **분석 설정**:
   - Concept: `Love`
   - Model: `GPT-4o`
   - API Key: (OpenAI 키 입력)

3. **"분석 시작" 클릭**

4. **결과 확인**:
   - P, S, L, R 값 표시
   - 3D 구체 업데이트
   - 히스토리에 저장됨 ✅

---

## ✅ 완료!

**축하합니다!** 🎉

이제 다음을 사용할 수 있습니다:
- ✅ 실시간 PSLR 분석
- ✅ PostgreSQL 데이터베이스
- ✅ 라이브 URL
- ✅ HTTPS 자동 적용
- ✅ 분석 히스토리 저장

---

## 🚀 다음 단계

### Option 1: 커스텀 도메인 연결
`pslr.ai` 같은 도메인 구매 후 연결
→ [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#커스텀-도메인-연결) 참고

### Option 2: 다른 모델 추가
Claude, Gemini, DeepSeek 등 추가 API 키 설정

### Option 3: 논문 연동
논문 PDF를 `/paper` 라우트에 연결

---

## 📞 도움이 필요하면?

- **README.md**: 전체 문서
- **DEPLOYMENT_GUIDE.md**: 상세 배포 가이드
- **GitHub Issues**: 문제 보고

---

**Happy Analyzing! 🔮**
