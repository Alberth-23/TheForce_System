from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from app.api import auth, endpoints
from app.core.config import settings
from jose import jwt, JWTError
from fastapi.responses import RedirectResponse

app = FastAPI(title=settings.PROJECT_NAME)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Middleware to check authentication from cookies
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Public paths
    if request.url.path in ["/login", "/logout", "/static", "/favicon.ico"] or request.url.path.startswith("/static"):
        return await call_next(request)
    
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    try:
        # Bearer <token>
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except (JWTError, IndexError):
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    return await call_next(request)

# Include routers
app.include_router(auth.router)
app.include_router(endpoints.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)