# Overview

This is a Telegram bot that automatically generates AI-themed educational content for a Telegram channel. The bot creates 20 posts daily between 07:00-21:00 UTC, with each post containing AI-related text content in Uzbek language and accompanying generated images. The bot uses Google's Gemini AI models for both text generation (Gemini 1.5 Flash) and image generation (Gemini 2.5 Flash Image Preview), with a fallback mechanism to create text-based images using PIL when AI image generation fails.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Components

**Bot Engine**: Single-threaded Python application using the `schedule` library for time-based post generation. Runs continuously with 42-minute intervals between posts during operational hours.

**Content Generation Pipeline**: Two-stage content creation process:
1. Text generation using Gemini 1.5 Flash for educational AI content in Uzbek
2. Image generation using Gemini 2.5 Flash Image Preview with "nano banana" visual metaphors

**Fallback System**: When AI image generation fails (due to API limits or preview model instability), the system automatically generates professional text-based images using PIL with typography rendering.

**Error Handling**: Retry mechanism with exponential backoff for API calls, comprehensive exception handling for all external service interactions.

**Deployment Architecture**: Designed as a background worker service for Render.com platform, using environment variables for secure configuration management.

## Design Patterns

**Retry Pattern**: Implements exponential backoff retry logic for handling transient API failures and rate limiting.

**Fallback Pattern**: Graceful degradation when primary image generation service is unavailable, ensuring 100% post delivery reliability.

**Environment Configuration**: All sensitive data (API keys, tokens) loaded through environment variables for security and deployment flexibility.

# External Dependencies

## AI Services
- **Google Generative AI**: Primary content generation service using Gemini models
  - Text: `gemini-1.5-flash-latest` for content generation
  - Image: `gemini-2.5-flash-image-preview` for visual content creation

## Messaging Platform
- **Telegram Bot API**: Content delivery platform for publishing generated posts to channels

## Python Libraries
- **Flask**: Web framework for API endpoints and health checks
- **google-generativeai**: Google AI SDK for content generation
- **Pillow (PIL)**: Image processing and fallback text-to-image rendering
- **requests**: HTTP client for API communications  
- **schedule**: Task scheduling for automated post timing

## Replit Environment Setup
- **Port Configuration**: Flask app runs on port 5000 (required for Replit)
- **Host Configuration**: Binds to 0.0.0.0 to allow proxy access
- **Environment Variables**: Gracefully handles missing API keys during development
- **Health Endpoints**: `/health`, `/status`, `/test_post` for monitoring and testing

## Required Environment Variables
- `GOOGLE_API_KEY`: Google AI Studio API key for Gemini models
- `TELEGRAM_BOT_TOKEN`: Bot token from @BotFather on Telegram
- `TELEGRAM_CHANNEL_ID`: Target channel ID or username (e.g., @ai_learn_uz)