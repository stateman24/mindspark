 ![MindSpark Logo](/static/assets/Group%201.svg)

MindSpark is a dynamic and interactive Quiz Application designed to challenge and sharpen users' minds. Built with a modern tech stack, the app offers a seamless user experience for testing knowledge across various topics.

## Current Features

### 1. **User Authentication**
   - Users can sign up, log in, and log out securely.
   - Authentication implemented using Django's built-in user management system.
   - Social login with Google

### 2. **Quiz Creation**
   - Admins can create and manage quizzes with role-based access controls to ensure proper permissions.
   - Questions can have multiple choices, with one correct answer.

### 3. **Taking Quizzes**
   - Users can attempt quizzes and submit answers.
   - Real-time feedback on quiz progress.

### 4. **Responsive Design**
   - Tailwind CSS ensures the application is mobile-friendly and looks great on any device.

### 5. **Data Persistence**
   - PostgreSQL is used to store user details, quiz data, and results securely.

## Features in Development

### 1. **Leaderboard**
   - A global leaderboard showcasing top-performing users.

### 2. **Timed Quizzes**
   - Add timers to quizzes to make them more challenging.

### 3. **Quiz Categories**
   - Users will be able to choose quizzes based on specific topics or difficulty levels.

### 4. **User Profiles**
   - Users can view their quiz history, scores, and achievements.

### 5. **Quiz Analytics**
   - Provide detailed statistics and insights on performance.

### 6. **Gamification Features**
   - Add badges and rewards to encourage consistent engagement.

## Tech Stack

- **Frontend**: Django (template engine), Tailwind CSS
- **Backend**: Django Framework
- **Database**: PostgreSQL
- **Interactivity**: JavaScript

## How to Run the Application

### Prerequisites
- Python 3.x
- PostgreSQL
- Node.js (optional, for managing Tailwind CSS)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mindspark.git
   ```
2. Navigate to the project directory:
   ```bash
   cd mindspark
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
   ```
6. Access the application at `http://127.0.0.1:8000`.

## Contributing
Contributions are welcome! If you'd like to add new features or fix bugs, feel free to fork the repository and create a pull request.

## Future Vision
MindSpark aims to become a go-to platform for engaging and interactive quizzes, combining learning and fun in an intuitive way. Stay tuned for more updates!