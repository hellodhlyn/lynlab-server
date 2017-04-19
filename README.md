# lynlab
## Deploy & Run
### Requirements
  - git
  - docker-compose

### Setup
```
# 레포지토리 Clone
git clone https://github.com/HelloDHLyn/lynlab.git

# 설정 변수 세팅
vim project/settings/settings_var.py

# Docker 실행
docker-compose up -d
```

### docker profiles
  - `docker-compose.yml` : production environment
  - `docker-compose.alpha.yml` : remote test environment
  - `docker-compose.dev.yml` : local development environment (DEBUG mode)

## Django apps
  - blog
  - media
  - wiki (*개선 작업 진행중, 현재는 기존 문서를 readonly로 제공*)