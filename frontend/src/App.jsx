import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [backendMessage, setBackendMessage] = useState(
    'Connecting to backend...'
  )

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then((response) => response.json())
      .then((data) => setBackendMessage(data.message))
      .catch(() => setBackendMessage('Could not connect to backend'))
  }, [])

  return (
    <main>
      <h1>ElderCare Companion</h1>
      <p>{backendMessage}</p>
    </main>
  )
}

export default App