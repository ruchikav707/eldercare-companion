import { useEffect, useState } from 'react'
import './App.css'

const API_BASE_URL = 'http://127.0.0.1:8000'
const SESSION_ID = 'eldercare-demo-session'

async function requestAppointments() {
  const response = await fetch(`${API_BASE_URL}/appointments`)

  if (!response.ok) {
    throw new Error('Unable to load appointments.')
  }

  return response.json()
}

function App() {
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [chatMessages, setChatMessages] = useState([
    {
      role: 'assistant',
      text: 'Hello! I am your ElderCare Companion. How can I help with your appointments today?',
    },
  ])
  const [chatInput, setChatInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const [chatError, setChatError] = useState('')

  function loadAppointments() {
    setLoading(true)

    requestAppointments()
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
  }

  useEffect(() => {
    let isActive = true

    requestAppointments()
      .then((data) => {
        if (!isActive) return

        setAppointments(data)
        setError('')
      })
      .catch(() => {
        if (!isActive) return

        setError(
          'We could not load your appointments. Please check your connection and try again.'
        )
      })
      .finally(() => {
        if (isActive) {
          setLoading(false)
        }
      })

    return () => {
      isActive = false
    }
  }, [])

  async function handleChatSubmit(event) {
    event.preventDefault()

    const message = chatInput.trim()

    if (!message || chatLoading) {
      return
    }

    setChatMessages((currentMessages) => [
      ...currentMessages,
      {
        role: 'user',
        text: message,
      },
    ])

    setChatInput('')
    setChatError('')
    setChatLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/agent/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: SESSION_ID,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail || 'The assistant is temporarily unavailable.'
        )
      }

      setChatMessages((currentMessages) => [
        ...currentMessages,
        {
          role: 'assistant',
          text: data.reply,
        },
      ])

      if (
        data.tool_used === 'create_appointment' &&
        data.confirmation_required === false
      ) {
        loadAppointments()
      }
    } catch (requestError) {
      setChatError(
        requestError.message ||
          'The assistant is temporarily unavailable. Please try again.'
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
          Manage your appointments through a simple simulated Alexa+
          experience.
        </p>
      </header>

      <section
        className="chat-section"
        aria-labelledby="assistant-heading"
      >
        <div className="section-heading">
          <div>
            <p className="eyebrow chat-eyebrow">
              SIMULATED ALEXA+ EXPERIENCE
            </p>

            <h2 id="assistant-heading">Talk to your assistant</h2>
          </div>

          <span className="assistant-status">
            <span className="status-dot" aria-hidden="true"></span>
            Ready
          </span>
        </div>

        <div
          className="chat-messages"
          aria-live="polite"
          aria-label="Conversation with ElderCare Companion"
        >
          {chatMessages.map((chatMessage, index) => (
            <div
              className={`chat-message ${chatMessage.role}`}
              key={`${chatMessage.role}-${index}`}
            >
              <p className="message-sender">
                {chatMessage.role === 'assistant'
                  ? 'ElderCare Companion'
                  : 'You'}
              </p>

              <p>{chatMessage.text}</p>
            </div>
          ))}

          {chatLoading && (
            <div className="chat-message assistant thinking-message">
              <p className="message-sender">ElderCare Companion</p>
              <p>Thinking...</p>
            </div>
          )}
        </div>

        {chatError && (
          <p className="chat-error" role="alert">
            {chatError}
          </p>
        )}

        <form className="chat-form" onSubmit={handleChatSubmit}>
          <label className="sr-only" htmlFor="chat-input">
            Type your message
          </label>

          <input
            id="chat-input"
            type="text"
            value={chatInput}
            onChange={(event) => setChatInput(event.target.value)}
            placeholder="For example: What do I have tomorrow?"
            maxLength={1000}
            disabled={chatLoading}
          />

          <button
            type="submit"
            disabled={chatLoading || !chatInput.trim()}
          >
            {chatLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </section>

      <section
        className="appointments-section"
        aria-labelledby="appointments-heading"
      >
        <div className="section-heading">
          <h2 id="appointments-heading">Your Appointments</h2>

          <button
            className="refresh-button"
            type="button"
            onClick={loadAppointments}
            disabled={loading}
          >
            {loading ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>

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
                  <h3>
                    {appointment.title || 'Untitled appointment'}
                  </h3>

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
                  {appointment.preparation_notes ||
                    'No preparation notes'}
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