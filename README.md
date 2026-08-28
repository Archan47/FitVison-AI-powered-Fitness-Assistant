# FitVison-AI-powered-Fitness-Assistant

# FitVision

**FitVision** is an AI-powered fitness platform that combines secure user authentication, computer vision, workout tracking, and intelligent fitness assistance in a modular backend architecture.

The project is designed to track exercises in real time, analyze body posture, count workout repetitions, and later provide personalized recommendations based on user activity.

## Features

- Secure user registration and login
- JWT-based authentication and authorization
- Email verification for account activation
- User profile management
- Real-time exercise tracking
- Push-up repetition counter
- Body landmark detection
- Joint angle calculation
- Workout posture analysis
- Visual pose skeleton overlay
- Planned personalized workout recommendations
- Modular service-based architecture

## Tech Stack

### Backend

- Java
- Spring Boot
- Spring Security
- Spring Data JPA
- JWT Authentication
- MySQL
- REST APIs

### Computer Vision & AI

- Python
- OpenCV
- MediaPipe
- NumPy
- Machine Learning

### DevOps & Tools

- Docker
- Git & GitHub
- Postman
- IntelliJ IDEA
- PyCharm

## Architecture

```text
                        FitVision
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Java Backend                Python Services
              │                           │
      ┌───────┴────────┐          ┌───────┴─────────┐
      │                │          │                 │
 Auth Service     User Profile   Workout Tracker   AI Advisory
      │                           │
 Spring Boot                  OpenCV + MediaPipe
      │                           │
     JWT                     Pose Detection
      │                           │
    MySQL                 Exercise Counting
```

## Authentication Service

The authentication service is built using **Spring Boot and Spring Security**.

It currently handles:

- User signup
- User login
- Password encryption using BCrypt
- JWT token generation
- Protected API access
- Email verification status
- User profile information

Users are initially registered as unverified and are allowed to access the platform after successful account verification.

## Workout Tracking

The workout tracking module uses **OpenCV and MediaPipe Pose Landmarker** to detect body landmarks from video frames.

It can:

- Detect body joints
- Draw pose connections
- Calculate joint angles
- Identify exercise stages
- Count repetitions
- Track movement in real time

The current implementation includes a working **push-up counter**, with additional exercises planned for future versions.

## Planned Features

- Squat counter
- Multiple exercise tracking
- Incorrect posture detection
- Exercise form feedback
- Workout history
- Progress analytics
- Personalized workout recommendations
- AI-based fitness advisory
- API Gateway
- Frontend dashboard
- Dockerized service deployment

## Project Goal

The goal of FitVision is to build a complete intelligent fitness ecosystem where computer vision can understand exercise movements and provide useful real-time feedback while a secure backend manages users, workout data, and future AI recommendations.

## Status

🚧 **Currently under active development**

- ✅ Authentication system
- ✅ JWT security
- ✅ User registration and login
- ✅ Push-up tracking
- ✅ Pose landmark detection
- ✅ Exercise repetition counting
- 🔄 Profile and verification improvements
- 🔄 Additional exercises
- 🔄 AI recommendation system
- 🔄 Frontend integration
