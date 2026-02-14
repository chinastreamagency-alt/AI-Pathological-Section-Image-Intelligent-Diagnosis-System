import React, { useState, useEffect } from 'react'
import { Table, Tag, Modal, Card, Typography, message } from 'antd'
import { HistoryOutlined, RobotOutlined } from '@ant-design/icons'
import ReactMarkdown from 'react-markdown'
import { getHistory, getDiagnosisDetail } from '../services/api'

const { Text } = Typography

export default function HistoryPage() {
  const [data, setData] = useState({ items: [], total: 0 })
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [detail, setDetail] = useState(null)
  const [modalOpen, setModalOpen] = useState(false)

  const fetchHistory = async (p) => {
    setLoading(true)
    try {
      const res = await getHistory(p, 10)
      setData(res)
    } catch {
      message.error('获取诊断记录失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchHistory(page)
  }, [page])

  const showDetail = async (id) => {
    try {
      const res = await getDiagnosisDetail(id)
      setDetail(res)
      setModalOpen(true)
    } catch {
      message.error('获取诊断详情失败')
    }
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      width: 60,
    },
    {
      title: '文件名',
      dataIndex: 'original_name',
      ellipsis: true,
    },
    {
      title: '图像尺寸',
      render: (_, r) => `${r.image_width}x${r.image_height}`,
      width: 120,
    },
    {
      title: '关注方向',
      dataIndex: 'question',
      ellipsis: true,
      render: (q) => q || <Text type="secondary">全面分析</Text>,
    },
    {
      title: '模型',
      dataIndex: 'model_used',
      width: 160,
      render: (m) => <Tag color="blue">{m}</Tag>,
    },
    {
      title: '时间',
      dataIndex: 'created_at',
      width: 170,
    },
    {
      title: '操作',
      width: 80,
      render: (_, r) => (
        <a onClick={() => showDetail(r.id)}>查看</a>
      ),
    },
  ]

  return (
    <div>
      <Card
        title={
          <span>
            <HistoryOutlined style={{ marginRight: 8 }} />
            诊断记录
          </span>
        }
      >
        <Table
          columns={columns}
          dataSource={data.items}
          rowKey="id"
          loading={loading}
          pagination={{
            current: page,
            total: data.total,
            pageSize: 10,
            onChange: setPage,
            showTotal: (total) => `共 ${total} 条记录`,
          }}
          size="small"
        />
      </Card>

      <Modal
        title={
          <span>
            <RobotOutlined style={{ marginRight: 8 }} />
            诊断详情
          </span>
        }
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        footer={null}
        width={800}
      >
        {detail && (
          <div>
            <p><Text type="secondary">文件：</Text>{detail.original_name}</p>
            <p><Text type="secondary">尺寸：</Text>{detail.image_width}x{detail.image_height}px</p>
            {detail.question && (
              <p><Text type="secondary">关注方向：</Text>{detail.question}</p>
            )}
            <p><Text type="secondary">模型：</Text><Tag color="blue">{detail.model_used}</Tag></p>
            <p><Text type="secondary">时间：</Text>{detail.created_at}</p>
            <Card size="small" style={{ marginTop: 12 }} className="diagnosis-report">
              <div className="markdown-body">
                <ReactMarkdown>{detail.diagnosis_result}</ReactMarkdown>
              </div>
            </Card>
          </div>
        )}
      </Modal>
    </div>
  )
}
