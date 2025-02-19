from fastapi import FastAPI, HTTPException,Query
from pydantic import BaseModel, validator, Field
from prisma import Prisma
from decimal import Decimal
from datetime import datetime
import pandas as pd
from typing import List, Optional
from InsertIntoDB import insert_data_from_excel
import os   

prisma = Prisma()

class StockDataIn(BaseModel):
    timestamp: datetime = Field(..., description="Stock data timestamp", example="2024-02-19T10:30:00")
    open: Decimal = Field(..., gt=0, example=100.50)
    high: Decimal = Field(..., gt=0, example=105.75)
    low: Decimal = Field(..., gt=0, example=98.25)
    close: Decimal = Field(..., gt=0, example=103.00)
    volume: int = Field(..., gt=0, example=10000)

    @validator('high')
    def check_high(cls, v, values):
        if 'low' in values and v < values['low']:
            raise ValueError("High cannot be lower than low")
        if 'open' in values and v < values['open']:
            raise ValueError("High cannot be lower than open")
        return v

    @validator('low')
    def check_low(cls, v, values):
        if 'high' in values and v > values['high']:
            raise ValueError("Low cannot be greater than high")
        return v

class StockDataResponse(BaseModel):
    id: int
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

class StrategyPerformanceResponse(BaseModel):
    total_returns: float
    accuracy: float
    buy_signals: List[datetime]
    sell_signals: List[datetime]

app = FastAPI(title="Stock Trading API", version="1.0.0")

@app.on_event("startup")
async def startup():
    await prisma.connect()
    try:
        count = await prisma.marketdata.count()
        if(count<=0):
            file_path = "HINDALCO_1D.xlsx"  
            await insert_data_from_excel(file_path)
        else:
            print("Table already contains data. Skipping insertion.")
            return
    except Exception as e:
        print(f"Error checking table data: {e}")


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/data", response_model=List[StockDataResponse])
async def get_all_data(
    limit: Optional[int] = Query(50, ge=1, le=1000, description="Max records to return"),
    offset: Optional[int] = Query(0, ge=0, description="Records to skip")
):
    try:
        stock_data = await prisma.marketdata.find_many(
            take=limit,
            skip=offset,
            
        )
        return stock_data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


@app.post("/data", response_model=StockDataResponse)
async def create_stock_data(data: StockDataIn):
    try:
        stock_data = await prisma.marketdata.create(
            data={
                "datetime": data.timestamp,
                "open": float(data.open),
                "high": float(data.high),
                "low": float(data.low),
                "close": float(data.close),
                "volume": data.volume
            }
        )
        return stock_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating record: {str(e)}")

@app.get("/strategy/performance", response_model=StrategyPerformanceResponse)
async def get_strategy_performance():
    try:
        if not os.path.exists("HINDALCO_1D.csv"):
            raise HTTPException(status_code=404, detail="CSV file not found")

        data = pd.read_csv("HINDALCO_1D.csv")

        if data.empty:
            raise HTTPException(status_code=404, detail="CSV file is empty")

        required_columns = {'datetime', 'close'}
        if not required_columns.issubset(data.columns):
            raise HTTPException(status_code=400, detail=f"Missing required columns: {required_columns - set(data.columns)}")

        data['SMA50'] = data['close'].rolling(window=50, min_periods=1).mean()
        data['SMA200'] = data['close'].rolling(window=200, min_periods=1).mean()

        data['Signal'] = 0
        data.loc[50:, 'Signal'] = (data.loc[50:, 'SMA50'] > data.loc[50:, 'SMA200']).astype(int)
        data['Position'] = data['Signal'].diff()

        data['Returns'] = data['close'].pct_change()
        data['StrategyReturns'] = data['Returns'] * data['Position'].shift(1)

        data = data.fillna(0)

        strategy_accuracy = (data['Position'].diff() == data['Returns'].shift(-1)).mean()
        total_returns = data['StrategyReturns'].sum()

        buy_signal_times = data.loc[data['Position'] == 1, 'datetime'].tolist()
        sell_signal_times = data.loc[data['Position'] == -1, 'datetime'].tolist()

        return StrategyPerformanceResponse(
            total_returns=round(total_returns * 100, 2),
            accuracy=round(strategy_accuracy * 100, 2),
            buy_signals=buy_signal_times,
            sell_signals=sell_signal_times
        )

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=404, detail="CSV file is empty")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV file format")
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error calculating strategy performance: {str(e)}"
        )
