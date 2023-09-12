up:
	docker compose -f notification.local.yml --profile notification up -d --build

down:
	docker compose -f notification.local.yml --profile notification down

