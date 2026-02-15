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


# 生产模式：服务前端静态文件
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.isdir(FRONTEND_DIST):
    from fastapi.responses import FileResponse

    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="frontend-assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
