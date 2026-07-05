import { useState, useRef, useCallback } from 'react'
import { Client } from '@gradio/client'
import { Upload, Sparkles, Trash2, Copy, Check, Layers, Shield, Cpu, GitBranch, ExternalLink, Scale, RefreshCw } from 'lucide-react'

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false)
  const handleCopy = () => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }
  if (!text) return null
  return (
    <button className={`copy-btn ${copied ? 'copied' : ''}`} onClick={handleCopy}>
      {copied ? <><Check size={14} /> Copied</> : <><Copy size={14} /> Copy</>}
    </button>
  )
}

export default function App() {
  const [image, setImage] = useState(null)
  const [preview, setPreview] = useState(null)
  const [conciseCaption, setConciseCaption] = useState('')
  const [detailedCaption, setDetailedCaption] = useState('')
  const [style, setStyle] = useState('Both')
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState({ text: '', type: '' })
  const [dragOver, setDragOver] = useState(false)
  const fileRef = useRef(null)

  const handleFile = useCallback((file) => {
    if (!file || !file.type.startsWith('image/')) {
      setStatus({ text: '⚠️ Please select a valid image file.', type: 'error' })
      return
    }
    setImage(file)
    setPreview(URL.createObjectURL(file))
    setConciseCaption('')
    setDetailedCaption('')
    setStatus({ text: '', type: '' })
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    handleFile(file)
  }, [handleFile])

  const handleGenerate = async () => {
    if (!image) {
      setStatus({ text: '⚠️ Please upload an image first.', type: 'error' })
      return
    }
    setLoading(true)
    setConciseCaption('')
    setDetailedCaption('')

    const maxRetries = 3
    let attempt = 0

    while (attempt < maxRetries) {
      try {
        attempt++
        if (attempt > 1) {
          setStatus({ text: `⏳ Hugging Face Space is warming up or busy. Retrying (Attempt ${attempt}/${maxRetries})...`, type: '' })
          await new Promise((r) => setTimeout(r, 2500 * attempt))
        } else {
          setStatus({ text: '🔄 Connecting to Hugging Face Space & loading BLIP...', type: '' })
        }

        // Connect to the Hugging Face Space backend
        const app = await Client.connect("vardhanmit6/SnapScribe-AI-Image-Caption")
        
        setStatus({ text: '⚡ Running BLIP vision model inference...', type: '' })
        
        // Call the predict API endpoint
        const result = await app.predict("/predict", {
          img: image,
          prompt: prompt,
          style: style,
        })

        // Destructure outputs
        const [concise, detailed, statusMsg] = result.data
        
        setConciseCaption(concise || '')
        setDetailedCaption(detailed || '')
        
        if (statusMsg && statusMsg.includes('❌')) {
          throw new Error(statusMsg)
        }
        
        setStatus({ text: '✅ Captions generated successfully!', type: 'success' })
        setLoading(false)
        return // Success! Exit retry loop
      } catch (err) {
        console.error(`Inference Attempt ${attempt} failed:`, err)
        if (attempt >= maxRetries) {
          const errMsg = err.message || 'TypeError: Failed to fetch'
          setStatus({ 
            text: `❌ Connection Error (${errMsg}). If you are on a corporate network/VPN (like Zscaler) or have strict ad-blockers, they may block Hugging Face API streaming. Please try refreshing or checking your network connection.`, 
            type: 'error' 
          })
        }
      }
    }
    setLoading(false)
  }

  const handleClear = () => {
    setImage(null)
    setPreview(null)
    setConciseCaption('')
    setDetailedCaption('')
    setPrompt('')
    setStatus({ text: '', type: '' })
    if (fileRef.current) fileRef.current.value = ''
  }

  return (
    <>
      <div className="bg-effects">
        <div className="bg-blob-pink" />
      </div>

      <div className="app">
        <header className="hero fade-in">
          <h1 className="hero-title">✨ SnapScribe</h1>
          <p className="hero-subtitle">
            AI-powered image captioning that understands your visuals.
            Upload any image and get intelligent descriptions instantly.
          </p>
          <div className="badges" style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '8px', marginTop: '1rem' }}>
            <span className="badge badge-purple"><Cpu size={12} style={{ marginRight: '4px', display: 'inline' }} /> BLIP Model</span>
            <a href="https://huggingface.co/spaces/vardhanmit6/SnapScribe-AI-Image-Caption" target="_blank" rel="noopener noreferrer" className="badge badge-teal" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              🤗 HF Backend <ExternalLink size={10} />
            </a>
            <a href="https://github.com/Vardhan-Mittal/SnapScribe-AI-Image-Caption" target="_blank" rel="noopener noreferrer" className="badge badge-pink" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <GitBranch size={12} /> GitHub Repo <ExternalLink size={10} />
            </a>
            <a href="https://web-cyan-sigma-42.vercel.app" target="_blank" rel="noopener noreferrer" className="badge badge-purple" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              ⚡ Vercel Live <ExternalLink size={10} />
            </a>
            <span className="badge badge-green"><Scale size={12} style={{ marginRight: '4px', display: 'inline' }} /> MIT Licensed</span>
          </div>
        </header>

        <main className="main-grid">
          {/* Left Column — Upload & Settings */}
          <div className="glass-panel fade-in fade-in-delay-1">
            <div className="section-header">
              <h2 className="section-title">📸 Upload Image</h2>
              <p className="section-subtitle">Drop an image or click to browse</p>
            </div>

            <div
              className={`upload-zone ${dragOver ? 'drag-over' : ''} ${preview ? 'has-image' : ''}`}
              onClick={() => !preview && fileRef.current?.click()}
              onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
            >
              <input
                ref={fileRef}
                type="file"
                accept="image/*"
                onChange={(e) => handleFile(e.target.files[0])}
              />
              {preview ? (
                <>
                  <img src={preview} alt="Preview" className="preview-image" />
                  <button className="remove-image-btn" onClick={(e) => { e.stopPropagation(); handleClear() }}>
                    <Trash2 size={16} />
                  </button>
                </>
              ) : (
                <>
                  <div className="upload-icon"><Upload size={40} /></div>
                  <p className="upload-text">Drag & drop your image here</p>
                  <p className="upload-hint">Supports JPEG, PNG, WebP • Max 5MB</p>
                </>
              )}
            </div>

            <div className="options-section">
              <div className="option-group">
                <label className="option-label">Guided Captioning (Optional)</label>
                <input
                  type="text"
                  className="text-input"
                  placeholder="e.g., 'A photo of' or 'This image shows'"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                />
                <p className="option-hint">Guide the AI by providing a starting phrase</p>
              </div>

              <div className="option-group">
                <label className="option-label">Caption Style</label>
                <div className="style-selector">
                  {['Concise', 'Detailed', 'Both'].map((opt) => (
                    <button
                      key={opt}
                      className={`style-btn ${style === opt ? 'active' : ''}`}
                      onClick={() => setStyle(opt)}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="actions">
              <button
                className="btn-primary"
                onClick={handleGenerate}
                disabled={loading || !image}
              >
                {loading ? <><span className="spinner" />Generating...</> : <><Sparkles size={16} style={{ marginRight: '6px', display: 'inline' }} /> Generate Caption</>}
              </button>
              <button className="btn-secondary" onClick={handleClear}>🗑️ Clear</button>
            </div>
          </div>

          {/* Right Column — Results */}
          <div className="glass-panel fade-in fade-in-delay-2">
            <div className="section-header">
              <h2 className="section-title">📝 Results</h2>
              <p className="section-subtitle">Your AI-generated captions will appear here</p>
            </div>

            {(style === 'Concise' || style === 'Both') && (
              <div className="result-card" style={{ marginBottom: '1.5rem' }}>
                <div className="result-label"><Sparkles size={14} /> Concise Caption</div>
                <div className={`result-text ${!conciseCaption ? 'empty' : ''}`}>
                  {loading && style === 'Concise' ? (
                    <div className="skeleton" style={{ height: '50px' }} />
                  ) : (
                    conciseCaption || 'Upload an image and generate caption...'
                  )}
                  <CopyButton text={conciseCaption} />
                </div>
              </div>
            )}

            {(style === 'Detailed' || style === 'Both') && (
              <div className="result-card">
                <div className="result-label"><Layers size={14} /> Detailed Caption</div>
                <div className={`result-text ${!detailedCaption ? 'empty' : ''}`}>
                  {loading && style === 'Detailed' ? (
                    <div className="skeleton" style={{ height: '70px' }} />
                  ) : (
                    detailedCaption || 'Upload an image and generate caption...'
                  )}
                  <CopyButton text={detailedCaption} />
                </div>
              </div>
            )}

            {status.text && (
              <div className={`status-bar ${status.type}`} style={{ marginTop: '1.5rem', lineHeight: '1.5' }}>{status.text}</div>
            )}
          </div>
        </main>

        <hr className="divider" />
        <section className="how-section fade-in fade-in-delay-3">
          <h2 className="section-title">🚀 How It Works</h2>
          <div className="how-grid">
            <div className="how-card">
              <div className="how-card-icon">📸</div>
              <h3 className="how-card-title">Upload</h3>
              <p className="how-card-desc">
                Drop any image — photos, screenshots, artwork. Supports JPEG, PNG, and WebP.
              </p>
            </div>
            <div className="how-card">
              <div className="how-card-icon">🧠</div>
              <h3 className="how-card-title">Analyze</h3>
              <p className="how-card-desc">
                The BLIP vision-language model processes your image, understanding objects, scenes, and context.
              </p>
            </div>
            <div className="how-card">
              <div className="how-card-icon">✍️</div>
              <h3 className="how-card-title">Caption</h3>
              <p className="how-card-desc">
                Get an intelligent, context-aware caption you can copy and use anywhere.
              </p>
            </div>
          </div>
        </section>

        <footer className="footer" style={{ textAlign: 'center', lineHeight: '1.8', padding: '2rem 0' }}>
          <div>
            Built with ❤️ by <a href="https://github.com/Vardhan-Mittal" target="_blank" rel="noopener noreferrer">Vardhan Mittal</a> · Powered by{' '}
            <a href="https://huggingface.co/Salesforce/blip-image-captioning-base" target="_blank" rel="noopener noreferrer">BLIP</a> · Distributed under the <strong style={{ color: '#fff' }}>MIT License</strong>
          </div>
          <div style={{ marginTop: '0.5rem', fontSize: '0.85rem' }}>
            <a href="https://github.com/Vardhan-Mittal/SnapScribe-AI-Image-Caption" target="_blank" rel="noopener noreferrer" style={{ margin: '0 8px', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <GitBranch size={12} /> GitHub Repository
            </a>
            •
            <a href="https://web-cyan-sigma-42.vercel.app" target="_blank" rel="noopener noreferrer" style={{ margin: '0 8px', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              ⚡ Vercel Live Deployment
            </a>
            •
            <a href="https://huggingface.co/spaces/vardhanmit6/SnapScribe-AI-Image-Caption" target="_blank" rel="noopener noreferrer" style={{ margin: '0 8px', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              🤗 Hugging Face Backend Space
            </a>
          </div>
        </footer>
      </div>
    </>
  )
}
