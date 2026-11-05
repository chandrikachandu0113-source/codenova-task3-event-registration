# CodeNova Task 3 – Event Registration Platform

## Project Overview

A beginner-friendly Event Registration Platform developed for the CodeNova Full Stack Development Internship – Batch 01.

The application allows users to explore upcoming events and register online. An admin dashboard helps view participant registrations.

## Features

- Display upcoming events
- Online event registration
- Registration form validation
- Duplicate registration prevention
- Event seat availability tracking
- Admin dashboard to view registrations
- SQLite database for persistent storage
- Responsive user interface

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

## Project Structure

```text
CodeNova_Task3_Event_Registration/
├── app.py
├── database.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── admin.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/chandrikachandu0113-source/codenova-task3-event-registration.git
```

### 2. Navigate to the project directory

```bash
cd codenova-task3-event-registration
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Initialize the database

```bash
python database.py
```

### 7. Run the application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000

## Admin Dashboard

Visit:

http://127.0.0.1:5000/admin

The dashboard displays registered participants and their event details.

## Internship Details

**Program:** CodeNova Internship Program

**Domain:** Full Stack Development

**Batch:** 01

**Task:** Event Registration Platform

## Disclaimer

This project was developed for educational purposes as part of an internship. It is a beginner-level demonstration and is not intended for production use without additional security and deployment improvements.