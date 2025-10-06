import { Metadata } from 'next'
import HomePage from '@/components/HomePage'

export const metadata: Metadata = {
  title: 'Music Ranking App',
  description: 'Rate albums and songs with AI-powered playlist generation and Spotify integration',
}

export default function Page() {
  return <HomePage />
}