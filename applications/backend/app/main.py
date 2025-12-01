from fastapi import FastAPI

app = FastAPI(title="CloudMart API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "CloudMart backend is running on Azure"}
