# Skill Tracker

This project is a lightweight local web server for tracking skill development. It allows users to manage their skills, including adding, updating, and deleting skills.

## Project Structure

```
skill-tracker
├── src
│   ├── server.ts               # Entry point of the application
│   ├── routes
│   │   ├── index.ts            # Main routes setup
│   │   └── skills.ts           # Routes for skill management
│   ├── controllers
│   │   └── skillsController.ts  # Handles skill-related requests
│   ├── services
│   │   └── skillService.ts      # Business logic for managing skills
│   ├── models
│   │   └── skill.ts             # Defines the structure of a skill object
│   ├── db
│   │   └── index.ts             # Database connection and CRUD operations
│   ├── public
│   │   ├── css
│   │   │   └── styles.css       # CSS styles for the web application
│   │   └── js
│   │       └── app.js           # Client-side JavaScript
│   └── schemas
│       └── skill_tree.schema.json # JSON schema for skill data
├── package.json                 # npm configuration file
├── tsconfig.json                # TypeScript configuration file
├── .env.example                 # Example environment variables
└── README.md                    # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd skill-tracker
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Set up environment variables:**
   Copy `.env.example` to `.env` and configure your database connection and other settings.

4. **Run the application:**
   ```
   npm start
   ```

## Features

- Add, update, and delete skills.
- View a list of all skills.
- Lightweight and easy to set up.
- Uses a local database for data storage.

## Usage

Once the server is running, you can access the application in your web browser at `http://localhost:3000`. Use the provided routes to manage your skills effectively.