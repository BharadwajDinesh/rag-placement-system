import { useState, useRef, useEffect } from 'react'
import Header from './components/Header.jsx'
import MessageList from './components/MessageList.jsx'
import InputBox from './components/InputBox.jsx'
import WelcomeScreen from './components/WelcomeScreen.jsx'
import './App.css'

const SUGGESTED_QUESTIONS = [
  "What is the One Student One Job policy?",
  "What are the eligibility criteria for placements?",
  "What is the role of the Training and Placement Cell?",
  "Can I participate in placements with a backlog?",
]

function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading])

  const sendMessage = async (text) => {
    const query = text.trim()
    if (!query || loading) return

    const userMsg = { role: 'user', content: query, id: Date.now() }
    setMessages(prev => [...prev, userMsg])
    setLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 3 })
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()

      const botMsg = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        id: Date.now() + 1
      }
      setMessages(prev => [...prev, botMsg])
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: "Sorry, I couldn't connect to the server. Please make sure the backend is running.",
        error: true,
        id: Date.now() + 1
      }])
    } finally {
      setLoading(false)
    }
  }

  const clearChat = () => setMessages([])

  return (
    <div className="app-layout">
      <Header onClear={clearChat} hasMessages={messages.length > 0} />
      <main className="chat-area">
        {messages.length === 0 ? (
          <WelcomeScreen
            suggestions={SUGGESTED_QUESTIONS}
            onSuggest={sendMessage}
          />
        ) : (
          <MessageList
            messages={messages}
            loading={loading}
            messagesEndRef={messagesEndRef}
          />
        )}
      </main>
      <InputBox onSend={sendMessage} loading={loading} />
    </div>
  )
}

export default App