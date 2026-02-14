import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 180000,
})

export async function submitDiagnosis(file, question) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('question', question || '')
  const response = await api.post('/diagnosis', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export async function getHistory(page = 1, pageSize = 10) {
  const response = await api.get('/history', {
    params: { page, page_size: pageSize },
  })
  return response.data
}

export async function getDiagnosisDetail(id) {
  const response = await api.get(`/history/${id}`)
  return response.data
}
