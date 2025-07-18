# SavorSync API

A FastAPI-based backend for recipe generation, management, and admin operations, using MongoDB for storage.

## Features

- Generate recipes using AI
- Store and retrieve recipes
- Admin endpoints for recipe management

---

## Prerequisites

- **Python 3.10+**
- **MongoDB** (local or remote instance)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd SavorSync_API
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
MONGODB_URI= your_mongodb_cluster_uri  # Or your MongoDB connection string
ADMIN_API_KEY=your_admin_api_key       # Set a strong secret for admin endpoints
# Optional LangSmith tracking (for recipe generation)
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=savor-sync-recipe-generation
```

---

## Running the API

Start the FastAPI server in development mode:

```bash
fastapi dev app/main.py
```

- The API will be available at: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

---

## Populating the Database (Optional)

To auto-generate and populate recipes for various cuisines, run:

```bash
python populate_database.py
```

This script uses the `/generation/recipe` endpoint and requires `ADMIN_API_KEY` in your `.env`.

---

## API Usage

### Public Endpoints

- `GET /recipes/` — List all recipes
- `GET /recipes/{recipe_id}` — Get a recipe by ID

### Recipe Generation (Admin Only)

- `POST /generation/recipe` — Generate a new recipe using AI
  - Requires `admin-api-key` header (set to your `ADMIN_API_KEY`)
  - Request body example:
    ```json
    {
      "recipe_name": "Chicken Tikka Masala",
      "cuisine": "Indian",
      "save_to_database": true
    }
    ```

### Admin Endpoints (Require `admin-api-key` header)

- `POST /admin/recipes` — Create a recipe
- `PUT /admin/recipes/{recipe_id}` — Update a recipe
- `DELETE /admin/recipes/{recipe_id}` — Delete a recipe
- `GET /admin/recipes` — List all recipes (admin view)
