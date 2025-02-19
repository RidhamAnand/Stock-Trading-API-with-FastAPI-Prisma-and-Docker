# Use Node.js with Debian base
FROM node:18-bullseye AS builder

WORKDIR /app

# Install Python & dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# Install Prisma CLI globally
RUN npm install -g prisma

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Prisma Python adapter
RUN pip install prisma

# Copy the Prisma schema
COPY prisma ./prisma

# Generate Prisma client
RUN prisma generate

# Copy the rest of the FastAPI app
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
