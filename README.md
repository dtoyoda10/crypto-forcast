# Cryptocurrency Forecast Application

A full-stack web application for cryptocurrency price forecasting using machine learning. The application provides real-time cryptocurrency data, historical price analysis, and price predictions using linear regression models.

## Features

- Real-time cryptocurrency price tracking via Coinbase API
- Machine learning-based price predictions
- User authentication with JWT tokens
- Multi-language support (English, French, Arabic, Chinese)
- Responsive Material-UI design
- Dark/Light theme support
- Portfolio management
- Interactive price charts and visualizations

## Technology Stack

### Frontend
- React 18.2.0 with TypeScript
- Material-UI (MUI) v5
- Redux Toolkit for state management
- ApexCharts for data visualization
- Axios for API communication
- React Router for navigation

### Backend
- Flask 3.0.0 (Python)
- MongoDB for data storage
- Flask-JWT-Extended for authentication
- Scikit-learn for ML predictions
- Flask-CORS for cross-origin requests
- Flask-Limiter for rate limiting

### DevOps
- Docker and Docker Compose
- Nginx for production frontend serving
- Health checks and monitoring

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- MongoDB 7.0 or higher
- Docker and Docker Compose (optional)

## Installation

### Option 1: Docker Deployment (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/dtoyoda10/crypto-forcast.git
cd crypto-forcast
```

2. Create environment file:
```bash
cp server/.env.example server/.env
```

3. Generate secure secret keys:
```bash
python -c "import os; print('SECRET_KEY=' + os.urandom(32).hex())" >> server/.env
python -c "import os; print('JWT_SECRET_KEY=' + os.urandom(32).hex())" >> server/.env
```

4. Start all services:
```bash
docker-compose up -d
```

5. Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:5000
- MongoDB: localhost:27017

### Option 2: Manual Installation

#### Backend Setup

1. Navigate to server directory:
```bash
cd server
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
```

5. Edit `.env` file with your configuration:
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=crypto_forcast
```

6. Start MongoDB:
```bash
mongod
```

7. Run the Flask application:
```bash
python app.py
```

#### Frontend Setup

1. Navigate to client directory:
```bash
cd client
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
cp .env.example .env
```

4. Edit `.env` file:
```bash
REACT_APP_API_URL=http://localhost:5000
```

5. Start development server:
```bash
npm start
```

6. Build for production:
```bash
npm run build
```

## API Documentation

### Authentication Endpoints

#### Register User
```
POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response:
{
  "message": "User registered successfully",
  "email": "user@example.com"
}
```

#### Login
```
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response:
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "email": "user@example.com"
}
```

### Cryptocurrency Endpoints

#### Get Price Predictions
```
POST /api/prediction
Content-Type: application/json

{
  "coin": "BTC",
  "period": "day"
}

Response:
{
  "coin": "BTC",
  "period": "day",
  "predictions": [
    ["2025-01-15 10:00:00", 45234.56],
    ["2025-01-15 11:00:00", 45345.67]
  ]
}
```

#### Get Coins Summary
```
GET /api/get_coins_summary

Response:
{
  "data": [...]
}
```

#### Get Historical Data
```
POST /api/get_coins_histories
Content-Type: application/json

{
  "coin": "ETH",
  "period": "week"
}

Response:
{
  "coin": "ETH",
  "period": "week",
  "data": {...}
}
```

#### Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "service": "crypto-forecast-api"
}
```

## Configuration

### Backend Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| FLASK_ENV | Environment mode | development | No |
| SECRET_KEY | Flask secret key | - | Yes (Production) |
| JWT_SECRET_KEY | JWT signing key | - | Yes (Production) |
| MONGODB_URI | MongoDB connection string | mongodb://localhost:27017 | Yes |
| MONGODB_DB_NAME | Database name | crypto_forcast | No |
| COINBASE_API_TIMEOUT | API request timeout (seconds) | 10 | No |
| CORS_ORIGINS | Allowed CORS origins (comma-separated) | http://localhost:3000 | No |
| RATELIMIT_ENABLED | Enable rate limiting | True | No |
| RATELIMIT_DEFAULT | Default rate limit | 100 per hour | No |
| LOG_LEVEL | Logging level | INFO | No |
| PORT | Server port | 5000 | No |

### Frontend Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| REACT_APP_API_URL | Backend API URL | http://localhost:5000 | Yes |

## Security Features

- Bcrypt password hashing
- JWT-based authentication with token expiration
- Rate limiting to prevent abuse
- CORS protection with whitelisted origins
- Input validation and sanitization
- SQL/NoSQL injection prevention
- Secure HTTP headers (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection)
- Environment-based configuration
- Database connection pooling with timeouts

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

## Development

### Running Tests

Backend:
```bash
cd server
pytest
```

Frontend:
```bash
cd client
npm test
```

### Code Linting

Frontend:
```bash
cd client
npm run lint
```

### Building for Production

Frontend:
```bash
cd client
npm run build
```

## Project Structure

```
crypto-forcast/
├── client/                    # React frontend application
│   ├── public/
│   ├── src/
│   │   ├── assets/           # Images and static files
│   │   ├── components/       # Reusable React components
│   │   ├── layouts/          # Layout components
│   │   ├── routes/           # Route configuration
│   │   ├── store/            # Redux store
│   │   ├── theme/            # Material-UI theme
│   │   ├── utils/            # Utility functions
│   │   └── views/            # Page components
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── server/                   # Flask backend application
│   ├── app.py               # Application entry point
│   ├── auth.py              # Authentication logic
│   ├── coinbase.py          # Coinbase API integration
│   ├── config.py            # Configuration management
│   ├── models.py            # Database models
│   ├── routes.py            # API routes
│   ├── services.py          # ML prediction service
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml       # Docker orchestration
└── README.md
```

## Troubleshooting

### MongoDB Connection Issues

If you encounter MongoDB connection errors:

1. Ensure MongoDB is running:
```bash
systemctl status mongod
```

2. Check connection string in .env file

3. Verify network connectivity:
```bash
mongosh mongodb://localhost:27017
```

### CORS Errors

If you see CORS errors in the browser console:

1. Check that the backend CORS_ORIGINS includes your frontend URL
2. Verify the frontend is using the correct API URL
3. Ensure both frontend and backend are running

### Docker Issues

If containers fail to start:

1. Check logs:
```bash
docker-compose logs
```

2. Rebuild containers:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Production Deployment

### Before Deploying

1. Generate strong secret keys
2. Set FLASK_ENV=production
3. Configure proper MONGODB_URI
4. Set appropriate CORS_ORIGINS
5. Review and adjust rate limiting settings
6. Set up SSL/TLS certificates
7. Configure proper logging and monitoring
8. Set up database backups

### Recommended Production Setup

1. Use a managed MongoDB service (MongoDB Atlas, etc.)
2. Deploy backend on a platform like AWS, GCP, or Heroku
3. Deploy frontend on Netlify, Vercel, or similar
4. Use environment variables for all secrets
5. Enable HTTPS only
6. Set up monitoring and alerting
7. Implement database backups
8. Use a reverse proxy (Nginx, Caddy)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## Acknowledgments

- Coinbase API for cryptocurrency data
- Material-UI for the component library
- Scikit-learn for machine learning capabilities
