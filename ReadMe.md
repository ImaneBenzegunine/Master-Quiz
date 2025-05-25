# Master Quiz

Master Quiz is an interactive educational platform designed to enhance learning through AI-powered quiz generation. Teachers can create courses via voice recordings, while students engage with automatically generated quizzes and downloadable PDF summaries for effective revision.

## Key Features

- **Automated Quiz Generation**: Instantly creates MCQs from lecture transcripts
- **PDF Course Summaries**: Generate and download concise course summaries
- **Role-Based Access**:
  - *Teachers*: Record lessons, share course IDs
  - *Students*: Access courses via ID, take quizzes, view results, and download PDFs
- **Voice-to-Text Transcription**: Real-time audio recording and transcription
- **AI Integration**: Utilizes Groq API with llama-3.3-70b model for content generation

## Technologies Used

**Backend**: Python, Flask  
**Database**: MySQL with SQLAlchemy  
**Speech Recognition**: SpeechRecognition, sounddevice, numpy  
**AI**: Groq API (llama-3.3-70b)  
**Authentication**: Flask-Login  
**PDF Generation**: ReportLab  
**Frontend**: HTML, CSS, JavaScript  

## Installation

### Prerequisites
- Python 3.9+
- MySQL Server
- Groq API account (for API key)

### Setup Instructions

1. Clone repository:
   ```bash
   https://github.com/ImaneBenzegunine/Master-Quiz.git
   cd Quiz_master
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Database setup:
   ```sql
   CREATE DATABASE master_quiz;
   ```



## Commands Reference

### Database Operations
```bash
# Initialize database tables
flask db init

# Create migration scripts
flask db migrate -m "initial migration"

# Apply migrations
flask db upgrade
```

### Development
```bash
# Run the Flask development server
flask run

# Alternative run command
python quiz.py

# Run with debug mode
flask run --debug
```

### Virtual Environment
```bash
# Deactivate environment
deactivate

# Freeze requirements
pip freeze > requirements.txt
```

### Testing
```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
coverage run -m pytest tests/
coverage report
```

## Usage Guide

### For Teachers
1. Register with "professor" role
2. Navigate to recording interface
3. Start/stop voice recording sessions
4. Share generated course ID with students

### For Students
1. Register with "student" role
2. Enter provided course ID
3. Complete auto-generated quiz
4. View results and download PDF summary

## Development Team | Data Girls

| Member             | Role           | Affiliation                                  |
|--------------------|----------------|---------------------------------------------|
| Maria El Houdaigui | Data Engineer  | Big Data & Information Systems Student, ENSA Berrechid |
| Ilham Bouatioui    | Data Scientist | Big Data & Information Systems Student, ENSA Berrechid |
| Imane Benzegunine  | AI Engineer    | Big Data & Information Systems Student, ENSA Berrechid |

## License

This project is currently not licensed for public use. Please contact the development team if you would like to use or contribute to this project.

