import React from 'react'
import { Input, Button, Card, Space, Alert } from 'antd'
import { SendOutlined, ClearOutlined } from '@ant-design/icons'

const { TextArea } = Input

const EXAMPLE_QUESTIONS = [
  '请重点分析是否存在恶性肿瘤特征',
  '请关注细胞异型性和核分裂象',
  '请评估肿瘤浸润深度和分级',
  '请分析是否为炎性病变，排除肿瘤可能',
]

export default function DiagnosisForm({ question, onQuestionChange, onSubmit, loading }) {
  return (
    <Card title="诊断关注方向" size="small" style={{ marginTop: 16 }}>
      <TextArea
        rows={3}
        value={question}
        onChange={(e) => onQuestionChange(e.target.value)}
        placeholder="请输入您需要重点关注的诊断方向、病变部位或核心疑问（可留空，系统将进行全面分析）"
        maxLength={500}
        showCount
        disabled={loading}
      />
      <div style={{ marginTop: 8 }}>
        <Space wrap size={[4, 4]}>
          {EXAMPLE_QUESTIONS.map((q, i) => (
            <Button
              key={i}
              size="small"
              type="dashed"
              onClick={() => onQuestionChange(q)}
              disabled={loading}
            >
              {q}
            </Button>
          ))}
        </Space>
      </div>
      <div style={{ marginTop: 16, display: 'flex', gap: 8 }}>
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={onSubmit}
          loading={loading}
          size="large"
          block
        >
          {loading ? 'AI 正在分析中...' : '提交诊断'}
        </Button>
        {!loading && (
          <Button
            icon={<ClearOutlined />}
            onClick={() => onQuestionChange('')}
            size="large"
          >
            清空
          </Button>
        )}
      </div>
      {loading && (
        <Alert
          message="AI 正在分析病理切片图像，这可能需要 10-30 秒，请耐心等待..."
          type="info"
          showIcon
          style={{ marginTop: 12 }}
        />
      )}
    </Card>
  )
}
