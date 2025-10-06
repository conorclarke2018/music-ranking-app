'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { MusicalNoteIcon, StarIcon, PlayIcon } from '@heroicons/react/24/solid'

interface ApiResponse {
  message: string
  timestamp: string
  features: string[]
}

export default function HomePage() {
  const [apiData, setApiData] = useState<ApiResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const testBackendConnection = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/test')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        setApiData(data)
      } catch (err) {
        setError('Unable to connect to backend. Make sure the FastAPI server is running on port 8000.')
        console.error('Backend connection error:', err)
      } finally {
        setIsLoading(false)
      }
    }

    testBackendConnection()
  }, [])

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6">
      <div className="max-w-4xl mx-auto text-center">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mb-12"
        >
          <div className="flex items-center justify-center mb-6">
            <MusicalNoteIcon className="h-16 w-16 text-purple-400 mr-4" />
            <h1 className="text-6xl font-bold text-gradient">
              Music Ranking App
            </h1>
          </div>
          
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Rate albums and songs with AI-powered playlist generation and seamless Spotify integration
          </p>

          {/* Feature Cards */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="card p-6"
            >
              <StarIcon className="h-8 w-8 text-yellow-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Rate & Review</h3>
              <p className="text-gray-300 text-sm">
                Rate your favorite albums and songs, build your personal music library
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="card p-6"
            >
              <PlayIcon className="h-8 w-8 text-green-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">AI Playlists</h3>
              <p className="text-gray-300 text-sm">
                Get AI-generated playlists based on your listening patterns and ratings
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="card p-6"
            >
              <MusicalNoteIcon className="h-8 w-8 text-blue-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Spotify Integration</h3>
              <p className="text-gray-300 text-sm">
                Connect with Spotify and other music platforms for seamless experience
              </p>
            </motion.div>
          </div>

          {/* Backend Connection Status */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="card p-6 mb-8"
          >
            <h3 className="text-lg font-semibold mb-4">Backend Connection Status</h3>
            
            {isLoading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-400 mr-2"></div>
                <span className="text-gray-300">Testing connection...</span>
              </div>
            ) : error ? (
              <div className="text-red-400">
                <p className="font-medium mb-2">❌ Connection Failed</p>
                <p className="text-sm">{error}</p>
              </div>
            ) : apiData ? (
              <div className="text-green-400">
                <p className="font-medium mb-4">✅ {apiData.message}</p>
                <div className="text-left">
                  <p className="text-sm text-gray-300 mb-2">Available Features:</p>
                  <ul className="text-sm space-y-1">
                    {apiData.features.map((feature, index) => (
                      <li key={index} className="text-gray-300">• {feature}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : null}
          </motion.div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 1.0 }}
              className="btn-primary"
            >
              Get Started
            </motion.button>
            
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 1.2 }}
              className="btn-secondary"
            >
              View Documentation
            </motion.button>
          </div>
        </motion.div>
      </div>
    </div>
  )
}