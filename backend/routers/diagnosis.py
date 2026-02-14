import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from config import MAX_FILE_SIZE
from database import get_db
from services.image_service import validate_extension, save_upload
from services.ai_service import run_diagnosis

router = APIRouter(prefix="/api/diagnosis", tags=["diagnosis"])


@router.post("")
async def create_diagnosis(
    file: UploadFile = File(...),
    question: str = Form(""),
):
    """上传病理图片并获取AI诊断结果"""
    if not validate_extension(file.filename):
        raise HTTPException(status_code=400, detail="不支持的文件格式，请上传 JPG/PNG/BMP/TIFF/WebP 格式的图片")

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过 20MB 限制")

    # 保存文件
    file_info = save_upload(file_bytes, file.filename)

    # 生成图片基本描述
    image_desc = (
        f"文件名: {file_info['original_name']} | "
        f"尺寸: {file_info['image_width']}x{file_info['image_height']}px | "
        f"大小: {file_info['file_size'] / 1024:.1f}KB"
    )

    # 调用AI诊断
    ai_result = await run_diagnosis(file_info["filepath"], question)

    # 保存到数据库
    db = await get_db()
    cursor = await db.execute(
        """INSERT INTO diagnoses
           (filename, original_name, file_size, image_width, image_height,
            question, image_description, diagnosis_result, model_used)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            file_info["filename"],
            file_info["original_name"],
            file_info["file_size"],
            file_info["image_width"],
            file_info["image_height"],
            question,
            image_desc,
            ai_result["result"],
            ai_result["model"],
        ),
    )
    await db.commit()
    diagnosis_id = cursor.lastrowid
    await db.close()

    return {
        "id": diagnosis_id,
        "image_info": {
            "filename": file_info["filename"],
            "original_name": file_info["original_name"],
            "width": file_info["image_width"],
            "height": file_info["image_height"],
            "size": file_info["file_size"],
            "description": image_desc,
        },
        "question": question,
        "diagnosis": ai_result["result"],
        "model_used": ai_result["model"],
    }
