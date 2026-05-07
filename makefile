.PHONY: build stop clean reset

build:
	docker compose --profile cpu-local up --build -d

stop:
# Stop all containers including ollama
	docker compose --profile cpu-local stop backend ollama-nomic-embed-text pgvector-db pgadmin

clean:
# Wipe pgdata volume, stop and remove all containers (incl. Ollama)
	docker compose --profile cpu-local down -v
	-docker rm -f ollama-nomic-embed-text pgvector-db pgadmin 2>/dev/null || true

reset:
# Reset all containers
	make clean
	sleep 10
	make build
