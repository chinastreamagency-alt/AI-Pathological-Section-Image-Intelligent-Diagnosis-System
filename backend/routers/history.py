from fastapi import APIRouter, HTTPException
from database import get_db

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("")
async def get_history(page: int = 1, page_size: int = 10):
    """获取诊断历史记录列表"""
    offset = (page - 1) * page_size
    db = await get_db()

    row = await db.execute_fetchall("SELECT COUNT(*) as total FROM diagnoses")
    total = row[0][0]

    rows = await db.execute_fetchall(
        """SELECT id, original_name, image_width, image_height, file_size,
                  question, model_used, created_at
           FROM diagnoses ORDER BY created_at DESC LIMIT ? OFFSET ?""",
        (page_size, offset),
    )
    await db.close()

    items = [
        {
            "id": r[0],
            "original_name": r[1],
            "image_width": r[2],
            "image_height": r[3],
            "file_size": r[4],
            "question": r[5],
            "model_used": r[6],
            "created_at": r[7],
        }
        for r in rows
    ]

    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/{diagnosis_id}")
async def get_diagnosis_detail(diagnosis_id: int):
    """获取单条诊断记录详情"""
    db = await get_db()
    rows = await db.execute_fetchall(
        "SELECT * FROM diagnoses WHERE id = ?", (diagnosis_id,)
    )
    await db.close()

    if not rows:
        raise HTTPException(status_code=404, detail="诊断记录不存在")

    r = rows[0]
    return {
        "id": r[0],
        "filename": r[1],
        "original_name": r[2],
        "file_size": r[3],
        "image_width": r[4],
        "image_height": r[5],
        "question": r[6],
        "image_description": r[7],
        "diagnosis_result": r[8],
        "model_used": r[9],
        "created_at": r[10],
    }
