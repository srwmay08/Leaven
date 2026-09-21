# Leaven

Leaven is a full-stack web application designed to help you manage recipes, track ingredients, organize market runs, and keep tabs on your grocery expenses and receipts. 

## 🛠 Tech Stack

*   **Backend:** Python (FastAPI/Flask/etc. - *update with your specific framework*), SQLite/PostgreSQL (*update database*)
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript

## ✨ Features

*   **Recipe Management:** Create, view, and organize your favorite recipes.
*   **Ingredient Tracking:** Keep track of what ingredients you have and what you need.
*   **Market & Expense Tracking:** Log trips to the market and track your spending.
*   **Receipts:** Manage and review your grocery receipts.

## 📁 Project Structure

The project is divided into two main directories:

*   `/backend`: Contains the Python backend API, database configuration (`core/database.py`), data models (`models/`), and API routes (`routers/`).
*   `/frontend`: Contains the user interface, including HTML pages, stylesheets (`css/`), and client-side logic (`js/`).

## 🚀 Getting Started

### Prerequisites

*   Python 3.x installed on your machine.
*   Git

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Seed the database (if applicable):
   ```bash
   python seed_data.py
   python seed_recipes.py
   ```
5. Start the backend server:
   ```bash
   # Example for FastAPI:
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Serve the frontend files. You can use Python's built-in HTTP server:
   ```bash
   python -m http.server 8000
   ```
3. Open your browser and navigate to `http://localhost:8000`.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request