# FitVison-AI-powered-Fitness-Assistant

**FitVision** is an AI-powered fitness platform designed to combine secure user management with computer vision-based workout tracking and personalized fitness assistance.

## Features

- Secure Signup & Login with JWT Authentication
- Email Verification
- User Profile Management
- Real-time Exercise Tracking
- Push-up / Workout Rep Counting
- Pose Detection using MediaPipe
- Posture Analysis using OpenCV
- AI-based Fitness Recommendations
- Microservice-oriented Backend Architecture

## Tech Stack

**Backend**
- Java
- Spring Boot
- Spring Security
- JWT
- MySQL

**AI / Computer Vision**
- Python
- OpenCV
- MediaPipe

**Architecture**
- REST APIs
- Microservices
- Docker

## Project Architecture

```text
FitVision
│
├── Auth Service
│   └── Spring Boot + MySQL + JWT
│
├── Workout Tracking Service
│   └── Python + OpenCV + MediaPipe
│
└── AI Recommendation Service
    └── Python / Machine Learning
```

## Goal

FitVision aims to provide a smart fitness experience where users can track exercises, analyze posture, monitor workout performance, and receive intelligent fitness recommendations.
