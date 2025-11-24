# RiskPulse
Automated Corporate Risk Scoring Engine

## Infrastructure

This project uses Docker Compose to manage the following infrastructure services:

- **PostgreSQL** (port 5432) - Main database
- **Redis** (port 6379) - Caching and session storage
- **Kafka** (port 9092) - Message broker
- **Zookeeper** (port 2181) - Kafka coordination

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Make (optional, for convenience commands)

### Starting Infrastructure

```bash
# Start all services
make up
# or
docker-compose up -d

# Check service status
make ps
# or
docker-compose ps

# View logs
make logs
# or
docker-compose logs -f
```

### Stopping Infrastructure

```bash
# Stop all services
make down
# or
docker-compose down

# Stop and remove all data
make clean
# or
docker-compose down -v
```

### Service Access

**PostgreSQL:**
```bash
make postgres-shell
# or
docker exec -it riskpulse-postgres psql -U riskpulse -d riskpulse
```

**Redis:**
```bash
make redis-cli
# or
docker exec -it riskpulse-redis redis-cli
```

**Kafka:**
```bash
make kafka-topics
# or
docker exec -it riskpulse-kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Health Checks

```bash
make health
```

## Project Structure

```
risk-project/
├── infra/              # Infrastructure configuration
│   ├── postgres/       # PostgreSQL initialization scripts
│   ├── kafka/          # Kafka configuration
│   └── redis/          # Redis configuration
├── docker-compose.yml  # Docker Compose configuration
├── Makefile           # Convenience commands
└── README.md          # This file
```

## Environment Variables

Default connection settings (can be overridden via environment variables):

- **PostgreSQL**: `localhost:5432`, user: `riskpulse`, password: `riskpulse`, database: `riskpulse`
- **Redis**: `localhost:6379`
- **Kafka**: `localhost:9092`

## Development

For development, you can create a `.env` file in the root directory to override default settings.
