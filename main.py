# SFWRTECH 4SA3 - Software Architecture
# CalPal Project
# Jonathan Principato (400527847)

from fastapi import FastAPI
from mangum import Mangum
from routers import employees 

app = FastAPI(title="CalPal API")

# Register routers
app.include_router(employees.router)

@app.get("/")
def root():
    return {"status": "CalPal API is running"}

# AWS Handler
handler = Mangum(app)
