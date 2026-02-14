import base64
import httpx
from openai import AsyncOpenAI
from config import GEMINI_API_KEY, OPENROUTER_API_KEY
from services.image_service import image_to_base64, get_mime_type

SYSTEM_PROMPT = """你是一位资深的AI病理学辅助诊断助手。用户将上传病理切片的显微镜照片，并可能提出具体的诊断关注方向。

请按照以下结构进行分析和回复：

## 影像基本信息
简要描述图像的基本特征（染色类型、放大倍数估计、组织类型等）。

## 组织形态学分析
详细描述观察到的组织学特征，包括：
- 细胞形态与排列
- 细胞核特征（大小、形状、染色质、核仁）
- 细胞质特征
- 组织结构与构架
- 间质特征

## 病变特征识别
列出识别到的异常或病变特征：
- 异型性表现
- 增殖活性
- 浸润模式
- 特殊结构（如腺体、乳头状、实性巢状等）
- 其他显著特征

## AI辅助诊断意见
基于以上分析，给出：
1. 最可能的诊断（附置信度评估）
2. 需要鉴别诊断的疾病
3. 建议进一步检查（如免疫组化、分子检测等）

## 重要提示
此分析仅为AI辅助参考意见，不可替代专业病理医师的诊断。最终诊断请以具有资质的病理医师意见为准。

请使用专业但易懂的中文进行回复。如果用户提出了具体问题，请优先围绕该问题进行分析。"""


async def diagnose_with_gemini(image_path: str, question: str) -> dict:
    """使用 Google Gemini API 进行诊断（免费）"""
    b64_image = image_to_base64(image_path)
    mime_type = get_mime_type(image_path)

    user_content = "请分析这张病理切片图像。"
    if question.strip():
        user_content += f"\n\n用户关注重点：{question}"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": b64_image,
                        }
                    },
                    {"text": user_content},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 4096,
        },
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return {"result": text, "model": "gemini-2.5-flash"}


async def diagnose_with_openrouter(image_path: str, question: str) -> dict:
    """使用 OpenRouter 免费模型进行诊断（备用）"""
    b64_image = image_to_base64(image_path)
    mime_type = get_mime_type(image_path)

    user_content_parts = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{b64_image}"},
        },
        {"type": "text", "text": "请分析这张病理切片图像。"},
    ]
    if question.strip():
        user_content_parts.append(
            {"type": "text", "text": f"用户关注重点：{question}"}
        )

    client = AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    response = await client.chat.completions.create(
        model="qwen/qwen3-vl-8b:free",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content_parts},
        ],
        temperature=0.3,
        max_tokens=4096,
    )

    text = response.choices[0].message.content
    return {"result": text, "model": "qwen3-vl-8b (OpenRouter Free)"}


async def run_diagnosis(image_path: str, question: str) -> dict:
    """执行AI诊断，优先Gemini，失败则用OpenRouter"""
    # 优先使用 Gemini（免费且效果好）
    if GEMINI_API_KEY:
        try:
            return await diagnose_with_gemini(image_path, question)
        except Exception as e:
            print(f"Gemini 调用失败: {e}")

    # 备用：OpenRouter 免费模型
    if OPENROUTER_API_KEY:
        try:
            return await diagnose_with_openrouter(image_path, question)
        except Exception as e:
            print(f"OpenRouter 调用失败: {e}")

    return {
        "result": "错误：未配置有效的 API Key。请在 .env 文件中设置 GEMINI_API_KEY 或 OPENROUTER_API_KEY。",
        "model": "none",
    }
