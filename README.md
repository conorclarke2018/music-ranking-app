# Music Ranking App

A comprehensive music ranking application that allows users to rate albums and songs, with seamless integration to Spotify and other music platforms. Features AI-powered playlist generation based on user interactions and listening patterns.

## 🎵 Features

### Core Functionality
- **Music Rating System**: Rate and review albums, songs, and artists
- **Multi-Platform Integration**: Connect with Spotify, Apple Music, and other streaming services
- **Personal Music Library**: Track your listening history and favorites
- **Advanced Search**: Find music by genre, artist, album, or mood

### AI-Powered Features
- **Smart Playlist Generation**: AI creates personalized playlists based on your ratings and listening behavior
- **Music Recommendations**: Get suggestions for new music based on your taste profile
- **Mood-Based Curation**: Generate playlists that match your current mood or activity
- **Trend Analysis**: Discover trending music in your preferred genres

### Social Features
- **User Profiles**: Create and customize your music profile
- **Social Sharing**: Share your favorite albums and playlists with friends
- **Community Ratings**: See how your ratings compare with the community
- **Music Discovery**: Find new music through other users' recommendations

## 🛠 Tech Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **Headless UI**: Accessible UI components

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database
- **Pydantic**: Data validation and serialization
- **Alembic**: Database migration tool

### External Services
- **Spotify API**: Music streaming integration
- **OpenAI API**: AI-powered features and recommendations
- **JWT Authentication**: Secure user authentication

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v18 or higher)
- **Python** (v3.9 or higher)
- **PostgreSQL** (v13 or higher)
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd music-ranking-app
   ```

2. **Install root dependencies**
   ```bash
   npm install
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Set up the backend**
   ```bash
   cd ../backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Environment Configuration**
   
   Create `.env` files in both frontend and backend directories:

   **Frontend (.env.local):**
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_SPOTIFY_CLIENT_ID=your_spotify_client_id
   ```

   **Backend (.env):**
   ```env
   DATABASE_URL=postgresql://username:password@localhost/musicrankingdb
   SECRET_KEY=your_secret_key
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   OPENAI_API_KEY=your_openai_api_key
   ```

6. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb musicrankingdb
   
   # Run migrations
   cd backend
   alembic upgrade head
   ```

### Running the Application

1. **Start both frontend and backend**
   ```bash
   npm run dev
   ```

   This will start:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

2. **Or run them separately**
   ```bash
   # Terminal 1 - Backend
   npm run dev:backend
   
   # Terminal 2 - Frontend
   npm run dev:frontend
   ```

## 📁 Project Structure

```
music-ranking-app/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # Reusable React components
│   │   ├── services/        # API calls and external services
│   │   └── types/          # TypeScript type definitions
│   ├── public/             # Static assets
│   └── package.json
├── backend/                # FastAPI application
│   ├── src/
│   │   ├── api/           # API routes
│   │   ├── models/        # Database models
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utility functions
│   ├── alembic/          # Database migrations
│   └── requirements.txt
├── config/               # Configuration files
├── docs/                # Documentation
├── tests/               # Test files
└── README.md
```

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Tests
```bash
cd backend
pytest
```

### Run All Tests
```bash
npm test
```

## 🔧 Development

### API Documentation
Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Code Formatting
```bash
# Frontend
npm run lint

# Backend
cd backend
black src/
flake8 src/
```

## 🌟 Features Roadmap

- [ ] Advanced music analytics and insights
- [ ] Social features and user following
- [ ] Mobile app development
- [ ] Integration with additional music platforms
- [ ] Advanced AI recommendation algorithms
- [ ] Real-time collaboration features
- [ ] Music event and concert integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 External APIs

- **Spotify Web API**: For music data and streaming integration
- **OpenAI API**: For AI-powered recommendations and playlist generation
- **Last.fm API**: For additional music metadata (optional)

## 📞 Support

For questions or support, please open an issue in the GitHub repository or contact the development team.