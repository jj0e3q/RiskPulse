# Redis Configuration

Redis is used for caching and session storage.

## Connection

- Host: `localhost`
- Port: `6379`
- No password by default (for development)

## Usage Examples

### Using redis-cli

```bash
docker exec -it riskpulse-redis redis-cli
```

### Python Example

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('key', 'value')
print(r.get('key'))
```

