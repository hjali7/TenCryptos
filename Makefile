SHELL := /bin/bash
COMPOSE = docker compose

# 🧱
.DEFAULT_GOAL := help

# 📦 
up: perms
	@echo "🔼 Starting containers..."
	@$(COMPOSE) up -d --build || (echo "❌ Failed to start containers" && exit 1)

# 🛑
down:
	@echo "🛑 Stopping containers..."
	@$(COMPOSE) down || (echo "❌ Failed to stop containers" && exit 1)

# 🔄ا
restart: down up

# 🔍 
logs:
	@$(COMPOSE) logs -f --tail=100

# ✅ 
perms:
	@echo "🔧 Fixing permissions for bootstrap scripts..."
	@chmod +x scripts/*.sh || echo "⚠️ Failed to apply script permissions"

# 🆘 
help:
	@echo ""
	@echo "🛠️  Available commands:"
	@echo "   make up        ⬆️  Build & run all services"
	@echo "   make down      ⛔ Stop all services"
	@echo "   make restart   🔁 Restart all services"
	@echo "   make logs      📜 View logs"
	@echo "   make perms     🔑 Fix script permissions"
	@echo ""
