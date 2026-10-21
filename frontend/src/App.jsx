
import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

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
