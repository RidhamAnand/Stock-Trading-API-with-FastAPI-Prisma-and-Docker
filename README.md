# Stock Trading API with FastAPI and PostgreSQL



A FastAPI-based Stock Trading API that stores market data in PostgreSQL using Prisma ORM. It provides endpoints for 
retrieving stock data, inserting new records, and evaluating a Moving Average Crossover strategy for generating buy/sell signals. The project is fully containerized using Docker.
## Features


#### Access APIs at http://0.0.0.0:8000/docs
![image](https://github.com/user-attachments/assets/d93e99e5-16b8-42a9-bc89-4c6460d0a0dc)

#### 

- **REST API Endpoints**
  - CRUD operations for stock data
  - Moving Average Crossover Strategy analysis
  - Paginated data retrieval
- **Data Validation**
  - Field-level validation with Pydantic
  - Business logic checks (high > low, etc.)
- **Automated Testing**
  - 90%+ test coverage
  - Input validation tests
  - Strategy calculation verification

## Technologies

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql)
![Prisma](https://img.shields.io/badge/Prisma-4.0+-black?logo=prisma)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue?logo=docker)

## Installation

```bash
# Clone repository
https://github.com/RidhamAnand/Stock-Trading-API-with-FastAPI-Prisma-and-Docker.git
cd Stock-Trading-API-with-FastAPI-Prisma-and-Docker

# Start containers
docker-compose up --build

# API will be available at http://localhost:8000
# PostgreSQL available on port 5432
```

## API Endpoints
### **1. Data Retrieval Endpoint**

#### **GET** `/data`
**Purpose**: Fetch paginated historical stock data from the database  
**Method**: `GET`  
**Authentication**: None  
**Pagination**:
- `limit` (int): Number of records per page (1-1000), default=50
- `offset` (int): Records to skip for pagination, default=0

#### Result

![image](https://github.com/user-attachments/assets/aba2fc26-3bc1-4e06-8dc2-5d2445dcba77)


### **2. Data Creation Endpoint**
#### **POST** '/data'
**Purpose**: Fetch paginated historical stock data from the database
**Method**: `POST`  
**Authentication**: None  
**Validation Rules**:
- All price values (open, high, low, close) must be positive decimals
- high must be ≥ low and ≥ open
- volume must be a positive integer
- timestamp must be in ISO 8601 format

### Request Schema:
```
{
  "timestamp": "string($date-time)",
  "open": "number > 0",
  "high": "number > 0",
  "low": "number > 0",
  "close": "number > 0",
  "volume": "integer > 0"
}

```

### Result
![image](https://github.com/user-attachments/assets/faa8f5c9-d429-4187-a771-06c162adea8a)


### **3. Strategy Analysis Endpoint**
#### **GET** '/strategy/performance'
**Purpose**: Fetch paginated historical stock data from the database
**Method**: `GET`  
**Authentication**: None  
**Data Source**: Requires ```HINDALCO_1D.csv``` file in root directory
**Strategy Logic:**
- Calculate 50-day and 200-day Simple Moving Averages (SMA)
- Generate buy/sell signals:
  - Buy: When SMA50 crosses above SMA200
  - Sell: When SMA50 crosses below SMA200
- Calculate strategy returns and accuracy

#### Result 
![image](https://github.com/user-attachments/assets/9d9c3bcc-f684-465c-8a0c-bd25a96ebe6a)



## Test Coverage

### Comprehensive Testing Strategy

Rigorous testing standards with **92% code coverage** to ensure reliability and correctness. The testing suite includes:

**Key Test Categories**:
1. **Input Validation**
   - Invalid data types for price/volume fields
   - Negative values for prices/volume
   - High < Low and High < Open scenarios
   - Malformed timestamps

2. **Database Operations**
   - Successful record creation
   - Pagination logic verification
   - Duplicate timestamp prevention
   - Bulk data insertion from Excel

3. **Strategy Logic**
   - Correct SMA calculations (50 & 200 periods)
   - Proper buy/sell signal generation
   - Returns calculation accuracy
   - Edge cases (empty dataset, single record)

4. **Error Handling**
   - Missing CSV file handling
   - Invalid CSV format detection
   - Database connection failures
   - Unexpected data types in CSV

```
-------------------------- coverage: platform linux, python 3.10.6-final-0 --------------------------
Name      Stmts   Miss  Cover   Missing
---------------------------------------
main.py     102     18    92%   24, 32, 54-64
---------------------------------------
TOTAL       102     18    92%
```
