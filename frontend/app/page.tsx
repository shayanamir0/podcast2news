'use client'

import { useState } from 'react'
import { Play, Download, Loader2, AlertCircle } from 'lucide-react'
import axios from 'axios'

interface NewsArticle {
  title: string
  content: string
  key_quote: string
}

interface GenerateNewsResponse {
  success: boolean
  articles: NewsArticle[]
  session_id: string
  url: string
}

export default function Home() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [articles, setArticles] = useState<NewsArticle[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!url.trim()) return

    setLoading(true)
    setError(null)
    setArticles([])

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await axios.post<GenerateNewsResponse>(
        `${apiUrl}/generate-news`,
        { url }
      )

      if (response.data.success) {
        setArticles(response.data.articles)
        setSessionId(response.data.session_id)
      } else {
        setError('Failed to generate news articles')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred while processing the podcast')
    } finally {
      setLoading(false)
    }
  }

  const downloadArticle = async (articleIndex: number, title: string, format: string = 'txt') => {
    if (!sessionId) return

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await axios.get(
        `${apiUrl}/download-article/${sessionId}/${articleIndex}/${format}`,
        { responseType: 'blob' }
      )

      const blob = new Blob([response.data], { 
        type: format === 'docx' 
          ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
          : 'text/plain' 
      })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${title.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '_')}.${format}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Error downloading article:', err)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Podcast2News
        </h1>
        <p className="text-xl text-gray-600">
          Transform podcast content into engaging news articles
        </p>
      </div>

      {/* Input Form */}
      <div className="card mb-8">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
              YouTube Podcast URL
            </label>
            <input
              id="url"
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Processing podcast...</span>
              </>
            ) : (
              <>
                <Play className="h-5 w-5" />
                <span>Generate News Articles</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Error Message */}
      {error && (
        <div className="card mb-8 bg-red-50 border-red-200">
          <div className="flex items-center space-x-2 text-red-700">
            <AlertCircle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="card mb-8">
          <div className="flex items-center justify-center space-x-2 text-gray-600">
            <Loader2 className="h-6 w-6 animate-spin" />
            <span>Extracting transcript and generating articles...</span>
          </div>
        </div>
      )}

      {/* News Articles */}
      {articles.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Generated News Articles
          </h2>
          
          {articles.map((article, index) => (
            <div key={index} className="card">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold text-gray-900 flex-1">
                  {article.title}
                </h3>
                <div className="flex space-x-2 ml-4">
                  <button
                    onClick={() => downloadArticle(index, article.title, 'txt')}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <Download className="h-4 w-4" />
                    <span>TXT</span>
                  </button>
                  <button
                    onClick={() => downloadArticle(index, article.title, 'docx')}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <Download className="h-4 w-4" />
                    <span>DOCX</span>
                  </button>
                </div>
              </div>
              
              <div className="prose prose-gray max-w-none">
                <p className="text-gray-700 leading-relaxed mb-4">
                  {article.content}
                </p>
                
                {article.key_quote && (
                  <blockquote className="border-l-4 border-primary-500 pl-4 py-2 bg-primary-50 rounded-r-lg">
                    <p className="text-primary-700 italic">
                      "{article.key_quote}"
                    </p>
                  </blockquote>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
} 