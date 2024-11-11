compose-up:
	docker compose up -d --build ${container}

compose-down:
	docker compose down ${container}
	
compose-down-force:
	docker compose down -v --remove-orphans ${container}

compose-logs:
	docker compose logs -f ${container}

replica-init:
	docker exec -it dev-mongo1-1 bash -c "./docker-entrypoint-initdb.d/init-replica.sh"
	
mongo-shell:
	docker exec -it dev-mongo1-1 mongosh "mongodb://se:P%40ssw0rd1%21@mongo1:27017/admin?authSource=admin&replicaSet=rs0&retryWrites=true&w=majority&readPreference=primary&connectTimeoutMS=5000&socketTimeoutMS=5000"
	
redis-cli:
	docker exec -it dev-redis-1 redis-cli
	
install-poetry:
	docker exec -it dev-poetry-1 poetry install --no-root
	
python:
	docker exec -it dev-poetry-1 poetry run python3 $(file)
	
denormalize:
	docker exec -it dev-poetry-1 poetry run python3 src/libs/DAL/to_json.py
	
inject-redis:
	docker exec -it dev-poetry-1 poetry run python3 src/libs/DAL/inject_new_data_to_redis.py
	
inject-mongo:
	docker exec -it dev-poetry-1 poetry run python3 src/libs/DAL/inject_new_data_to_mongo.py
	
remove-pycache:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	
remove-pytest-cache:
	find . -name ".pytest_cache" -type d -exec rm -rf {} +