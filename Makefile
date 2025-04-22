# Makefile - TenCryptos 🚀 DevOps Automation

# ========================
# 🌍 GLOBAL VARIABLES
# ========================
COMPOSE=docker compose
PROJECT_NAME=tencryptos

# ========================
# 🚀 MAIN COMMANDS
# ========================

## Run full stack
up: perms compose
	@echo "✅ Project started successfully!"

## Stop all
down:
	@$(COMPOSE) down --remove-orphans
	@echo "🛑 All services stopped."

## Restart everything
restart: down up

## Logs
logs:
	@$(COMPOSE) logs -f --tail=100

## Rebuild all
rebuild:
	@$(COMPOSE) build --no-cache
	@echo "🔁 Rebuild complete."

## Rebuild single
rebuild-svc:
	@$(COMPOSE) build --no-cache $(svc)

# ========================
# ⚙️ PERMISSIONS
# ========================
perms:
	@chmod +x scripts/*.sh || true
	@echo "🔐 Permissions set for scripts."

# ========================
# 🐍 PYTHON LAMBDA DEPLOY
# ========================
lambda-deploy:
	docker build -t lambda-deployer ./infrastructure/lambda
	docker run --rm \
		--network=tencryptos_net \
		--env-file=./infrastructure/lambda/.env \
		lambda-deployer

# ========================
# 🦫 GO LAMBDA DEPLOY (Inside Project)
# ========================
go-lambda-up:
	@echo "🚀 Running Go Lambda (internal method)..."
	@/bin/bash scripts/bootstrap_go_lambda.sh

# ========================
# 🐳 GO LAMBDA DEPLOY (Docker way)
# ========================
go-lambda-updater:
	@echo "🚀 Running Go Lambda Updater container..."
	docker build -t go-lambda-updater ./infrastructure/go_lambdas/init_updater
	docker run --rm \
		--env-file=./infrastructure/go_lambdas/init_updater/.env \
		--network=tencryptos_net \
		-v $(PWD)/scripts:/scripts \
		-v $(PWD)/infrastructure/go_lambdas/init_updater:/lambda \
		go-lambda-updater \
		/bin/bash /scripts/bootstrap_go_lambdas.sh

# ========================
# 🧪 TEST UTILS
# ========================
sync:
	@curl -X POST http://localhost:8000/cryptos/update

show-db:
	@curl http://localhost:8000/cryptos/db | jq

s3-list:
	@curl http://localhost:8000/devtools/s3/list

sqs-send:
	@curl http://localhost:8000/devtools/sqs/send

sqs-receive:
	@curl http://localhost:8000/devtools/sqs/receive

cloudwatch-logs:
	@sh scripts/create_log_groups.sh

# ========================
# 🧹 CLEANERS
# ========================
clean:
	@docker system prune -a --volumes

.PHONY: up down restart logs rebuild rebuild-svc perms lambda-deploy go-lambda-up go-lambda-updater sync show-db s3-list sqs-send sqs-receive cloudwatch-logs clean


# ========================
# 🧱 LOCALSTACK COMMANDS
# ========================

## Run LocalStack (standalone from separate docker-compose)
localstack-up:
	@echo "🟢 Starting LocalStack..."
	@docker compose -f docker-compose.localstack.yml up -d
	@sleep 5
	@if [ "$$(docker inspect -f '{{.State.Running}}' localstack 2>/dev/null)" = "true" ]; then \
		echo "✅ LocalStack started successfully!"; \
	else \
		echo "❌ LocalStack failed to start."; \
	fi

localstack-down:
	@echo "🔴 Stopping LocalStack..."
	@docker compose -f docker-compose.localstack.yml down
	@sleep 2
	@if [ "$$(docker inspect -f '{{.State.Running}}' localstack 2>/dev/null)" = "false" ]; then \
		echo "✅ LocalStack stopped successfully!"; \
	else \
		echo "❌ LocalStack failed to stop."; \
	fi

localstack-logs:
	@echo "📜 LocalStack logs:"
	@docker compose -f docker-compose.localstack.yml logs -f --tail=100

localstack-restart:
	@echo "🔄 Restarting LocalStack..."
	@docker compose -f docker-compose.localstack.yml restart
	@sleep 5
	@if [ "$$(docker inspect -f '{{.State.Running}}' localstack 2>/dev/null)" = "true" ]; then \
		echo "✅ LocalStack restarted successfully!"; \
	else \
		echo "❌ LocalStack failed to restart."; \
	fi