# RiskPulse

Automated corporate risk assessment system.

## What is it

The system collects company data, processes it using NLP, and assesses risks. Built on microservices architecture with asynchronous communication via Kafka.

## Technologies

- Python 3.11 + FastAPI
- PostgreSQL for data storage
- Redis for caching
- Kafka for messaging between services
- Docker for deployment

## Services

**Gateway** — entry point, routes requests

**Auth Service** — user registration and authorization

**Company Service** — company management and risk assessment requests

**Collector Service** — collects raw company data

**NLP Service** — processes and classifies events

## How it works

User requests a company risk assessment via API. The request goes to Kafka, where Collector Service picks it up, gathers data, and sends it forward. NLP Service processes this data and saves the results to the database.

---

# RiskPulse

Система автоматической оценки корпоративных рисков компаний.

## Что это

Система собирает данные о компаниях, обрабатывает их с помощью NLP и оценивает риски. Построена на микросервисной архитектуре с асинхронным общением через Kafka.

## Технологии

- Python 3.11 + FastAPI
- PostgreSQL для хранения данных
- Redis для кэширования
- Kafka для обмена сообщениями между сервисами
- Docker для запуска

## Сервисы

**Gateway** — точка входа, маршрутизирует запросы

**Auth Service** — регистрация и авторизация пользователей

**Company Service** — управление компаниями и запросы на оценку рисков

**Collector Service** — собирает сырые данные о компаниях

**NLP Service** — обрабатывает и классифицирует события

## Как работает

Пользователь запрашивает оценку риска компании через API. Запрос попадает в Kafka, где его подхватывает Collector Service, собирает данные и отправляет дальше. NLP Service обрабатывает эти данные и сохраняет результаты в базу.



