/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['i.scdn.co', 'mosaic.scdn.co'], // Spotify image domains
  },
  env: {
    CUSTOM_KEY: 'my-value',
  },
}

module.exports = nextConfig