# Deployment Checklist

Follow these steps after committing changes:

- [ ] Redeploy backend on Render (ensure `PORT` binding is used by the service)
- [ ] Redeploy frontend on Vercel (ensure `VITE_API_URL` environment variable is set to the backend URL)
- [ ] Test login/register from Vercel URL in browser DevTools and confirm no CORS/Network Error
- [ ] If OPTIONS requests still return 400, check Render service logs for proxy/port binding errors

Helpful commands (local test):
```bash
cd frontend
npm run build
npm run preview
# open http://localhost:4173 and test auth flows
```
# Deployment Checklist

- [ ] Redeploy backend on Render (ensure updated `backend/app/main.py` deployed)
- [ ] Redeploy frontend on Vercel (ensure `VITE_API_URL` env var set in Vercel project)
- [ ] Test login/register from Vercel and confirm no CORS/Network Error in DevTools
- [ ] If CORS errors persist, verify Render ingress and any proxies are forwarding OPTIONS correctly

Notes:
- Local test: `cd frontend && npm run build && npm run preview`
- Ensure `frontend/.env` contains `VITE_API_URL` pointing at the Render API URL for local preview.
