# Quick Start Guide - Phase 2

Get the São Paulo Gas Price Tracker running in 5 minutes.

## Prerequisites

- Python 3.9+ 
- Node.js 14+ with npm
- Google Maps Embed API Key (free - [get here](https://console.cloud.google.com/))

## 🚀 Quick Start

### Terminal 1: Backend

```bash
cd backend

# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python -m uvicorn main:app --reload
```

✅ Backend ready: `http://localhost:8000`
🔗 API Docs: `http://localhost:8000/docs`

### Terminal 2: Frontend

```bash
cd frontend

# Install dependencies
npm install

# Setup environment (with your API key)
cat > .env << EOF
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_GOOGLE_MAPS_API_KEY=AIzaSyD5G-tz32Qc5ZA4FqnO1ChEeq2ShelK-vs
EOF

# Start development server
npm start
```

✅ Frontend ready: `http://localhost:3000`

## 🧪 Test It

1. **Open browser:** `http://localhost:3000`
2. **Enter coordinates:**
   - Latitude: `-23.5505`
   - Longitude: `-46.6561`
   - Radius: `2.0 km`
3. **Click Search**
4. **See results:**
   - Embedded map centered on search location
   - Sidebar shows stations sorted by price
   - Green "Cheapest" badge highlights lowest price
   - Click "Navigate" buttons to open in Google Maps

## 📝 Sample API Call

```bash
# Search stations
curl "http://localhost:8000/api/stations?latitude=-23.5505&longitude=-46.6561&radius_km=2.0"

# Update price (replace {id} with actual UUID)
curl -X PATCH "http://localhost:8000/api/stations/{station_id}" \
  -H "Content-Type: application/json" \
  -d '{"gasolina_comum_price": 6.50, "status": "Success"}'
```

## 📚 Full Documentation

- **[PHASE2_IMPLEMENTATION.md](./PHASE2_IMPLEMENTATION.md)** - Complete setup & testing guide
- **[PHASE2_SUMMARY.md](./PHASE2_SUMMARY.md)** - What was implemented
- **[frontend/README_MAPS_EMBED.md](./frontend/README_MAPS_EMBED.md)** - Maps Embed API guide
- **[backend/PHASE1_SETUP.md](./backend/PHASE1_SETUP.md)** - Database setup

## 🐛 Troubleshooting

### Backend won't start
```bash
# Wrong directory?
cd backend

# Missing dependencies?
pip install -r requirements.txt

# Port in use?
python -m uvicorn main:app --port 8001
```

### Frontend shows blank page
```bash
# Missing dependencies?
cd frontend && npm install

# API key in .env?
# Check: cat .env

# API not responding?
# Check backend is running: http://localhost:8000/docs
```

## 🎯 Features at a Glance

### Backend (FastAPI)
- ✅ Spatial search with Haversine distance
- ✅ Admin price override endpoint
- ✅ CORS enabled for frontend
- ✅ Swagger API documentation

### Frontend (React)
- ✅ Location search with coordinate input
- ✅ Embedded Google Maps
- ✅ Price-sorted station list
- ✅ Navigation links to Google Maps
- ✅ Mobile responsive design
- ✅ Material-UI components
- ✅ **FREE** - Uses Maps Embed API

## 🌍 Deployment

When ready to deploy:

1. **Backend:**
   - Set `DATABASE_URL` to production PostgreSQL
   - Set `REACT_APP_API_BASE_URL` for production frontend URL
   - Use `gunicorn` instead of dev uvicorn

2. **Frontend:**
   - Run `npm run build`
   - Deploy `build/` folder to web host
   - Update `REACT_APP_API_BASE_URL` for production backend

## 📞 Support

Check the full documentation files for detailed information on:
- Architecture design
- Component structure
- API specifications
- Testing procedures
- Deployment checklist

**Happy coding! 🚀**

