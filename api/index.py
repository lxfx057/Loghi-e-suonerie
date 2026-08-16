import os
from flask import Flask, request, Response
import yt_dlp

app = Flask(__name__)

# Database di esempio delle suonerie con link YouTube associati
RINGTONES = {
    "1": {"name": "Topolona", "url": "https://www.youtube.com/watch?v=ESEMPIO_LINK_1"},
    "2": {"name": "Crazy Frog", "url": "https://www.youtube.com/watch?v=k85mRPqvMbE"},
    "3": {"name": "Dragostea Din Tei", "url": "https://www.youtube.com/watch?v=YRS-82VZbAU"},
    "4": {"name": "The Ketchup Song", "url": "https://www.youtube.com/watch?v=VAdbt7QUhAI"}
}

@app.route("/", methods=["GET"])
def home():
    return "Retro Ringtone IVR Service is online!"

# Endpoint 1: Risposta iniziale alla chiamata (Genera il menu vocale TwiML)
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

# Endpoint 2: Elabora la scelta della suoneria e chiede il numero destinatario
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
    
    # Chiede all'utente di digitare il numero di telefono a cui inviare la suoneria seguito da cancelleto (#)
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Gather finishOnKey="#" action="/send-ringtone?choice={digit_pressed}" method="POST">
            <Say language="it-IT">Hai scelto {ringtone_name}. Ora inserisci il numero di telefono del destinatario seguito dal tasto cancelleto.</Say>
        </Gather>
    </Response>
    """
    return Response(twiml_response, mimetype="application/xml")

# Endpoint 3: Riceve il numero, scarica l'audio (simulazione/logica) e chiude la chiamata
@app.route("/send-ringtone", methods=["POST"])
def send_ringtone():
    choice = request.args.get("choice")
    recipient_phone = request.form.get("Digits") # Il numero digitato dall'utente
    
    ringtone_data = RINGTONES.get(choice)
    
    if ringtone_data and recipient_phone:
        # Qui puoi inserire la logica di yt-dlp per scaricare l'mp3 su uno storage temporaneo o inviarlo
        # Esempio di download sicuro (nota: Vercel ha limiti di scrittura su disco, usa /tmp/)
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
            # Esegue il download dell'audio da YouTube
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([ringtone_data["url"]])
            print(file_path := "/tmp/ringtone.mp3")
            # In un'implementazione reale, qui useresti le API di WhatsApp (es. Twilio o Meta Cloud API) 
            # per inviare il file dal percorso /tmp/ringtone.mp3 al numero recipient_phone.
        except Exception as e:
            print(f"Errore durante il download: {e}")

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say language="it-IT">Perfetto! La suoneria è stata inviata via messaggio al numero {recipient_phone}. Grazie e arrivederci!</Say>
        <Hangup/>
    </Response>
    """
    return Response(twiml_response, mimetype="application/xml")

if __name__ == "__main__":
    app.run(debug=True)
