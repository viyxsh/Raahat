# RAAHAT — ngrok Setup Guide
## Task 5: Share a live demo URL with your reviewer

ngrok creates a **public HTTPS tunnel** to your local backend so your supervisor
can open the API or the dashboard on *their* phone/laptop without needing to be
on the same Wi-Fi.

---

## Step 1 — Install ngrok

```
# Download the Windows ZIP from https://ngrok.com/download
# Extract ngrok.exe to a folder you can run from, e.g. C:\ngrok\ngrok.exe
```

Or if you have Chocolatey:
```
choco install ngrok
```

Or with winget:
```
winget install ngrok.ngrok
```

---

## Step 2 — Sign up (free) and authenticate

1. Go to https://dashboard.ngrok.com/signup → sign up with Google/GitHub.
2. Copy your **Authtoken** from https://dashboard.ngrok.com/get-started/your-authtoken.
3. Run once:
```
ngrok config add-authtoken <YOUR_AUTHTOKEN>
```

---

## Step 3 — Start the tunnel

With your **backend** already running on port 8000:

```
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
```

Copy the `https://abc123.ngrok-free.app` URL — this is your **public API URL**.

---

## Step 4 — Update the frontend to use the ngrok URL

In `frontend/.env` (create if it doesn't exist):
```
VITE_API_BASE=https://abc123.ngrok-free.app
```

Restart the frontend dev server:
```
npm run dev
```

Now the dashboard and map will fetch tickets from the public URL.

---

## Step 5 — Share with your reviewer

Send them:
- **API (Swagger docs)**:  `https://abc123.ngrok-free.app/docs`
- **Dashboard**:  `http://localhost:5173`  (still local — for your own screen)
- **Test a ticket** (reviewer can do this from their phone):
  ```
  POST https://abc123.ngrok-free.app/simulate/sms
  Body: {"message":"NEED WATER","phone":"+910000000000","lat":23.21,"lng":77.41}
  ```

---

## Step 6 — (Optional) Also tunnel the frontend

Open a **second terminal**:
```
ngrok http 5173
```

Now send the reviewer the frontend ngrok URL too — they can open the full dashboard on their phone.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ERR_NGROK_108` (tunnel limit) | Free plan allows 1 tunnel at a time. Stop the backend tunnel before opening a frontend one, or upgrade to free static domain. |
| CORS errors after switching to ngrok URL | Make sure `VITE_API_BASE` is set and frontend was restarted. Also confirm backend `CORSMiddleware` has `allow_origins=["*"]`. |
| Reviewer gets "Tunnel not found" | ngrok session expired (free tier ~2h). Re-run `ngrok http 8000` and send new URL. |
| Reviewer needs to accept ngrok warning page | First visit shows a warning page on free plan. Click "Visit Site". To skip, get a free static domain in ngrok dashboard. |

---

## Demo Day Checklist

```
[ ] Backend running:     uvicorn app.main:app --reload --port 8000
[ ] ngrok running:       ngrok http 8000
[ ] Frontend running:    npm run dev  (with VITE_API_BASE set)
[ ] Seeder ready:        python demo/run_demo.py --base https://abc123.ngrok-free.app
[ ] Integration tests:   pytest demo/integration_tests/ -v
[ ] Screenshots folder:  demo/screenshots/ (capture after seed)
```
