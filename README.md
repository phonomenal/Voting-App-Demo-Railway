# Voting Service Demo

A modern, containerized voting application built with Python Flask and Redis, demonstrating cloud-native development practices and deployment strategies.

## 🗳️ What is this app?

This is a simple yet powerful voting application that allows users to vote between two options (currently Pizza vs Brownie in a "bake off" scenario). The application demonstrates:

- **Microservices Architecture**: Separate frontend (Python Flask) and backend (Redis) services
- **Containerization**: Full Docker support for consistent deployment across environments
- **Cloud Deployment**: Ready for deployment on Railway with automatic scaling
- **Local Development**: Easy setup with Docker Compose for development and testing

## 🏗️ How it works

The application consists of two main components:

### Frontend Service (`voting-service-front`)
- **Technology**: Python Flask web application
- **Purpose**: Serves the web interface and handles user interactions
- **Features**:
  - Clean, responsive web interface
  - Real-time vote counting
  - Vote reset functionality
  - Configurable voting options and titles

### Backend Service (`voting-service-back`)
- **Technology**: Redis database
- **Purpose**: Stores and manages vote counts
- **Features**:
  - In-memory data storage for fast access
  - Persistent vote counting
  - Automatic failover to in-memory storage if Redis is unavailable

### Architecture Flow
1. User visits the web interface
2. User clicks on their preferred option (Pizza or Brownie)
3. Frontend service processes the vote
4. Vote is stored in Redis backend
5. Updated vote counts are displayed in real-time

## 🚀 Local Development & Testing

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Voting-App-Demo
   ```

2. **Build and run with Docker Compose**
   ```bash
   # Build the application
   docker compose build

   # Start all services
   docker compose up
   ```

3. **Access the application**
   - Open your browser and navigate to: http://localhost:8080
   - Start voting and see the results update in real-time!

4. **Stop the application**
   ```bash
   # Stop services (Ctrl+C, then)
   docker compose down
   ```

### Development Workflow

1. **Make changes to the application**
   - Edit files in `voting-service/voting-service/`
   - Modify `config_file.cfg` to change voting options or title

2. **Rebuild and test**
   ```bash
   docker compose build
   docker compose up
   ```

3. **View logs**
   ```bash
   # View all logs
   docker compose logs

   # View specific service logs
   docker compose logs voting-service-front
   docker compose logs voting-service-back
   ```

### Customization

Edit `voting-service/voting-service/config_file.cfg` to customize:
```ini
# UI Configurations
TITLE = 'Your Custom Voting Title!'
VOTE1VALUE = 'Option A'
VOTE2VALUE = 'Option B'
SHOWHOST = 'false'
```

## ☁️ Railway Deployment

This application is configured for easy deployment on [Railway](https://railway.app), a modern cloud platform that simplifies deployment.

### Automatic Deployment (Recommended)

1. **Fork this repository** to your GitHub account

2. **Connect to Railway**
   - Visit [Railway](https://railway.app)
   - Sign up/login with your GitHub account
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository

3. **Add Redis Database**
   - In your Railway project dashboard
   - Click "New" → "Database" → "Add Redis"
   - Railway automatically configures the `REDIS_URL` environment variable

4. **Configure Environment Variables** (Optional)
   - Go to your service settings
   - Add custom environment variables:
     - `VOTE1VALUE`: First voting option (default: "Pizza")
     - `VOTE2VALUE`: Second voting option (default: "Brownie")
     - `TITLE`: Application title (default: "Bake off voting service demo!")

5. **Deploy**
   - Railway automatically builds and deploys your application
   - Your app will be available at the provided Railway URL

### Manual Deployment with Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Run the deployment script**
   ```bash
   chmod +x deploy-railway.sh
   ./deploy-railway.sh
   ```

3. **Follow the interactive prompts**
   - Login to Railway
   - Create a new project
   - Add Redis database manually through the dashboard
   - Deploy the application

### Railway Configuration

The application includes:
- **`railway.json`**: Railway-specific configuration
- **`Dockerfile`**: Production-ready container configuration
- **Health checks**: Automatic health monitoring
- **Auto-restart**: Automatic restart on failure

## 🛠️ Technical Details

### Project Structure
```
Voting-App-Demo/
├── voting-service/           # Main application directory
│   ├── voting-service/       # Python Flask application
│   │   ├── main.py          # Main application file
│   │   ├── config_file.cfg  # Configuration file
│   │   └── templates/       # HTML templates
│   └── Dockerfile           # Container configuration
├── compose.yaml             # Docker Compose configuration
├── Dockerfile               # Production Dockerfile for Railway
├── railway.json             # Railway deployment configuration
├── deploy-railway.sh        # Railway deployment helper script
└── manifests/               # Kubernetes manifests (for AKS deployment)
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection URL | Auto-configured by Railway |
| `REDIS` | Redis hostname | `voting-service-back` (Docker Compose) |
| `VOTE1VALUE` | First voting option | `Pizza` |
| `VOTE2VALUE` | Second voting option | `Brownie` |
| `TITLE` | Application title | `Bake off voting service demo!` |
| `FLASK_ENV` | Flask environment | `production` |

### Ports
- **Frontend**: Port 8080 (local), Port 5000 (Railway)
- **Redis**: Port 6379 (internal)

## 🔧 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Stop any running containers
   docker compose down
   # Or change the port in compose.yaml
   ```

2. **Redis connection issues**
   - Ensure Redis service is running: `docker compose ps`
   - Check logs: `docker compose logs voting-service-back`

3. **Application not loading**
   - Verify all services are running: `docker compose ps`
   - Check application logs: `docker compose logs voting-service-front`

### Development Tips

- Use `docker compose up --build` to rebuild and start in one command
- Add `-d` flag to run in background: `docker compose up -d`
- Use `docker compose exec voting-service-front bash` to access the container shell

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Railway Documentation](https://docs.railway.app/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Redis Documentation](https://redis.io/documentation)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test locally
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).