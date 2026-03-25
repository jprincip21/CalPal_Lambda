# SFWRTECH 4SA3 - Software Architecture
# CalPal Project Lambda
# Jonathan Principato (400527847)

from fastapi import FastAPI
from mangum import Mangum
from routers import employees 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CalPal API", redirect_slashes=False)

origins = [
    "https://calpal.jprincip.me",      # For production dashboard
    "http://localhost:3000",           # For local Next.js development
    "http://127.0.0.1:3000",           # For Alternative local address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(employees.router, 
                    prefix="/employees", # All routes in this file start with /employees
                    tags=["Employees"]) # Groups Endpoints in the SwaggerUI auto-generated docs

@app.get("/")
def root():
    return {"status": "CalPal API is running"}

# AWS Handler
handler = Mangum(app)
