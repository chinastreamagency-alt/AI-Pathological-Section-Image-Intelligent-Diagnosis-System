import React from 'react'
import { Upload, message } from 'antd'
import { InboxOutlined } from '@ant-design/icons'

const { Dragger } = Upload

const ALLOWED_TYPES = [
  'image/jpeg', 'image/png', 'image/bmp',
  'image/tiff', 'image/webp',
]

export default function ImageUpload({ fileList, onChange }) {
  const props = {
    name: 'file',
    multiple: false,
    maxCount: 1,
    fileList,
    accept: ALLOWED_TYPES.join(','),
    beforeUpload(file) {
      if (!ALLOWED_TYPES.includes(file.type)) {
        message.error('请上传 JPG/PNG/BMP/TIFF/WebP 格式的图片')
        return Upload.LIST_IGNORE
      }
      if (file.size > 20 * 1024 * 1024) {
        message.error('文件大小不能超过 20MB')
        return Upload.LIST_IGNORE
      }
      return false
    },
    onChange(info) {
      onChange(info.fileList.slice(-1))
    },
    onDrop() {},
  }

  return (
    <Dragger {...props} className="upload-dragger">
      <p className="ant-upload-drag-icon">
        <InboxOutlined />
      </p>
      <p className="ant-upload-text">点击或拖拽病理切片图片到此区域</p>
      <p className="ant-upload-hint">
        支持 JPG、PNG、BMP、TIFF、WebP 格式，单文件不超过 20MB
      </p>
    </Dragger>
  )
}
