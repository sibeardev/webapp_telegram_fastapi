# WebApp Telegram FastAPI

## Overview

This project is a web application skeleton for building a Telegram bot using FastAPI and Python Telegram Bot. It includes integration with MongoDB as the database backend.

## Features

- **FastAPI Backend**: Utilizes FastAPI framework for building the web application backend.
- **Python Telegram Bot**: Integrates Python Telegram Bot library for interacting with the Telegram API.
- **MongoDB Database**: Uses MongoDB as the database backend for storing bot data.
- **Skeleton Structure**: Provides a basic structure to kickstart the development of a Telegram bot web application.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/sibeardev/webapp_telegram_fastapi.git
```

2. Navigate into the cloned directory: 

```bash
cd webapp_telegram_fastapi
```

3. Install dependencies: 
   - `pip install virtualenv`
   - `python -m venv .venv` (create a virtual environment)
   - `source .venv/bin/activate` (activate the virtual environment)
   - `pip install -r requirements.txt`

4. Set up environment variables: Create a `.env` file and define the necessary environment variables.

```plaintext
   TELEGRAM_TOKEN=  # Telegram API Token
   MONGODB_URL=mongodb://localhost:27017  # MongoDB connection URL
   X_TOKEN=fake-super-secret-token  # Additional secret token
   WEBHOOK_URL= # Webhook URL
```

Note: For testing purposes, you can use [ngrok](https://ngrok.com/docs/getting-started/) to expose your local server to the internet. After installing ngrok, run ngrok http 8000 in a separate terminal window. Then, insert the ngrok URL generated for your server as the value for the WEBHOOK_URL variable in your .env file.

5. Start the application: `docker-compose up`

## Contributing

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License.

