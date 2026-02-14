# AI 病理切片智能诊断系统

上传病理切片照片，AI 自动分析并生成诊断报告。支持指定诊断关注方向，获取针对性分析结果。

## 功能

- 上传病理切片图片（JPG/PNG/BMP/TIFF/WebP）
- 图像预览与基本信息展示
- 输入诊断关注方向（病变部位、核心疑问等）
- AI 自动分析切片图像，生成结构化诊断报告
- 诊断记录历史查询

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | React + Ant Design + Vite |
| 后端 | Python FastAPI |
| AI 诊断 | Google Gemini API（免费）/ OpenRouter 免费模型 |
| 数据库 | SQLite |

## 快速开始

### 1. 配置 API Key

```bash
cp .env.example .env
```

编辑 `.env` 文件，至少配置一个 API Key：

- **Gemini API Key**（推荐）：[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- **OpenRouter API Key**（备选）：[https://openrouter.ai/keys](https://openrouter.ai/keys)

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

后端运行在 `http://localhost:8000`

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:3000`

## 使用流程

1. 打开浏览器访问 `http://localhost:3000`
2. 上传病理切片照片
3. （可选）输入诊断关注方向
4. 点击「提交诊断」，等待 AI 分析
5. 查看诊断报告

## 免责声明

本系统提供的分析结果仅为 AI 辅助参考意见，不可替代专业病理医师的诊断。最终诊断请以具有资质的病理医师意见为准。
