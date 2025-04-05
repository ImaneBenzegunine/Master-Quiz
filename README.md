# 📝 **Voice-to-Quiz: AI-Powered Lecture Transcription & Quiz Generator** 🎤➡️📚  

**Voice-to-Quiz** is an innovative web application that transforms spoken lectures into interactive quizzes using AI. Professors can record their lectures, and students receive auto-generated quizzes based on the transcribed content—enhancing learning efficiency and engagement.  

## 🚀 **Key Features**  

✅ **Real-Time Audio Recording** – Professors can record lectures directly in the browser.  
✅ **AI-Powered Transcription** – Converts speech to text using Google’s Speech Recognition.  
✅ **Automated Quiz Generation** – Uses **Groq's LLaMA 3.3-70B** to generate multiple-choice quizzes from transcribed text.  
✅ **Student Quiz Interface** – Students enter a unique lecture ID to access quizzes.  
✅ **Instant Feedback & Scoring** – Students receive immediate results with correct answers.  
✅ **PDF Summary Export** – AI-generated lecture summaries in downloadable PDF format.  
✅ **User Authentication** – Secure login for professors and students.  

## 🛠 **Tech Stack**  

- **Backend**: Python (Flask, SQLAlchemy)  
- **Frontend**: HTML, CSS, JavaScript (with Flask templating)  
- **AI & NLP**: Groq API (LLaMA 3.3-70B) + Google Speech Recognition  
- **Database**: SQLite (with Flask-SQLAlchemy ORM)  
- **Audio Processing**: `sounddevice`, `wave`, `SpeechRecognition`  
- **PDF Generation**: `reportlab`  

## 📌 **How It Works**  

1. **Professor Records Lecture**  
   - Starts/stops recording via the web interface.  
   - Audio is saved as a WAV file and transcribed to text.  

2. **AI Generates Quiz**  
   - The transcribed text is sent to **Groq's LLaMA 3.3-70B** to generate quiz questions.  
   - Questions include **4 choices + correct answer**.  

3. **Student Takes Quiz**  
   - Enters a unique lecture ID.  
   - Answers questions and gets instant feedback.  
   - Can download a **PDF summary** of the lecture.  
![image](https://github.com/user-attachments/assets/a1d76c3b-fcbb-445b-9b77-8d05d4177c33)

---  

### 🎯 **Why This Project Stands Out?**  
- **Education Tech Innovation** – Bridges the gap between lectures and interactive learning.  
- **Cutting-Edge AI** – Uses **Groq’s ultra-fast LLaMA 3.3-70B** for quiz generation.  
- **Practical Use Case** – Helps professors automate assessments and students reinforce learning.  

🚀 **Try it out and revolutionize learning with AI!** 🚀
