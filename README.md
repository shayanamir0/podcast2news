
---

## Demo

Production URL: [https://podcast2news.vercel.app](https://podcast2news.vercel.app)

---

## Tech Stack

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** FastAPI (Python)
- **APIs:** OpenAI, Deepgram
- **Deployment:** Vercel (frontend), Railway (backend), Docker (optional)

---

## Quick Local Start

For local development, simply run:

```bash
./start_backend.sh
./start_frontend.sh
```

> **Note:** Main instructions below are for production deployment/hosting.

---

## Deployment & Hosting

### Frontend (Vercel)

1. **Push the `frontend/` directory to a GitHub repository.**
2. **Import the repository into [Vercel](https://vercel.com/).**
3. **Set the environment variable in the Vercel dashboard:**

   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.up.railway.app
   ```

   Replace with your actual backend URL from Railway.

4. **Deploy!**  
   Vercel will handle the build and deployment automatically.

---

### Backend (Railway)

1. **Push the `backend/` directory to a GitHub repository.**
2. **Create a new project on [Railway](https://railway.app/).**
3. **Connect your GitHub repository.**
4. **Set the following environment variables in the Railway dashboard:**

   ```
   OPENAI_API_KEY=your_openai_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   ALLOWED_ORIGINS=https://[your-domain].vercel.app
   ENVIRONMENT=production
   HOST=0.0.0.0
   PORT=8000
   ```

   - Replace `your_openai_api_key` and `your_deepgram_api_key` with your actual API keys.
   - `ALLOWED_ORIGINS` should include your Vercel frontend URL.

5. **Deploy the backend.**
6. **Copy the public URL provided by Railway and use it as `NEXT_PUBLIC_API_URL` in your Vercel frontend.**

---

## Docker

You can also run both frontend and backend using Docker Compose for local development or self-hosting:

```bash
docker-compose up --build
```

- Edit `docker-compose.yml` or `docker-compose.prod.yml` to set environment variables as needed.

---
