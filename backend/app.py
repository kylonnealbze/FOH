"""
FOH Coral Reef Monitoring API
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .database import engine, Base

# Import all route modules
from .routes import sites, photomosaics, outplanting, temperature, surveys, spatial

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS - IMPORTANT for PHP application on Hostgator to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + [
        "*"  # Allow all origins for now - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(sites.router)
app.include_router(photomosaics.router)
app.include_router(outplanting.router)
app.include_router(temperature.router)
app.include_router(surveys.router)
app.include_router(spatial.router)


@app.get("/", summary="API Root")
def root():
    """
    API root endpoint - provides basic information and links
    """
    return {
        "message": "FOH Coral Reef Monitoring API",
        "version": settings.API_VERSION,
        "documentation": "/api/docs",
        "endpoints": {
            "sites": "/api/sites",
            "photomosaics": "/api/photomosaics",
            "outplanting": "/api/outplanting",
            "temperature": "/api/temperature",
            "surveys": "/api/surveys",
            "spatial": "/api/spatial"
        }
    }


@app.get("/api/health", summary="Health Check")
def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy", "message": "API is running"}


@app.on_event("startup")
async def startup_event():
    """
    Startup event - initialize database connection
    """
    print("=" * 60)
    print(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    print(f"Database: {settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event - cleanup
    """
    print("Shutting down API...")


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unexpected errors
    """
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
