check:
    npm run format
    sh .husky/pre-commit

run:
    npm run dev

# Start Postgres only (API/web on host with DATABASE_URL)
docker-postgres:
    docker compose up -d postgres

# Start full stack (Postgres + API + Web)
docker-up:
    docker compose up -d

docker-down:
    docker compose down