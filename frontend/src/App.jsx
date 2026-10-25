
import { useState } from 'react'


function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#">
          <span className="brand-mark">A</span>
          <span>AskAI</span>
        </a>

        <span className="topbar-label">DOCUMENT INTELLIGENCE</span>
      </header>

      <main className="workspace">
        <section className="welcome-section">
          <p className="eyebrow">YOUR KNOWLEDGE, CONNECTED</p>
          <h1>Ask your documents.</h1>
          <p className="welcome-description">
            Upload a document, ask a question, and get answers grounded
            in your content.
          </p>
        </section>

        <div className="workspace-grid">
          <aside className="upload-panel">
            <DocumentUpload />
          </aside>

          <section className="question-panel">
            <QuestionForm />
          </section>
        </div>

        <footer className="page-footer">
          <span>AskAI</span>
          <span>Answers grounded in your documents.</span>
        </footer>
      </main>
    </div>
  )
}


function DocumentUpload() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadMessage, setUploadMessage] = useState('')
  const [isUploading, setIsUploading] = useState(false) 
  

  
  async function handleUpload() {
    if (!selectedFile) {
      setUploadMessage('Please select a PDF first.')
      return
    }

    setIsUploading(true)
    setUploadMessage('')

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData,
      })  

      const data = await response.json()

      if (!response.ok) {
        setUploadMessage(
          typeof data.detail === 'string'
            ? data.detail
            : 'Upload failed. Please try again.'
        )
        return
      }

      setUploadMessage(
        `Upload successful! Pages: ${data.page_count}, Chunks: ${data.chunk_count}`
      )
    } catch (error) {
      console.error(error)
      setUploadMessage('Could not connect to the backend.')
    } finally {
      setIsUploading(false)
    }
  }


  function handleFileChange(event) {
    const file = event.target.files[0]
    setSelectedFile(file ?? null)
  }

  return (
    <div className="upload-content">
      <h2 className="panel-title">Add your document</h2>

      <p className="panel-description">
        Upload a PDF to start asking questions about its content.
      </p>

      <div className="file-dropzone">
        <div className="upload-icon">↑</div>

        <p className="dropzone-title">Choose a PDF document</p>

        <p className="dropzone-description">
          Select a PDF from your computer
        </p>

        <input
          className="file-input"
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
        />

        {selectedFile && (
          <p className="selected-file">
            Selected: {selectedFile.name}
          </p>
        )}

        <button
          className="primary-button upload-button"
          type="button"
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
        >
          {isUploading ? 'Uploading...' : 'Upload document'}
        </button>

        {uploadMessage && (
          <p className="upload-message">{uploadMessage}</p>
        )}
      </div>
    </div>
  )
}




function QuestionForm() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])
  const [isAsking, setIsAsking] = useState(false)

  function handleQuestionChange(event) {
    setQuestion(event.target.value)
  }

  
  async function handleAsk() {
    setIsAsking(true)
    setAnswer('')
    setSources([])

    
    try {
      const response = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
        }),
      })

      const data = await response.json()
      console.log('Full backend response:', data)
      console.log('Sources received:', data.sources)

      if (!response.ok) {
        setAnswer(data.detail || data.message || 'Something went wrong.')
        return
      }

      setAnswer(data.answer)
      setSources(data.sources ?? [])
    } catch (error) {
      setAnswer('Could not connect to the backend. Please check that it is running.')
      console.error(error)
    } finally {
      setIsAsking(false)
    }
  }


  
  return (
    <div className="question-content">
      <h2 className="panel-title">Ask a question</h2>

      <p className="panel-description">
        Ask anything about your uploaded document.
      </p>

      <div className="question-form">
        <input
          className="question-input"
          type="text"
          placeholder="e.g. What are the key points?"
          value={question}
          onChange={handleQuestionChange}
        />

        <button
          className="primary-button ask-button"
          type="button"
          onClick={handleAsk}
          disabled={isAsking || !question.trim()}
        >
          {isAsking ? 'Thinking...' : 'Ask question'}
        </button>
      </div>

      {answer && (
        <div className="answer-section">
          <h3 className="result-title">Answer</h3>
          <p className="answer-text">{answer}</p>

          {sources.length > 0 && (
            <div className="sources-section">
              <h3 className="result-title">Sources</h3>

              {sources.map((source, index) => (
                <div className="source-card" key={index}>
                  <span className="source-label">
                    SOURCE {index + 1}
                  </span>
                  <p className="source-text">{source.text}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )

}



export default App
