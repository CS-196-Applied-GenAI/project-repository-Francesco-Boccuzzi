# Frontend Specification: GasPriceTracker.com

## 1. Overall Visual Identity & Design System
* **Aesthetic:** Light mode, minimalist, and clean. 
* **Color Palette:** Pastel colors. The interface should feel inviting and modern without being visually overwhelming.
* **Responsiveness:** Desktop-first. Mobile responsiveness is out of scope for this phase; the layout should be optimized for a standard computer screen.
* **Styling Implementation:** Developer's choice (e.g., plain CSS, Tailwind, or a UI library), as long as it adheres to the light/pastel minimalist aesthetic and works within the existing React setup.

## 2. Page Structure & Components

### Page 1: Landing Page
* **Layout:** All elements must be perfectly centered vertically and horizontally on the screen.
* **Text Content:**
    * **Welcome Message & Description:**
        > Welcome to GasPriceTracker.com!
        > 
        > Input your address, choose a range and find the gas stations with the cheapest prices near you!
        > Don't hesitate. Experiment and start saving!
* **Call to Action (CTA) Button:** * **Text:** "Start Searching"
    * **Action:** Clicking this routes the user to the Search Page.

### Page 2: Search Page
* **Navigation:** Include a simple "Back" button somewhere unobtrusive (e.g., top left) that routes the user back to the Landing Page.
* **Layout:** The core feature is a horizontal "search bar" style layout (similar to Zillow), containing three inline elements:
    1.  **Address Input (Dropdown):**
        * A text input field that acts as a dropdown menu.
        * *Functionality:* Hardcoded placeholder. 
        * *Data:* Populate the dropdown strictly with these four options:
            * Parque do Ibirapuera
            * MASP, Avenida Paulista
            * Allianz Parque
            * Universidade de São Paulo
    2.  **Range Selector (Dropdown):**
        * A standard dropdown menu with three specific options: `1km`, `2km`, and `3km`.
    3.  **"Go" Button:**
        * A button placed at the end of the horizontal search bar to submit the query.

## 3. Interaction & Error Handling (Placeholder Logic)
* **Database/Backend Integration:** Currently out of scope. Do not attempt to fetch real gas prices or connect to the database yet.
* **"Go" Button Behavior:**
    * When the user clicks "Go", the system should bypass form validation (it does not matter if the address or range fields are empty).
    * **Action:** Immediately render the text `"service not available"`.
    * **Placement:** This text must appear directly beneath the horizontal search bar. It should not be a browser alert popup or an overlay.