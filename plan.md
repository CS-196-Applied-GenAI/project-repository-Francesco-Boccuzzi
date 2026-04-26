# Backend Implementation Plan: São Paulo Gas Price Tracker

This plan breaks down the backend development into iterative, testable chunks. Each step is designed to be small enough for safe implementation but significant enough to provide value.

## Phase 1: Environment & Core Data Model
**Goal:** Establish the foundation and the "Source of Truth."

### Step 1.1: Project Initialization & Database Setup
* Initialize a Node.js/Express (or Python/FastAPI) project with TypeScript/Type safety.
* Setup a PostgreSQL database (using an ORM like Prisma or SQLAlchemy).
* Implement the `Station` schema as defined in the spec (UUID, name, phone, address, coordinates, price, status).
* **Test:** Run a migration and manually insert/retrieve a record using a script.

### Step 1.2: Seed Data Acquisition
* Create a seeding script to import the initial list of São Paulo gas stations.
* Ensure all stations are flagged with `status: "Pending"` and `city: "São Paulo"`.
* **Test:** Verify database count matches the expected number of São Paulo stations.

---

## Phase 2: The API Layer (Read/Write)
**Goal:** Enable communication between the frontend and the database.

### Step 2.1: Spatial Query Endpoint
* Implement a `GET /api/stations` endpoint.
* Logic: Accept `lat`, `lng`, and `radius` (1-5km).
* Filter stations using the Haversine formula (or PostGIS `ST_DWithin` if using Postgres) to return stations within the bounds.
* **Test:** Use Postman/Curl to query a specific lat/lng and verify only nearby stations are returned.

### Step 2.2: Admin Override API
* Implement a `PATCH /api/stations/:id` endpoint.
* Logic: Allow manual updates to `gasolina_comum_price` and `status`.
* Automatically update `last_verified_at` to the current timestamp on save.
* **Test:** Update a "No Data" station and verify the timestamp and price update correctly.

---

## Phase 3: AI Automation (ElevenLabs Integration)
**Goal:** Automate the phone-based price collection.

### Step 3.1: ElevenLabs Conversational Agent Setup
* Configure the ElevenLabs Agent via their SDK/API.
* Define the System Prompt: "You are an automated assistant. Call the gas station, ask 'Qual o preço da gasolina comum hoje?', and record the response."
* **Test:** Trigger a single test call to a controlled number to verify the agent speaks the correct script.

### Step 3.2: Voice Response Parsing & Logic
* Implement a webhook or post-call processing logic to extract the numeric price from the ElevenLabs transcript.
* Create a service that maps the AI output to a float value.
* Handle "Failures": If the transcript implies a refusal or silence, set status to `No Data`.
* **Test:** Mock AI transcripts (e.g., "O preço é cinco e oitenta") and verify the parser outputs `5.80`.

### Step 3.3: The Monthly Cron Job
* Implement a scheduled task (using `node-cron` or `celery`) that runs on the 1st of every month.
* Logic: Iterate through all stations with `city: "São Paulo"`, trigger the ElevenLabs call, and update the DB based on the response.
* Include rate-limiting to avoid overwhelming the ElevenLabs API or the gas stations.
* **Test:** Trigger the cron manually for a small batch (3-5 stations) and verify DB updates.

---

## Phase 4: Geofencing & Refinement
**Goal:** Finalize the business logic constraints.

### Step 4.1: City Boundary Validation
* Implement a utility function to check if a coordinate is within the São Paulo city polygon (using a GeoJSON boundary file).
* Integrate this check into the search flow to return the specified error message if out of bounds.
* **Test:** Test with coordinates for Evanston, IL (Fail) and Avenida Paulista (Pass).

### Step 4.2: Sorting & Distance Calculation
* Ensure the API returns the calculated distance from the user's input point for each station.
* Add logic to identify the `min(price)` in the result set to help the frontend highlight the "Cheapest" marker.
* **Test:** Verify the "cheapest" flag is correctly identified in a multi-station response.