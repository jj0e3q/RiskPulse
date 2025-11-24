# Kafka Configuration

This directory contains Kafka-related configuration files.

## Topics

Create Kafka topics as needed for your services. Example:

```bash
docker exec -it riskpulse-kafka kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 3 \
  --topic risk-events
```

## List Topics

```bash
docker exec -it riskpulse-kafka kafka-topics --list --bootstrap-server localhost:9092
```

