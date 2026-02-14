import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import init_db
from config import UPLOAD_DIR
from routers import diagnosis, history


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield


app = FastAPI(
    title="AI病理切片智能诊断系统",
    description="上传病理切片图像，获取AI辅助诊断结果",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(diagnosis.router)
app.include_router(history.router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "AI病理切片智能诊断系统运行中"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
