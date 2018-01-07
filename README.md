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
  - `docker-compose.dev.yml` : local development environment (DEBUG mode)
  - `docker-compose.alpha.yml` : remote test environment
  - `docker-compose.yml` : production environment

## Django apps
  - public
    - 블로그 (`/blog`)
    - 위키 (`/wiki`)
    - 스토리지 (구. media, `/storage`)
  - private
    - 가계부
