🚌 Real-Time Bus Coordination System
A location-based web application enabling passengers to request pickups and drivers to view real-time pickup requests on an interactive dashboard.
📋 Overview
Built in 1 week for a local bus company as a proof-of-concept for streamlining passenger-driver coordination. While the company ultimately decided not to implement the system due to business timing, the technical implementation demonstrates modern full-stack development practices and real-time location-based services.
✨ Key Features
Passenger Interface

📍 Real-time location sharing via browser geolocation
🎫 Name or booking ID submission
✅ Instant confirmation feedback
🔒 No account required - frictionless experience

Driver Dashboard

🗺️ Live view of all active pickup requests
🔄 Auto-refresh every 5 seconds
🍎 One-click Apple Maps navigation
✓ Mark pickups as complete
🔐 HTTP Basic Auth protection
⏱️ Automatic request expiration (30 min TTL)

🛠️ Technical Stack
Backend:

FastAPI (Python 3.13) - Modern async web framework
Pydantic - Data validation
Python-dotenv - Environment configuration

Frontend:

Vanilla JavaScript - No framework overhead
HTML5 Geolocation API
CSS3 with animations
Apple Maps integration

Architecture:

RESTful API design
Polling-based real-time updates (5s intervals)
In-memory storage (MVP/demo suitable)
Timezone-aware datetime handling

🚀 Quick Start
Prerequisites

Python 3.11+
Modern web browser with geolocation support

Installation

Clone the repository

bashgit clone <your-repo-url>
cd bus-tracking-system

Install dependencies

bashpip install fastapi uvicorn python-dotenv

Create .env file

bashDRIVER_USERNAME=driver
DRIVER_PASSWORD=your_secure_password_here

Run the application

bashuvicorn main:app --reload

Access the application


Rider page: http://localhost:8000/rider
Driver dashboard: http://localhost:8000/driver (requires auth)

📱 Usage
For Passengers:

Navigate to the rider page
Enter your name or booking ID
Click "Share My Location"
Wait for confirmation

For Drivers:

Navigate to the driver dashboard (login required)
View all active pickup requests with timestamps
Click "Open in Apple Maps" to navigate to passenger
Click "Complete" when pickup is finished

🏗️ Project Structure
bus-tracking-system/
├── main.py              # FastAPI backend with all endpoints
├── templates/
│   ├── rider.html       # Passenger request interface
│   └── driver.html      # Driver dashboard
├── static/
│   └── style.css        # Shared styling with animations
├── .env                 # Environment variables (not in repo)
└── README.md
🔒 Security Features

HTTP Basic Authentication for driver dashboard
Credential management via environment variables
Secrets module for timing-attack-safe comparisons
No passenger data persistence (privacy-first)
30-minute auto-expiration of location data

🎯 Design Decisions
Why FastAPI?

Modern async Python framework
Automatic API documentation (Swagger UI)
Excellent performance for real-time features
Type hints for better code quality

Why polling instead of WebSockets?

Simpler deployment (no persistent connections)
Adequate for 5-second refresh interval
Lower complexity for MVP
Easier to scale horizontally

Why in-memory storage?

Sufficient for proof-of-concept
No pickup data persistence needed (privacy)
Fast read/write operations
Easy to swap for Redis/PostgreSQL in production

🚧 Known Limitations

In-memory storage (data lost on restart)
No historical trip data
Manual driver login (no session management)
Polling-based updates (not true real-time WebSockets)
No mobile native app (browser-based only)

🔮 Future Enhancements

 WebSocket implementation for true real-time updates
 PostgreSQL for persistent storage
 Push notifications when driver is nearby
 Route optimization for multiple pickups
 Driver location tracking
 Historical analytics dashboard
 SMS integration for confirmation
 Mobile app (React Native / Swift)

📊 What I Learned

Implementing real-time location-based services
Managing different user roles and permissions
Working with browser geolocation APIs
Building secure multi-user dashboards
FastAPI best practices and async patterns
Balancing feature scope for MVP delivery
Client requirements vs technical implementation

🤝 Client Context
Built for a local bus company to address passenger pickup coordination challenges. The project successfully demonstrated technical feasibility, though the company opted not to proceed with implementation due to business timing and operational priorities rather than technical limitations.
📝 License
This is a portfolio project. Code provided as-is for demonstration purposes.

👤 Author
Ali Tehrani

GitHub: [@alitehranwi]



Built in 1 week | Modern Python | Production-ready code structure | Real-world problem solving
