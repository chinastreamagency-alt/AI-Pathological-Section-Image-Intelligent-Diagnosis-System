import React from 'react'
import { Card, Descriptions, Tag, Divider, Typography } from 'antd'
import { CheckCircleOutlined, RobotOutlined } from '@ant-design/icons'
import ReactMarkdown from 'react-markdown'

const { Text } = Typography

export default function DiagnosisResult({ result }) {
  if (!result) return null

  const { image_info, question, diagnosis, model_used } = result

  return (
    <div style={{ marginTop: 24 }}>
      <Card
        title={
          <span>
            <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
            影像基本信息
          </span>
        }
        size="small"
      >
        <Descriptions column={2} size="small">
          <Descriptions.Item label="文件名">{image_info.original_name}</Descriptions.Item>
          <Descriptions.Item label="图像尺寸">
            {image_info.width} x {image_info.height} px
          </Descriptions.Item>
          <Descriptions.Item label="文件大小">
            {(image_info.size / 1024).toFixed(1)} KB
          </Descriptions.Item>
          <Descriptions.Item label="诊断模型">
            <Tag color="blue">{model_used}</Tag>
          </Descriptions.Item>
        </Descriptions>
        {question && (
          <>
            <Divider style={{ margin: '12px 0' }} />
            <Text type="secondary">关注方向：</Text>
            <Text strong>{question}</Text>
          </>
        )}
      </Card>

      <Card
        title={
          <span>
            <RobotOutlined style={{ color: '#1677ff', marginRight: 8 }} />
            AI 诊断分析报告
          </span>
        }
        size="small"
        style={{ marginTop: 16 }}
        className="diagnosis-report"
      >
        <div className="markdown-body">
          <ReactMarkdown>{diagnosis}</ReactMarkdown>
        </div>
      </Card>
    </div>
  )
}
