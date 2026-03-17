check:
    npm run format
    sh .husky/pre-commit


[working-directory: "apps/web"]
run-web:
    npm run dev
    
[working-directory: "apps/api"]
run-api:
    uv run uvicorn app.main:app --reload --port 8000 &

run-db:
    docker compose up -d postgres

run: run-db run-api run-web



# Start Postgres only (API/web on host with DATABASE_URL)
docker-postgres:
    docker compose up -d postgres

# Start full stack (Postgres + API + Web)
docker-up:
    docker compose up -d

docker-down:
    docker compose down

[working-directory: "apps/api"]
test-api:
    uv run pytest

[working-directory: "apps/web"]
test-web:
    npm run test



test: test-api test-web