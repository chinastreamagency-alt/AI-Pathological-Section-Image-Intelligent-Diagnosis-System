import React, { useState } from 'react'
import { Row, Col, Card, Image, message } from 'antd'
import { FileImageOutlined } from '@ant-design/icons'
import ImageUpload from '../components/ImageUpload'
import DiagnosisForm from '../components/DiagnosisForm'
import DiagnosisResult from '../components/DiagnosisResult'
import { submitDiagnosis } from '../services/api'

export default function HomePage() {
  const [fileList, setFileList] = useState([])
  const [previewUrl, setPreviewUrl] = useState(null)
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleFileChange = (newFileList) => {
    setFileList(newFileList)
    setResult(null)
    if (newFileList.length > 0) {
      const file = newFileList[0].originFileObj
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    } else {
      setPreviewUrl(null)
    }
  }

  const handleSubmit = async () => {
    if (fileList.length === 0) {
      message.warning('请先上传病理切片图片')
      return
    }

    setLoading(true)
    setResult(null)

    try {
      const file = fileList[0].originFileObj
      const data = await submitDiagnosis(file, question)
      setResult(data)
      message.success('AI 诊断分析完成')
    } catch (error) {
      const msg = error.response?.data?.detail || '诊断请求失败，请检查网络连接和 API 配置'
      message.error(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Row gutter={24}>
        <Col xs={24} lg={10}>
          <ImageUpload fileList={fileList} onChange={handleFileChange} />
          {previewUrl && (
            <Card
              title={
                <span>
                  <FileImageOutlined style={{ marginRight: 8 }} />
                  图像预览
                </span>
              }
              size="small"
              style={{ marginTop: 16 }}
            >
              <Image
                src={previewUrl}
                alt="病理切片预览"
                style={{ width: '100%', borderRadius: 4 }}
              />
            </Card>
          )}
        </Col>
        <Col xs={24} lg={14}>
          <DiagnosisForm
            question={question}
            onQuestionChange={setQuestion}
            onSubmit={handleSubmit}
            loading={loading}
          />
          <DiagnosisResult result={result} />
        </Col>
      </Row>
    </div>
  )
}
