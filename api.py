# api.py
from crochet import setup, run_in_reactor
# 1. Initialize Crochet before starting the FastAPI app.
# This prevents Twisted reactor conflicts.
setup()


import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
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

@run_in_reactor
def run_spider_logic(url: str, job_id: str):
    """
    Executes the Scrapy spider execution asynchronously inside a Crochet executor thread.
    This runs your existing Scrapy pipeline, downloads documents, and bundles them.
    """
    return crawl_runner.crawl(MguSpider, url=url, job_id=job_id)


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
        "job_id": job_id,
        "check_status_and_download": f"http://127.0.0.1:8000/download/{job_id}"
    }


@app.get("/download/{job_id}")
async def download_zip(job_id: str):
    """
    Checks if the background spider finished saving files and packages.
    Serves the ZIP file as a direct browser download when ready.
    """
    expected_zip_path = f"MGU_Archive_{job_id}.zip"
    
    # If the spider is still processing links or writing the zip to disk
    if not os.path.exists(expected_zip_path):
        return {
            "job_id": job_id,
            "status": "In Progress",
            "message": "The spider is still crawling pages or archiving assets. Please pull this endpoint again shortly."
        }
    
    # Send the physical ZIP file back as a stream response to trigger browser saving
    return FileResponse(
        path=expected_zip_path,
        media_type="application/zip",
        filename=f"MGU_Full_Archive_{job_id}.zip"
    )