---
description: How to start the stock prediction backend and frontend
---

# Start Stock Prediction System

// turbo-all

## Backend

1. Start the FastAPI backend server:
```
python -m uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
```
Run from `c:\stock_prediction_system`.

## Frontend

2. Start the Vite dev server:
```
npm run dev
```
Run from `c:\stock_prediction_system\frontend`.

## Access

- Backend API: http://localhost:8000/docs
- Frontend Dashboard: http://localhost:5173
