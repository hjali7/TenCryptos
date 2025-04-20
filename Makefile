# Makefile - TenCryptos 🚀 DevOps Automation

# ========================
# 🌍 GLOBAL VARIABLES
# ========================
COMPOSE=docker compose
PROJECT_NAME=tencryptos

# ========================
# 🚀 MAIN COMMANDS
# ========================

## Run everything from scratch (build + up + scripts)
up: perms compose
	@echo "✅ Project started successfully!"

## Stop and remove all containers
down:
	@$(COMPOSE) down --remove-orphans
	@echo "🛑 All services stopped."

## Rebuild everything cleanly
restart: down up

## Show logs
logs:
	@$(COMPOSE) logs -f --tail=100

## Rebuild only services
rebuild:
	@$(COMPOSE) build --no-cache
	@echo "🔁 Rebuild complete."

# ========================
# 📦 DOCKER COMPOSE
# ========================

compose:
	@$(COMPOSE) up -d --build || (echo '❌ Failed to start containers' && exit 1)

# ========================
# ⚙️ PERMISSIONS
# ========================

## Give execute permissions to scripts
perms:
	@chmod +x scripts/*.sh || true
	@echo "🔐 Permissions set for scripts."

# ========================
# ☁️ AWS + LocalStack Utils
# ========================

## Create CloudWatch logs groups and streams
cloudwatch-logs:
	@echo "📊 Creating CloudWatch Logs..."
	@sh scripts/create_log_groups.sh

## Trigger manual crypto sync
sync:
	@curl -X POST http://localhost:8000/cryptos/update

## Show cryptos in DB (quick test)
show-db:
	@curl http://localhost:8000/cryptos/db | jq

## Test S3/SQS devtools
s3-list:
	@curl http://localhost:8000/devtools/s3/list

sqs-send:
	@curl http://localhost:8000/devtools/sqs/send

sqs-receive:
	@curl http://localhost:8000/devtools/sqs/receive

# ========================
# 🔧 Utility Commands
# ========================

## Remove all docker artifacts (⚠️ CAUTION!)
clean:
	@docker system prune -a --volumes

## Rebuild a single service: make rebuild-svc svc=backend
rebuild-svc:
	@$(COMPOSE) build --no-cache $(svc)

deploy-lambda:
	docker build -t lambda-deployer ./infrastructure/lambda
	docker run --rm \
		--network=tencryptos_net \
		--env-file=./infrastructure/lambda/.env \
		lambda-deployer
		
.PHONY: up down restart logs rebuild compose perms cloudwatch-logs sync show-db s3-list sqs-send sqs-receive clean rebuild-svc


prebuild-go-lambda:
	@echo "🔧 Prebuilding Go Lambda outside Docker..."
	cd infrastructure/go_lambdas/init_updater && \
	chmod +x build.sh && \
	./build.sh

## 🦾 Deploy Go Lambda

go-lambda-updater:	perms
	@echo "🚀 Running Go Lambda Updater container..."
	@docker run --rm \
		--env-file=./infrastructure/go_lambdas/init_updater/.env \
		--network=tencryptos_tencryptos_net \
		-v $(PWD)/scripts:/scripts \
		-v $(PWD)/infrastructure/go_lambdas/init_updater:/lambda \
		go-lambda-updater:1.0.0 \
		/bin/bash /scripts/bootstrap_go_lambdas.sh

## 🔨Build Go Lambda Updater Image

build-go-lambda-updater-image:
	@echo "🚀 Creating Image go-lambda-updater ..."
	@docker build -t go-lambda-updater:1.0.0 ./infrastructure/go_lambdas/init_updater