
import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [messages, setMessages] = useState([])
  const [chatInput, setChatInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const [chatError, setChatError] = useState('')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/appointments')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Unable to load appointments.')
        }
        return response.json()
      })
      .then((data) => {
        setAppointments(data)
        setError('')
      })
      .catch(() => {
        setError(
          'We could not load your appointments. Please check your connection and try again.'
        )
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  async function sendMessage(event) {
    event.preventDefault()

    const userMessage = chatInput.trim()

    if (!userMessage || chatLoading) return

    setMessages((previousMessages) => [
      ...previousMessages,
      { role: 'user', text: userMessage },
    ])
    setChatInput('')
    setChatError('')
    setChatLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/agent/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          session_id: 'demo-session',
        }),
      })

      if (!response.ok) {
        throw new Error('The assistant could not respond. Please try again.')
      }

      const data = await response.json()

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: 'assistant',
          text: data.reply || 'Sorry, I could not generate a response.',
          confirmationRequired: data.confirmation_required || false,
        },
      ])
    } catch {
      setChatError(
        'Unable to reach the assistant. Please check that the backend is running and try again.'
      )
    } finally {
      setChatLoading(false)
    }
  }


  function formatDateTime(dateTime) {
    if (!dateTime) return 'Date and time not available'

    const date = new Date(dateTime)

    if (Number.isNaN(date.getTime())) {
      return 'Date and time not available'
    }

    return date.toLocaleString([], {
      dateStyle: 'long',
      timeStyle: 'short',
    })
  }

  return (
    <main className="dashboard">
      <header className="dashboard-header">
        <p className="eyebrow">YOUR PERSONAL CARE ASSISTANT</p>
        <h1>ElderCare Companion</h1>
        <p className="subtitle">
          Your appointments, organized in one simple place.
        </p>
      </header>

      <section className="chat-section" aria-labelledby="chat-heading">
        <h2 id="chat-heading">Chat with your care assistant</h2>
        <p className="chat-intro">
          Ask about your appointments or get help with your daily routine.
        </p>

        <div className="chat-messages" aria-live="polite">
          {messages.length === 0 && (
            <p className="chat-welcome">
              Hello! How can I help you today?
            </p>
          )}

          {messages.map((message, index) => (
            <div
              className={`chat-message ${message.role}`}
              key={`${message.role}-${index}`}
            >
              <strong>
                {message.role === 'user' ? 'You' : 'Care Assistant'}
              </strong>
              <p>{message.text}</p>
            </div>
          ))}

          {chatLoading && (
            <p className="chat-thinking" role="status">
              Assistant is thinking...
            </p>
          )}
        </div>

        {chatError && (
          <p className="message error" role="alert">
            {chatError}
          </p>
        )}

        <form className="chat-form" onSubmit={sendMessage}>
          <input
            type="text"
            value={chatInput}
            onChange={(event) => setChatInput(event.target.value)}
            placeholder="Type your message..."
            aria-label="Your message"
            maxLength={1000}
            disabled={chatLoading}
            required
          />
          <button type="submit" disabled={chatLoading || !chatInput.trim()}>
            {chatLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </section>

      <section className="appointments-section" aria-labelledby="appointments-heading">
        <h2 id="appointments-heading">Your Appointments</h2>

        {loading && (
          <p className="message" role="status">
            Loading your appointments...
          </p>
        )}

        {!loading && error && (
          <p className="message error" role="alert">
            {error}
          </p>
        )}

        {!loading && !error && appointments.length === 0 && (
          <div className="empty-state">
            <h3>No appointments yet</h3>
            <p>Your upcoming appointments will appear here.</p>
          </div>
        )}

        {!loading && !error && appointments.length > 0 && (
          <div className="appointments-list">
            {appointments.map((appointment) => (
              <article className="appointment-card" key={appointment.id}>
                <div className="card-heading">
                  <h3>{appointment.title || 'Untitled appointment'}</h3>
                  <span
                    className={`status status-${(
                      appointment.status || 'scheduled'
                    ).toLowerCase()}`}
                  >
                    {appointment.status || 'Scheduled'}
                  </span>
                </div>

                <p>
                  <strong>Date and time:</strong>{' '}
                  {formatDateTime(appointment.appointment_at)}
                </p>

                <p>
                  <strong>Location:</strong>{' '}
                  {appointment.location || 'Not specified'}
                </p>

                <p>
                  <strong>Preparation notes:</strong>{' '}
                  {appointment.preparation_notes || 'No preparation notes'}
                </p>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  )
}

export default App
