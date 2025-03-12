import sounddevice as sd
import wave
import threading
import os
import uuid
import speech_recognition as sr
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import requests
from groq import Groq
from time import sleep

app = Flask(__name__)
CORS(app)

# Paramètres de l'enregistrement
SAMPLERATE = 44100  # Taux d'échantillonnage, 44100 Hz
CHANNELS = 1  # Mono
FILENAME = "audio_recording.wav"  # Fichier WAV temporaire
TEXT_FILENAME = "transcription.txt"  # Fichier texte pour stocker la transcription
audio_data = None  # Variable globale pour l'audio en temps réel

# Enregistrement en cours
is_recording = False
audio_thread = None

# Configuration de la base de données et de la connexion utilisateur
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # "prof" ou "etudiant"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


with app.app_context():
    db.create_all()

# Fonction pour enregistrer l'audio en continu
def enregistrer_audio_continu():
    global audio_data
    global is_recording
    is_recording = True
    print("Enregistrement en cours...")
    audio_data = []

    with sd.InputStream(samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16') as stream:
        while is_recording:
            chunk, overflowed = stream.read(1024)
            audio_data.append(chunk)

# Fonction de conversion de l'audio en texte
def convertir_audio_en_texte(fichier_wav):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(fichier_wav) as source:
            print("Transcription en cours...")
            audio = recognizer.record(source)  # Lire le fichier audio
            texte = recognizer.recognize_google(audio, language="fr-FR")  # Reconnaissance vocale en français
            print("Texte transcrit :", texte)
            return texte
    except Exception as e:
        print("Erreur lors de la transcription :", str(e))
        return None

'''# transcription table
class Transcription(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID stocké en string
    text = db.Column(db.Text, nullable=False)  # Texte transcrit
    professeur_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID du professeur
'''
# transcription table
class Transcription(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID stocké en string
    text = db.Column(db.Text, nullable=False)  # Texte transcrit
    professeur_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID du professeur

    professor = db.relationship('User', backref='transcriptions')  # Association avec le professeur

with app.app_context():
    db.create_all()





# Fonction générique pour envoyer la requête via le client Groq
def send_request_to_groq(api_key, transcribed_text, retries=3, timeout=10):
    # Initialiser le client Groq avec la clé API
    groq_client = Groq(api_key=api_key)
    for attempt in range(retries):
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "tu es un assistant merveilleux et serviable."},
                    {"role": "user", "content": f"Peux-tu générer une série de questions pour un quiz à partir de ce texte :\n\n{transcribed_text}\n\nChaque question devrait avoir quatre choix de réponse possibles et une réponse correcte. La structure des données doit être sous la forme suivante : question, choices, correct_answer."}
                ],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Erreur de connexion (tentative {attempt + 1} sur {retries}): {e}")
            if attempt < retries - 1:
                print("Nouvelle tentative dans 5 secondes...")
                sleep(5)
            else:
                print("Le nombre maximal de tentatives a été atteint.")
                return None
    return None



def generate_quiz_from_text(transcribed_text, api_key, retries=3, timeout=10):
    # Appeler la fonction générique pour envoyer la requête avec le texte transcrit
    response_data = send_request_to_groq(api_key, transcribed_text, retries=retries, timeout=timeout)

    if response_data:
        # Assurer que la réponse est bien formatée
        questions = response_data.split("\n")  # Cela dépend de la réponse que l'API renvoie
        return questions  # Retourner les questions générées sous forme de liste
    else:
        print("Erreur lors de la génération du quiz.")
        return None


def read_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(email=email).first():
            return "Cet email est déjà utilisé."

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return "Email ou mot de passe incorrect"

        login_user(user)

        if user.role == "prof":
            return redirect(url_for('quiz'))
        else:
            return redirect(url_for('enter_id'))

    return render_template("login.html")

@app.route('/quiz')
@login_required
def quiz():
    if current_user.role != "prof":
        return redirect(url_for('home'))
    return render_template("quiz.html")

# API pour commencer l'enregistrement
@app.route('/start_recording', methods=['GET'])
@login_required
def start_recording():
    if current_user.role != "prof":
        return jsonify({"message": "Accès refusé"}), 403
    global audio_thread
    if not is_recording:
        audio_thread = threading.Thread(target=enregistrer_audio_continu)
        audio_thread.start()
        return jsonify({"message": "Enregistrement démarré."}), 200
    else:
        return jsonify({"error": "Enregistrement déjà en cours."}), 400


# API pour arrêter l'enregistrement et convertir en texte
import random

# API pour arrêter l'enregistrement et convertir en texte
@app.route('/stop_recording', methods=['GET'])
@login_required
def stop_recording():
    if current_user.role != "prof":
        return jsonify({"message": "Accès refusé"}), 403
    global is_recording
    if is_recording:
        is_recording = False
        audio_thread.join()

        # Sauvegarde de l'audio en fichier WAV
        with wave.open(FILENAME, 'wb') as f:
            f.setnchannels(CHANNELS)
            f.setsampwidth(2)  # 16 bits
            f.setframerate(SAMPLERATE)
            for chunk in audio_data:
                f.writeframes(chunk.tobytes())

        # Convertir l'audio en texte
        texte_transcrit = convertir_audio_en_texte(FILENAME)

        if texte_transcrit:
            # Générer un ID à 5 chiffres
            transcription_id = str(random.randint(10000, 99999))

            # Sauvegarde dans la base de données
            transcription = Transcription(id=transcription_id, text=texte_transcrit, professeur_id=current_user.id)
            db.session.add(transcription)
            db.session.commit()

            return jsonify({
                "message": "Enregistrement arrêté.",
                "transcription": texte_transcrit,
                "transcription_id": transcription_id  # Retourner l'ID
            }), 200
        else:
            return jsonify({"error": "Impossible de transcrire l'audio."}), 500

    else:
        return jsonify({"error": "Aucun enregistrement en cours."}), 400
'''
@app.route('/quiz1/<transcription_id>', methods=['GET'])
@login_required
def quiz1(transcription_id):
    if current_user.role != "etudiant":
        return redirect(url_for('home'))

    transcription = db.session.get(Transcription, int(transcription_id))
    text = read_text_from_file("C:/Users/bouat/PycharmProjects/data_girls/transcription.txt")
    if not transcription:
        return "ID invalide. Veuillez réessayer.", 400

    # Récupérer les questions générées à partir du texte transcrit
    api_key = "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"
    quiz_questions = generate_quiz_from_text(text, api_key)

    if not quiz_questions:
        return "Erreur dans la génération du quiz.", 500

    # Passer les questions générées au template
    return render_template('quiz1.html', transcription=transcription, questions=quiz_questions)
'''
@app.route('/quiz1/<transcription_id>', methods=['GET'])
@login_required
def quiz1(transcription_id):
    if current_user.role != "etudiant":
        return redirect(url_for('home'))

    # Récupérer la transcription par son ID
    transcription = db.session.get(Transcription, transcription_id)
    if not transcription:
        return "ID invalide. Veuillez réessayer.", 400

    # Récupérer le texte transcrit de la base de données
    text = transcription.text

    # Générer les questions à partir du texte transcrit
    api_key = "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"
    quiz_questions = generate_quiz_from_text(text, api_key)

    if not quiz_questions:
        return "Erreur dans la génération du quiz.", 500

    questions_with_indices = [(i, question) for i, question in enumerate(quiz_questions)]

    # Passer les questions avec leurs indices au template
    return render_template('quiz1.html', transcription=transcription, questions=quiz_questions)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    score = 0
    answers = {}

    # Vérifier les réponses de l'étudiant
    for i, question in enumerate(quiz_questions):
        student_answer = request.form.get(f"question_{i}")
        if student_answer == question['answer']:  # Comparer la réponse de l'étudiant avec la réponse correcte
            score += 1
        answers[i] = student_answer

    return render_template('quiz_result.html', score=score, total=len(quiz_questions), answers=answers,
                           questions=quiz_questions)


@app.route('/enter_id', methods=['GET'])
@login_required
def enter_id():
    if current_user.role != "etudiant":
        return redirect(url_for('home'))
    return render_template('enter_id.html')


@app.route('/validate_id', methods=['POST'])
@login_required
def validate_id():
    if current_user.role != "etudiant":
        return redirect(url_for('home'))

    transcription_id = request.form.get('transcription_id')
    transcription = db.session.get(Transcription, transcription_id)

    if transcription:
        return redirect(url_for('quiz1', transcription_id=transcription_id))
    else:
        return "ID invalide. Veuillez réessayer.", 400



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)







