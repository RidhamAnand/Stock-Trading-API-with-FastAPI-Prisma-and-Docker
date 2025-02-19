import pandas as pd
from prisma import Prisma
from decimal import Decimal

# Initialize Prisma Client
prisma = Prisma()

async def connect_to_db():
    await prisma.connect()

async def disconnect_from_db():
    await prisma.disconnect()

# Function to insert data into the database
async def insert_data_from_excel(file_path: str):
    df = pd.read_excel(file_path)

    await connect_to_db()

    for _, row in df.iterrows():
        try:
            data = {
                "datetime": row["datetime"],
                "close": Decimal(row["close"]),
                "high": Decimal(row["high"]),
                "low": Decimal(row["low"]),
                "open": Decimal(row["open"]),
                "volume": int(row["volume"])
            }
            await prisma.marketdata.create(data=data)
            print(f"Inserted data for {row['datetime']} into the database.")
        except Exception as e:
            print(f"Error inserting data for {row['datetime']}: {e}")

    await disconnect_from_db()

    
