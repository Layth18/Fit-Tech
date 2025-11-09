import { Routes, Route } from 'react-router-dom'
import LoginPage from './Pages/Login'
import GlobalLayout from './Pages/Layout'

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/app" element={<GlobalLayout />} />
    </Routes>
  )
}

export default App