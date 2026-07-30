# The Debuggers — GCE DevClub

Premium, responsive vanilla HTML/CSS/JavaScript landing page and registration form for Gaya College of Engineering's coding club.

## Project structure

- `frontend/` — static landing page and registration form
- `backend/` — FastAPI registration API and backend services

## Frontend

Open `frontend/index.html` directly in a browser. No dependencies or build step are required.

## Backend

The backend is a Python FastAPI application in `backend/`.

### Local development

1. Change into the backend folder:
   ```bash
   cd backend
   ```
2. Copy `.env.example` to `.env` and set the required environment variables:
   - `RESEND_API_KEY`
   - `RESEND_FROM_EMAIL`
   - `NOTIFICATION_EMAIL`
   - `ALLOWED_ORIGINS`
3. Install dependencies with `uv` and run the app:
   ```bash
   uv sync
   uv run uvicorn app.main:app --reload
   ```

The API is available at `http://127.0.0.1:8000`.

### Docker

Build and run the backend container from the `backend/` directory:

```bash
cd backend
docker build -t the-debuggers-backend .
docker run -p 8000:8000 --env-file .env the-debuggers-backend
```

The API will be available at `http://0.0.0.0:8000` inside the container.

### Deploying to Render with Docker

1. Create a Render Web Service and choose "Docker" or specify `backend/Dockerfile` as the Dockerfile path.
2. Set the service root directory to `backend` if Render asks for a build context.
3. Add required environment variables in the Render dashboard:
   - `DATABASE_URL`
   - `RESEND_API_KEY`
   - `RESEND_FROM_EMAIL`
   - `NOTIFICATION_EMAIL`
   - `ALLOWED_ORIGINS`
4. Render will build the Docker image using `backend/Dockerfile` and run the container on port `8000`.

No code changes are needed for Render deployment. The app reads configuration from environment variables and supports production container deployment using the optimized Docker image.

### Deployment

This repository is now configured for Docker deployment on Render. Use the `backend/Dockerfile` for container builds and keep launcher commands as:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```
