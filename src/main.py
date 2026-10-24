from fastapi import FastAPI
from src.auth.routes import auth_router
from src.user.routes import user_routes
from src.tasks.routes import task
from src.milestones.routes import milestones_router

app = FastAPI(
    title="Task Management REST API",
    version="1.0.0",
    description="A robust task management REST API built with FastAPI and SQLAlchemy 2.x."
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_routes, prefix="/api/v1")
app.include_router(task, prefix="/api/v1")
app.include_router(milestones_router, prefix="/api/v1")
