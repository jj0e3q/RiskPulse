# RiskPulse – Event-Driven Corporate Risk Scoring Engine (EN)

RiskPulse is a microservice-based, event-driven risk scoring platform designed to showcase production-grade architecture, modular service boundaries, Kafka-driven workflows, shared core libraries, and complete CI/CD automation.

This project demonstrates engineering practices expected from Senior-level backend developers: clean structure, separation of concerns, stateless services, message-based orchestration, validation layers, and a fully reproducible local environment.

---

## 🚀 Platform Overview

RiskPulse is built as an event-driven pipeline:

```
(Client / Postman)
          |
          v
      [Gateway]  ← JWT validation, routing
       /     \
      v       v
  [Auth]    [Company]  -- emits --> (company.score_requested) --> Kafka
                                     |
                                     v
                              [Collector]  -- emits --> (company.data_collected)
                                     |
                                     v
                                PostgreSQL (raw_events)
                                     |
                                     v
                             [NLP Service] -- emits --> (company.signals_ready)
                                     |
                                     v
                                PostgreSQL (normalized_events)
                                     |
                                     v
                            [Scoring Service] → PostgreSQL (company_scores)
```

---

## 🧩 Microservices

### **1. Gateway**
Entry point for all external traffic.
- Performs local JWT validation using shared core library.
- Proxies requests to internal services.
- Injects `X-User-Id` header when communicating with downstream microservices.

### **2. Auth Service**
Handles:
- User registration  
- Login  
- Password hashing via bcrypt  
- Access token creation using `shared/core/jwt.py`  
- Stores users in PostgreSQL  

### **3. Company Service**
Responsible for:
- Company CRUD (BIN + name)
- Publishing `company.score_requested` events to Kafka
- Returning basic company info to Gateway

### **4. Collector Service**
Core responsibilities:
- Consumes `company.score_requested`
- Saves raw events into `raw_events`
- (Optional) Enriches data with external sources
- Publishes `company.data_collected`

### **5. NLP Service**
Responsible for:
- Consuming `company.data_collected`
- Running rule-based NLP signal extraction
- Writing normalized signals to `normalized_events`
- Publishing `company.signals_ready`

### **6. Scoring Service**
Handles:
- Consuming `company.signals_ready`
- Aggregating normalized signals
- Producing a final risk score (0–100)
- Assigning `low | medium | high` risk level
- Exposing score over HTTP:
  - `GET /scores/{company_id}`

---

## 📦 Shared Core Library (`shared/core`)

This project uses a unified shared module to eliminate duplication across microservices:

```
shared/core/
  config.py       – BaseAppSettings (Pydantic)
  jwt.py          – Create & decode JWT
  kafka.py        – Global producer and consumer factory
  events.py       – Pydantic models for Kafka event contracts
  logging.py      – Unified logging formatter
```

All services import the same configuration primitives, JWT logic, event schemas, and Kafka utilities.  
This allows the entire platform to behave as a coherent, well-structured system.

---

## 🛠 Tech Stack

| Category      | Technology     |
|---------------|----------------|
| Language      | Python 3.11    |
| Framework     | FastAPI        |
| Messaging     | Apache Kafka   |
| Database      | PostgreSQL 16  |
| Cache         | Redis 7        |
| Container     | Docker / Compose |
| CI/CD         | GitHub Actions |
| Config        | Pydantic Settings |
| Security      | JWT (HS256)    |
| ORM           | SQLAlchemy 2.0 |

---

## 🐳 Running Locally

### Requirements
- Docker
- Docker Compose
- Free ports: `5432`, `6379`, `9092`, `8000–8003`

### Start the platform:

```bash
git clone https://github.com/jj0e3q/RiskPulse.git
cd RiskPulse
docker-compose up -d --build
```

Verify Gateway:

```
GET http://localhost:8000/health
```

---

## 🧪 Full End-to-End Flow (Postman)

Use the collection: `RiskPulse.postman_collection.json`

### **1. Register**
```
POST /auth/register
{
  "email": "test@example.com",
  "password": "StrongPass123!"
}
```

### **2. Login (save JWT automatically)**
```
POST /auth/login
```

### **3. Create Company**
```
POST /companies
Authorization: Bearer <token>
{
  "bin": "123456789012",
  "name": "Test Company Ltd."
}
```

### **4. Request Score**
Triggers entire Kafka pipeline:
- `company.score_requested`
- `company.data_collected`
- `company.signals_ready`

```
POST /score/request
{
  "bin": "123456789012"
}
```

### **5. Retrieve final score**
```
GET /score/{company_id}
Authorization: Bearer <token>
```

Example response:

```json
{
  "company_id": "4e0b7dba-...",
  "total_score": 78,
  "risk_level": "medium",
  "details": {
    "severity_counts": { "low": 3, "medium": 1 },
    "type_counts": { "general_activity": 4 },
    "events_considered": 4
  },
  "calculated_at": "2025-11-25T..."
}
```

---

## ⚙️ CI/CD (GitHub Actions)

### **ci.yml**
- Ruff linting  
- Black formatting check  
- mypy type checking  
- Syntax validation (`compileall`)  
- Matrix build per service  
- Docker build tests  

### **docker-build.yml**
- Multi-service Docker builds  
- Auto-tagging (semver, SHA)
- Push to GHCR  

### **security-scan.yml**
- `safety` vulnerability scanning for all `requirements.txt`

### **dependency-review.yml**
- GitHub dependency review gate on PRs

Together these workflows enforce quality and create a production-style engineering environment.

---

## 📈 Roadmap

- Replace rule-based NLP with ML models
- Integrate real sources (news, tenders, sanctions lists)
- Add observability (Prometheus, Grafana, OTel)
- Multi-model scoring support per industry
- API keys and rate limiting
- Role-based access control (RBAC)

---

## 📜 License
MIT License (see `LICENSE`)
