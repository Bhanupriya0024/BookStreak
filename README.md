# 📚 BookStreak

## Project Description

BookStreak is a dynamic web application for tracking reading progress. Users can add books, update pages read, edit book details, mark books as completed, and remove books. The application also displays reading statistics, daily reading goals, and reading streaks.

The application is built using Python Flask with SQLite and is delivered through GitHub and a CI/CD pipeline.

## Features

* Add a new book through a form
* Update reading progress
* Edit book details
* Delete books
* Track pages read
* Track completed books
* Calculate reading streak
* Daily reading goal
* Home page displaying data from the server
* JSON API: `/api/books`
* Health check: `/health`
* Footer displaying the running commit ID
* Automated tests
* flake8 lint check

## Technology Stack

* **Language:** Python 3.12
* **Framework:** Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, Jinja2
* **Testing:** unittest
* **Linting:** flake8
* **Version Control:** Git and GitHub
* **CI/CD:** GitHub Actions
* **Deployment:** Render
* **Server:** Gunicorn

## Project Structure

```text
BookStreak/
├── .github/
│   └── workflows/
│       └── ci.yml
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── app.py
├── test_app.py
├── requirements.txt
├── Procfile
├── README.md
└── .gitignore
```

## Run Locally

### 1. Create the virtual environment

```powershell
python -m venv venv
```

### 2. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the application

```powershell
python app.py
```

Open the application at:

```text
http://127.0.0.1:5000
```

## Testing

Run the automated tests:

```powershell
python -m unittest test_app.py
```

Run the lint check:

```powershell
flake8 app.py test_app.py
```

The project contains at least three automated tests covering the home page, JSON API, and health-check route.

## API Routes

### Books API

```text
GET /api/books
```

Returns the books stored in the application in JSON format.

### Health Check

```text
GET /health
```

Returns:

```json
{
    "status": "ok"
}
```

## Commit ID

The application footer displays the running commit ID using the `RENDER_GIT_COMMIT` environment variable.

This allows the deployed version to be identified from the live application.

## CI/CD Pipeline

The planned CI/CD pipeline follows this flow:

```text
Git Push
    ↓
Lint & Test
    ↓
Build
    ↓
Deploy
    ↓
Live Application
    ↓
Verify /health + Commit ID
```

### Pipeline Stages

1. **Lint and Test**

   * Install dependencies
   * Run flake8
   * Run automated tests

2. **Build**

   * Build the application
   * Verify that the application and `/health` route work

3. **Deploy**

   * Runs only after the previous stages pass
   * Deployment is triggered on pushes to `main`

4. **Verify**

   * Open the live application
   * Check the `/health` route
   * Confirm the commit ID displayed in the footer

## Git Workflow

The project uses Git branches and pull requests for feature development.

```text
main
 │
 └── feature branch
        │
        ├── Make changes
        ├── Run tests
        ├── Run lint
        ├── Commit
        └── Pull Request
                │
                └── Merge → main
```

## Failure Demonstration

A test will be intentionally broken on a branch and pushed to GitHub.

The CI pipeline should fail at the test stage, preventing the deployment stage from running.

After fixing the test, the change will be merged into `main`, producing a successful pipeline run.

## Success Demonstration

After a successful deployment:

* GitHub Actions shows a green pipeline
* The live application is accessible
* The footer displays the latest deployed commit ID

## Project Objective

The objective of BookStreak is to demonstrate a complete development and delivery workflow using:

* Dynamic web application development
* Git version control
* Branches and pull requests
* Automated testing
* Linting
* CI/CD using GitHub Actions
* Cloud deployment using Render
* Health-check verification

## Author

**Bhanupriya Jena**
