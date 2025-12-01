# CloudMart – CSP451 Final Project Submission

## 1. Azure Login and Resource Verification
- Subscription: Seneca College : CSP451NIA – 1001
- Resource group: Student-RG-1887764
- Region: Canada Central
- Resources:
  - Azure Container Instance: cloudmart-app
  - Cosmos DB account: <your-account-name>
  - Log Analytics Workspace: <name>
- Screenshot references:
  - S1 – Container Instance Overview
  - S4–S6 – Cosmos DB containers

## 2. Cosmos DB Setup
- Database name: `cloudmart`
- Containers:
  - `products` (partition key: `/category`)
  - `cart` (partition key: `/user_id`)
  - `orders` (partition key: `/user_id`)
- Sample commands / approach:
  - Products loaded by initialization script on first run
  - Cart & orders created by API calls
- Evidence: screenshots S4–S6

## 3. GitHub Repository and Secrets
- Repo URL: `https://github.com/<your-user>/Cloudmart`
- Secrets configured:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`
  - `AZURE_CREDENTIALS`
  - `COSMOS_ENDPOINT`
  - `COSMOS_KEY`
- Evidence:
  - S7 – Actions tab with green CI/CD runs

## 4. CI/CD Workflow Execution
- `CI - Test & Build`:
  - Runs on push to `main`
  - Steps: lint, tests, docker build
- `CD - Deploy CloudMart to Azure`:
  - Logs in to Azure with service principal
  - Pushes image to Docker Hub
  - Updates Azure Container Instance to latest image
- Evidence:
  - S7 – successful runs
  - (Optional) S9 – workflow run details page

## 5. API Endpoint Testing
Commands executed from Azure Cloud Shell (example):

```bash
curl $BASE_URL/health
curl $BASE_URL/api/v1/products
curl "$BASE_URL/api/v1/products?category=Electronics"
curl $BASE_URL/api/v1/cart
curl -X POST $BASE_URL/api/v1/cart/items -H "Content-Type: application/json" -d '{"user_id":"demo","product_id":"1","quantity":2}'
curl -X POST $BASE_URL/api/v1/orders -H "Content-Type: application/json" -d '{"user_id":"demo"}'
curl $BASE_URL/api/v1/orders
