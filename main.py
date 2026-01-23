from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta, timezone 
import uuid
import os
import secrets

from dotenv import load_dotenv
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Load enviroment variables from .env ( for local dev / simple deploys )
load_dotenv()


app = FastAPI()

# Mount static files (for CSS etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# In-memory storage for requests (for demo / MVP)
PINGS: List[dict] = []
PING_TTL_MINUTES = 30 # auto-expire after 30 minutes

# --- Driver auth configuration ---

DRIVER_USERNAME = os.getenv("DRIVER_USERNAME", "driver")
DRIVER_PASSWORD = os.getenv("DRIVER_PASSWORD", "changeme")

if not DRIVER_PASSWORD:
    print(
        "WARNING: DRIVER_PASSWORD is not set. Using default 'changeme'."
        "Set DRIVER_USERNAME and DRIVER_PASSWORD in your .env file."
    )
security = HTTPBasic()

def require_driver(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Simple HTTP Basic Auth for driver-only endpoints.
    Broswer will prompt for username and password the first
    """
    correct_username = secrets.compare_digest(credentials.username, DRIVER_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, DRIVER_PASSWORD)
    if not (correct_username and correct_password):
        # Trigger browser login diaglog again
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True
        





class PingCreate(BaseModel):
    name: str
    latitude: float
    longitude: float


def cleanup_expired():
    global PINGS
    now = datetime.now(timezone.utc)
    PINGS = [p for p in PINGS if p["created_at"] > now - timedelta(minutes=PING_TTL_MINUTES)] # checks for pings from now and 30 mins ago.


@app.get("/", response_class=HTMLResponse)
async def root():
    # Redirect to driver page as default homepage
    return RedirectResponse(url="/driver")


@app.get("/rider", response_class=HTMLResponse)
async def rider_page(request: Request):
    return templates.TemplateResponse("rider.html", {"request": request})


@app.get("/driver", response_class=HTMLResponse)
async def driver_page(
    request: Request,
    _: bool = Depends(require_driver), # ADDED: requires basic auth for drivers.

):
    return templates.TemplateResponse("driver.html", {"request": request})
    


@app.post("/api/ping")
async def create_ping(ping: PingCreate):
    cleanup_expired()
    ping_id = str(uuid.uuid4())
    new_ping = {
        "id": ping_id,
        "name": ping.name,
        "latitude": ping.latitude,
        "longitude": ping.longitude,
        "created_at": datetime.now(timezone.utc),
    }
    PINGS.append(new_ping)
    return {"status": "ok", "id": ping_id}


@app.get("/api/requests")
async def list_pings(
    _:bool = Depends(require_driver)
):
    """Return active pickup requests to the driver dashboard."""
    cleanup_expired()
    return [
        {
            **p,
            "created_at": p["created_at"].isoformat(),
        }
        for p in PINGS
    ]

@app.post("/api/complete")
async def complete_ping(
    ping_id: str = Form(...),
    _: bool = Depends(require_driver)  # Endpoint: protected
):
    """Driver marks pickup completed → remove it."""
    global PINGS
    PINGS = [p for p in PINGS if p["id"] != ping_id]
    return {"status": "ok"}

    



   
