# WebApp Telegram FastAPI

## Overview

This project is a full-stack web application skeleton for building a Telegram WebApp integrated with a FastAPI backend and MongoDB database.
It includes a SvelteKit frontend that runs as a Telegram WebApp and interacts with the backend via REST API.

## Features

#### Backend

- **FastAPI Framework** – High-performance Python web framework.
- **Python Telegram Bot** – Integration with the Telegram Bot API.
- **MongoDB Database** – Stores user and session data.
- **JWT Authentication** – Used for secure user authorization.
- **Async Webhooks** – Supports webhook integration for Telegram.

#### Frontend

- **SvelteKit** – Modern reactive framework for building single-page apps.
- **Telegram WebApp SDK (@twa-dev/sdk)** – Integration with Telegram’s native UI.
- **Dynamic Theming** – Adapts automatically to Telegram’s light/dark theme.
- **TailwindCSS** – Utility-first CSS framework for consistent UI.
- **REST API Integration** – Communicates with FastAPI backend via /api/\* routes.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/sibeardev/webapp_telegram_fastapi.git
cd webapp_telegram_fastapi
```

2. Environment Setup

Create `.env` in backend/ directory:

```plaintext
   MONGO_DSN=mongodb://mongo:27017
   SECRET_KEY=super_secret_key

   TELEGRAM__TOKEN=You can obtain a bot token from @BotFather in Telegram.
   TELEGRAM__SECRET="secrettelegram"
   TELEGRAM__ADMINS=[123456789]

   EXTERNAL_URL=https://example.com
```

> Note: For testing purposes, you can use [ngrok](https://ngrok.com/docs/getting-started/) to expose your local server to the internet. After installing ngrok, run ngrok http 8000 in a separate terminal window. Then, insert the ngrok URL generated for your server as the value for the EXTERNAL_URL variable in your .env file.

3. Running with Docker

```bash
docker-compose up --build
```

This will:

- Build the SvelteKit frontend (Node.js 20)
- Build the FastAPI backend (Python 3.12)
- Run a MongoDB instance
- Serve the built frontend via FastAPI at /

## Telegram Integration

Create a Telegram Bot using @BotFather
Set the WebApp URL in your bot configuration to your deployed app (e.g. https://yourdomain.com)
Launch the bot and open the WebApp directly in Telegram.

## Frontend Theming

The application automatically applies Telegram’s dynamic theme colors using CSS variables:

```css
.tg-bg {
  background-color: var(--tg-theme-bg-color);
}
.tg-text {
  color: var(--tg-theme-text-color);
}
.tg-button-bg {
  background-color: var(--tg-theme-button-color);
}
.tg-button-text {
  color: var(--tg-theme-button-text-color);
}
...
```

These styles are defined in src/app.css and imported globally in +layout.svelte.

## License

This project is licensed under the MIT License.
