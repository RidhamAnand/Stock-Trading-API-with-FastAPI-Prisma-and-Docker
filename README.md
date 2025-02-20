# Stock Trading API with FastAPI and PostgreSQL

A robust, containerized FastAPI-based Stock Trading API that leverages PostgreSQL for market data storage and Prisma ORM for database operations. The API provides comprehensive endpoints for stock data management and implements a Moving Average Crossover strategy for trading signals.

## 🚀 Access APIs
Access the APIs at http://0.0.0.0:8000/docs

![Swagger UI](https://github.com/user-attachments/assets/d93e99e5-16b8-42a9-bc89-4c6460d0a0dc)

## 🛠️ Key Features

| Category | Features |
|----------|----------|
| API Endpoints | • CRUD operations for stock data<br>• Moving Average Crossover Strategy analysis<br>• Paginated data retrieval |
| Data Validation | • Field-level validation with Pydantic<br>• Business logic checks (high > low, etc.) |
| Testing | • 90%+ test coverage<br>• Input validation tests<br>• Strategy calculation verification |

## 📦 Technology Stack

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql)
![Prisma](https://img.shields.io/badge/Prisma-4.0+-black?logo=prisma)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue?logo=docker)

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/RidhamAnand/Stock-Trading-API-with-FastAPI-Prisma-and-Docker.git
cd Stock-Trading-API-with-FastAPI-Prisma-and-Docker

# Start containers
docker-compose up --build

# Access points:
# API: http://localhost:8000
# PostgreSQL: port 5432
```

## 🔌 API Endpoints

### 1. Data Retrieval (`GET /data`)

#### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| limit | integer | Records per page (1-1000) | 50 |
| offset | integer | Records to skip | 0 |

#### Result
![Data Retrieval Result](https://github.com/user-attachments/assets/aba2fc26-3bc1-4e06-8dc2-5d2445dcba77)

### 2. Data Creation (`POST /data`)

#### Request Schema

| Field | Type | Validation Rules |
|-------|------|-----------------|
| timestamp | string | ISO 8601 format |
| open | number | > 0 |
| high | number | > 0, ≥ low, ≥ open |
| low | number | > 0 |
| close | number | > 0 |
| volume | integer | > 0 |

```json
{
  "timestamp": "string($date-time)",
  "open": "number > 0",
  "high": "number > 0",
  "low": "number > 0",
  "close": "number > 0",
  "volume": "integer > 0"
}
```

#### Result
![Data Creation Result](https://github.com/user-attachments/assets/faa8f5c9-d429-4187-a771-06c162adea8a)

### 3. Strategy Analysis (`GET /strategy/performance`)

#### Features

- Calculates 50-day and 200-day Simple Moving Averages (SMA)
- Generates trading signals:
  - Buy: SMA50 crosses above SMA200
  - Sell: SMA50 crosses below SMA200
- Provides strategy performance metrics

#### Results
![Strategy Analysis Result 1](https://github.com/user-attachments/assets/9d9c3bcc-f684-465c-8a0c-bd25a96ebe6a)
![Strategy Analysis Result 2](https://github.com/user-attachments/assets/9c9f554a-13df-492d-935a-baed8033c6f4)

## 🧪 Test Coverage Report

Current coverage: **92%**

| Test Category | Areas Covered |
|--------------|---------------|
| Input Validation | • Data type validation<br>• Price/volume negativity checks<br>• Price relationship validation<br>• Timestamp format verification |
| Database Operations | • Record creation<br>• Pagination testing<br>• Duplicate prevention<br>• Bulk data handling |
| Strategy Logic | • SMA calculations<br>• Signal generation<br>• Returns calculation<br>• Edge case handling |
| Error Handling | • File handling<br>• CSV format validation<br>• Database connection<br>• Data type management |

```plaintext
-------------------------- coverage: platform linux, python 3.10.6-final-0 --------------------------
Name      Stmts   Miss  Cover   Missing
---------------------------------------
main.py     102     18    92%   24, 32, 54-64
---------------------------------------
TOTAL       102     18    92%
```
