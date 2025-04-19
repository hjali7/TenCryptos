.PHONY: up perms compose

# مسیر اسکریپت‌ها
SCRIPTS = scripts/bootstrap_go_lambdas.sh scripts/bootstrap_iam.sh scripts/bootstrap_go_lambda.sh

# 🎯 ست کردن permission اجرا برای اسکریپت‌ها
perms:
	@echo "🔐 Setting script permissions..."
	@chmod +x $(SCRIPTS)

# 🎯 اجرای Docker Compose
compose:
	@echo "🐳 Running Docker Compose..."
	@docker compose up --build -d

# 🎯 اجرای همه با هم
up: perms compose
