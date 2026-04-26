# Project Specification: São Paulo Gas Price Tracker

## 1. System Architecture Overview
* **Target:** Responsive Web Application (React/Next.js preferred).
* **Back-end:** Node.js or Python with a PostgreSQL or MongoDB database.
* **Automation:** Cron-scheduled script using ElevenLabs Conversational AI API.
* **Maps:** Google Maps Platform (Maps SDK for JavaScript, Places API, Distance Matrix API).

## 2. Database Schema (Stations)
The database must store the following fields for each entry:

```json
{
  "station_id": "UUID",
  "name": "String",
  "phone_number": "String (E.164)",
  "address": "String",
  "city": "São Paulo",
  "coordinates": {
    "lat": "Float", 
    "lng": "Float"
  },
  "bandeira": "String (e.g., Shell, Ipiranga)",
  "gasolina_comum_price": "Float",
  "last_verified_at": "ISO8601 Timestamp",
  "status": "Enum (Success, No Data, Pending)"
}

## 3. Data Collection Logic (ElevenLabs Integration)
* **Trigger:** Monthly cron job filtering for `city: "São Paulo"`.
* **AI Agent Configuration:**
    * **Prompt:** "Call `[phone_number]`. Identify yourself briefly and ask: 'Qual o preço da gasolina comum hoje?' Record only the numeric value."
    * **Success Logic:** Parse spoken price (e.g., "Cinco e oitenta") to float (`5.80`). Update `gasolina_comum_price` and `last_verified_at`.
    * **Fallback:** If call fails or price is not retrieved, set `status` to `No Data`.
* **Admin Dashboard:** A simple table view showing all `No Data` entries with a manual "Override Price" input field for developer intervention.

## 4. Front-end Functional Requirements

### A. Search & Geofencing
* **Input:** Google Places Autocomplete search bar.
* **Logic:**
    1.  Validate that the selected address is within the **São Paulo City Bounds**.
    2.  If outside, return Error: *"No data available in this address."*
    3.  If inside, center map and fetch stations within a default **2km radius**.

### B. Radius & Filtering
* **Dynamic Radius:** A slider or toggle allowing values from **1km to 5km**.
* **Brand Logic:** Store the brand (`bandeira`), but **do not** implement a brand filter.

### C. Map Visualization (Google Maps API)
* **Marker Logic:**
    * **Function:** `getCheapestStation(radius_results)`
    * **Styling:** Cheapest station marker = `#00FF00` (Green). All other markers = `#FF0000` (Red).
* **InfoWindow (On Click):** Display `Name`, `Price`, `Bandeira`, `Last Verified Date`, and a Google Maps button linking to: `https://www.google.com/maps/dir/?api=1&destination=LAT,LNG`.
* **Behavior:** Show all markers in the radius immediately. **No** auto-zoom or auto-pan to the cheapest pin.

### D. Sidebar Component
* **Sort Logic:** `stations.sort((a, b) => a.price - b.price)`.
* **Card Contents:** `Name`, `Brand`, `Price`, `Distance` (calculated via `google.maps.geometry.spherical.computeDistanceBetween`).
* **State Management:** When a sidebar card is clicked, trigger `Marker.setAnimation(google.maps.Animation.BOUNCE)` or change the color of the corresponding map pin.

## 5. UI/UX Constraint Checklist
- [ ] **Public Access:** No auth headers or user sessions required.
- [ ] **Mobile First:** Sidebar must collapse to a bottom sheet on mobile devices.
- [ ] **Brand Visibility:** Hide brand names on map markers; reveal only inside the InfoWindow or Sidebar.
- [ ] **Timestamp:** Every price display must be accompanied by the `last_verified_at` string (Format: **DD/MM/YYYY**).