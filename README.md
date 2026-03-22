# CalPal API Deployment

## 1. Project Setup

Create the core application structure:

```bash
calpal-api/
│── main.py
│── database.py
│── routers/
│ ├── init.py
│ └── <your_route_files>.py
```

- `main.py` → Entry point (FastAPI app + Mangum handler)
- `database.py` → Database connection logic
- `routers/` → API route modules

---

## 2. Deployment Package

Create a dist/ folder and copy your code files and folders into it.

## 3. Install Dependencies

Run 
```bash
pip install fastapi mangum mysql-connector-python -t dist/ to bundle libraries.
```
## 4. Compress
Select all files inside the `dist/` folder and compress them into a single .zip file.

## 5. Create Lambda
Use Python runtime and x86_64 architecture in the AWS Lambda Console.

## 6. Upload
Upload your .zip file via the "Code" tab in the Lambda dashboard.

## 7. Set Handler
Change the Runtime Setting "Handler" to main.handler so AWS can find your code.

## 8. Secure Config
Add DB_HOST, DB_USER, DB_PASS, and DB_NAME to Lambda Environment Variables.

## 9. Networking
Configure the Lambda VPC or Security Group to allow outbound traffic to your RDS on port 3306.

# 10. Expose API
Create an AWS API Gateway (HTTP API) and point a `$default` or `/{proxy+}` route to your Lambda.