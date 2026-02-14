import React from 'react'
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import { Layout, Menu } from 'antd'
import { ExperimentOutlined, HistoryOutlined } from '@ant-design/icons'
import HomePage from './pages/HomePage'
import HistoryPage from './pages/HistoryPage'

const { Header, Content, Footer } = Layout

function AppMenu() {
  const location = useLocation()
  const currentKey = location.pathname === '/history' ? 'history' : 'home'

  const items = [
    {
      key: 'home',
      icon: <ExperimentOutlined />,
      label: <Link to="/">智能诊断</Link>,
    },
    {
      key: 'history',
      icon: <HistoryOutlined />,
      label: <Link to="/history">诊断记录</Link>,
    },
  ]

  return <Menu theme="dark" mode="horizontal" selectedKeys={[currentKey]} items={items} />
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ display: 'flex', alignItems: 'center' }}>
          <div className="logo">AI 病理切片智能诊断</div>
          <AppMenu />
        </Header>
        <Content style={{ padding: '24px', maxWidth: 1200, margin: '0 auto', width: '100%' }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </Content>
        <Footer style={{ textAlign: 'center', color: '#999' }}>
          AI病理切片智能诊断系统 - 仅供辅助参考，不可替代专业病理医师诊断
        </Footer>
      </Layout>
    </BrowserRouter>
  )
}
