# run_api.py
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting the FastAPI-Scrapy Web Server...")
    print("📋 API Documentation will be available at: http://127.0.0.1:8000/docs")
    
    # Configures Uvicorn engine
    # "api:app" means: look inside file 'api.py' for variable 'app'
    uvicorn.run(
        "api:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True  # Automatically updates server when code modifications are saved
    )