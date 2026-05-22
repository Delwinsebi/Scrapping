# api.py
from crochet import setup, run_in_reactor
# 1. Initialize Crochet before starting the FastAPI app.
# This prevents Twisted reactor conflicts.
setup()

import uvicorn
import os
import uuid
from fastapi import FastAPI, HTTPException
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

# IMPORT YOUR SPIDER HERE
# Make sure your crawler folder name matches 'harvester_core'
from harvester_core.spiders.mgu_portal import MguSpider



app = FastAPI(
    title="Universal Crawler API",
    description="FastAPI wrapper for running Scrapy spiders asynchronously and downloading assets.",
    version="1.0.0"
)

# 2. Load standard settings configured in harvester_core/settings.py
crawl_runner = CrawlerRunner(get_project_settings())

job_status = {}

@run_in_reactor
def run_spider_logic(url: str, job_id: str):
    """
    Executes the Scrapy spider execution asynchronously inside a Crochet executor thread.
    This runs your existing Scrapy pipeline, downloads documents, and bundles them.
    """
    job_status[job_id] = {"finished": False, "status": "running"}

    deferred = crawl_runner.crawl(MguSpider, url=url, job_id=job_id)

    def mark_done(result):
        job_status[job_id] = {"finished": True, "status": "completed"}
        return result

    def mark_failed(failure):
        job_status[job_id] = {
            "finished": True,
            "status": "failed",
            "error": str(failure.value)
        }
        return failure

    deferred.addCallbacks(mark_done, mark_failed)
    return deferred


@app.get("/")
async def root():
    return {"status": "API is online", "docs_url": "/docs"}


@app.post("/crawl")
async def trigger_crawl(target_url: str):
    """
    Triggers the universal crawler spider for a specific URL.
    Returns immediately with a unique job ID.
    """
    if not target_url:
        raise HTTPException(status_code=400, detail="Missing target_url query parameter.")
        
    # Generate a unique 8-character string to isolate separate client requests
    job_id = str(uuid.uuid4())[:8] 
    
    # Hand off execution to the background worker thread
    run_spider_logic(target_url, job_id)
    
    return {
        "status": "Crawl started successfully in background",
        "job_id": job_id
    }

@app.get("/crawl/{job_id}")
async def crawl_status(job_id: str):
    status = job_status.get(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Unknown job_id")
    return {"job_id": job_id, **status}


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