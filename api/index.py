import os
import random
from flask import Flask, request, Response
import yt_dlp

app = Flask(__name__)

# Database suonerie e un elenco di GIF random in stile anni 2000/trash
RINGTONES = {
    "1": {"name": "Topolona", "url": "https://www.youtube.com/watch?v=ESEMPIO_LINK_1"},
    "2": {"name": "Crazy Frog", "url": "https://www.youtube.com/watch?v=k85mRPqvMbE"},
    "3": {"name": "Dragostea Din Tei", "url": "https://www.youtube.com/watch?v=YRS-82VZbAU"},
    "4": {"name": "The Ketchup Song", "url": "https://www.youtube.com/watch?v=VAdbt7QUhAI"}
}

RANDOM_GIFS = [
    "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif", # Crazy frog style
    "https://media.giphy.com/media/l0HlRnAWXxn0MhOBK/giphy.gif",
    "https://media.giphy.com/media/10VxA3X7rC3W2s/giphy.gif",
    "https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.gif"
]

@app.route("/", methods=["GET"])
def home():
    return "Retro Ringtone IVR Service con MP3 e GIF è online!"

# 1. Menu Vocale Iniziale
@app.route("/voice", methods=["POST", "GET"])
def voice_menu():
    twiml_response = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Gather numDigits="1" action="/process-choice" method="POST">
            <Say language="it-IT">Benvenuto nel servizio suonerie retro. Premi 1 per Topolona, 2 per Crazy Frog, 3 per Dragostea Din Tei, o 4 per The Ketchup Song.</Say>
        </Gather>
    </Response>
    """
    return Response(twiml_response, mimetype="application/xml")

# 2. Riceve la scelta e chiede il numero
@app.route("/process-choice", methods=["POST"])
def process_choice():
    digit_pressed = request.form.get("Digits")
    
    if digit_pressed not in RINGTONES:
        twiml_response = """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say language="it-IT">Scelta non valida. Riprova.</Say>
            <Redirect>/voice</Redirect>
        </Response>
        """
        return Response(twiml_response, mimetype="application/xml")
    
    ringtone_name = RINGTONES[digit_pressed]["name"]
    
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Gather finishOnKey="#" action="/send-media?choice={digit_pressed}" method="POST">
            <Say language="it-IT">Hai scelto {ringtone_name}. Ora inserisci il numero di telefono del destinatario seguito dal tasto cancelleto.</Say>
        </Gather>
    </Response>
    """
    return Response(twiml_response, mimetype="application/xml")

# 3. Scarica MP3 da YouTube, seleziona una GIF random e invia tutto
@app.route("/send-media", methods=["POST"])
def send_media():
    choice = request.args.get("choice")
    recipient_phone = request.form.get("Digits")
    ringtone_data = RINGTONES.get(choice)
    
    selected_gif = random.choice(RANDOM_GIFS)
    
    if ringtone_data and recipient_phone:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '/tmp/ringtone.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        try:
            # Scarica l'audio da YouTube direttamente nella cartella temporanea di Vercel
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([ringtone_data["url"]])
            
            audio_path = "/tmp/ringtone.mp3"
            print(f"File MP3 pronto in: {audio_path}")
            print(f"GIF Random selezionata: {selected_gif}")
            
            # QUI PUOI INTEGRARE L'INVIO REALE:
            # - Usa le API di WhatsApp o un bot per spedire 'audio_path' e 'selected_gif' a 'recipient_phone'
            
        except Exception as e:
            print(f"Errore durante il download da YouTube: {e}")

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say language="it-IT">Boom! La suoneria MP3 e la GIF random sono in viaggio verso il numero {recipient_phone}. Ciao!</Say>
        <Hangup/>
    </Response>
    """
    return Response(twiml_response, mimetype="application/xml")

if __name__ == "__main__":
    app.run(debug=True)
