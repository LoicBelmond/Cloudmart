CloudMart – CSP451 Milestone 3 (Enterprise Cloud Solution)

A simple cloud-native e-commerce application deployed on Microsoft Azure using:

Python FastAPI backend

Static HTML + JS frontend

Docker containerization

GitHub Actions CI/CD

Azure Container Registry (optional)

Azure Container Instances (ACI) runtime

This project demonstrates cloud-native development, containerization, automation, and deployment of a production-style application.

🌐 Live Application (Azure URL)

Replace with your real URL

http://cloudmart1887764.canadacentral.azurecontainer.io/

✅ Features
Backend (FastAPI)

/ serves frontend (index.html)

/health returns API health

/api/v1/products returns in-memory product catalog

/api/v1/orders accepts order creation

Uses in-memory storage (no CosmosDB required for stable deployment)

Frontend

Simple UI built with HTML + JavaScript

Loads products from backend

Allows adding items to cart

Checkout creates orders

CI/CD

Automatic build + push Docker image

Automatic deployment to Azure Container Instances

Full workflow implemented in GitHub Actions (.github/workflows)

🏗 Project Structure
Cloudmart/
│
├── applications/
│   ├── backend/
│   │   ├── app/
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── frontend/
│       └── index.html
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── submission.md
└── README.md

⚙️ How to Run Locally
1️⃣ Install dependencies
pip install -r applications/backend/requirements.txt

2️⃣ Run FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000

3️⃣ Open in browser
http://localhost:8000/
http://localhost:8000/health
http://localhost:8000/api/v1/products

🐳 Build & Run with Docker
Build image
docker build -t cloudmart-api:v1 -f applications/backend/Dockerfile .

Run container
docker run -p 8080:80 cloudmart-api:v1

Test
http://localhost:8080/

🚀 Deploy to Azure
1️⃣ Login
az login

2️⃣ Create Resource Group
az group create --name CloudMart-RG --location canadacentral

3️⃣ Deploy Container
az container create \
  --resource-group CloudMart-RG \
  --name cloudmart-app \
  --image loicbelmond23/cloudmart-api:latest \
  --dns-name-label cloudmart1887764 \
  --ports 80


After deployment:

http://cloudmart1887764.canadacentral.azurecontainer.io/

🔄 CI/CD Pipeline (GitHub Actions)
✔ ci.yml

Builds Docker image

Pushes to Docker Hub

✔ deploy.yml

Connects to Azure using Service Principal

Deploys updated image to ACI

Replaces container instance

Whenever you push to main, the following happens:

CI builds your code

CI pushes new Docker image

CD deploys to Azure

Azure container restarts and hosts new version

📡 API Endpoints
Method	Endpoint	Description
GET	/	Serve frontend
GET	/health	Health check
GET	/api/v1/products	List products
GET	/api/v1/products/{id}	Get product by ID
POST	/api/v1/orders	Create order
GET	/api/v1/orders	List orders
🖼 Required Screenshots (For Milestone Submission)

📌 Add your screenshots under each section.

S1 – Azure Resource Group showing CloudMart resources

(insert screenshot here)

S2 – /health endpoint in browser

(insert screenshot here)

S3 – Running Docker image locally (docker ps)

(insert screenshot here)

S4 – Local backend running at http://localhost:8000

(insert screenshot here)

S5 – Azure Container Instance: Running state

(insert screenshot here)

S6 – Azure Container Instance Logs (Healthy Boot)

(insert screenshot here)

S7 – GitHub Actions CI success (green check)

(insert screenshot here)

S8 – GitHub Actions CD success

(insert screenshot here)

S9 – Docker Hub repository with tags

(insert screenshot here)

S10 – CloudMart frontend home page on Azure

(insert screenshot here)

S11 – Product list loaded from /api/v1/products

(insert screenshot here)

S12 – Cart + Order confirmation flow

(insert screenshot here)

S13 – Cosmos DB (optional) OR explanation why not used

(insert screenshot here)

📘 Submission Requirements

This project satisfies:

✔ Application runs on Azure
✔ CI/CD fully automated
✔ Docker image pushed to Docker Hub
✔ Backend and frontend working
✔ All endpoints working (products, orders, health)
✔ Documentation + required screenshots
✔ Clean folder structure
✔ Deployment reproducible

🧑‍💻 Author

Loic Belmond
Seneca College — CSP451: Enterprise Cloud Solution

🎉 End of README

If you want, I can also:

✅ generate a professional PDF submission
✅ fill your submission.md
✅ create diagrams (architecture, CI/CD flow)
✅ generate captions for screenshots
