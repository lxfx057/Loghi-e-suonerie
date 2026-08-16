// --- 1. DISEGNO DEL LOGO B/N (Pixel Art stile Nokia 72x14) ---
const canvas = document.getElementById('logoCanvas');
const ctx = canvas.getContext('2d');

function drawNokiaLogo() {
    ctx.fillStyle = '#8b9bb4'; // Sfondo display Nokia
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#111111'; // Colore pixel scuro
    // Disegniamo la scritta "TOPOLONA" in pixel art rudimentale
    const pixels = [
        // T O P O L O N A
        [1,1,1, 0, 1,1,1, 0, 1,1,1, 0, 1,1,1, 0, 1,0, 0, 1,1,1, 0, 1,1,1],
        [0,1,0, 0, 1,0,1, 0, 1,0,1, 0, 1,0,1, 0, 1,0, 0, 1,0,1, 0, 1,0,1],
        [0,1,0, 0, 1,0,1, 0, 1,1,1, 0, 1,0,1, 0, 1,0, 0, 1,0,1, 0, 1,1,1],
        [0,1,0, 0, 1,0,1, 0, 1,0,0, 0, 1,0,1, 0, 1,0, 0, 1,0,1, 0, 1,0,1],
        [0,1,0, 0, 1,1,1, 0, 1,0,0, 0, 1,1,1, 0, 1,1,1, 1,1,1,1, 0, 1,0,1]
    ];
    
    // Semplifichiamo stampando pixel blocco per blocco
    ctx.font = "10px monospace";
    ctx.fillText("T O P O L O N A", 2, 11);
}
drawNokiaLogo();


// --- 2. SINTESI DELLA SUONERIA (Stile Monofonico/Polifonico Nokia) ---
document.getElementById('playRingtoneBtn').addEventListener('click', () => {
    playZIGMelody();
});

function playZIGMelody() {
    // Utilizziamo la Web Audio API nativa del browser per suonare le note reali della suoneria
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    // Note celebri della suoneria Topolona / motivetti tormentone dell'epoca
    const notes = [
        { freq: 523.25, duration: 0.2 }, // Do
        { freq: 659.25, duration: 0.2 }, // Mi
        { freq: 783.99, duration: 0.2 }, // Sol
        { freq: 1046.50, duration: 0.4 },// Do alto
        { freq: 783.99, duration: 0.2 }, // Sol
        { freq: 880.00, duration: 0.4 }, // La
        { freq: 0, duration: 0.1 },      // Pausa
        { freq: 1046.50, duration: 0.5 } // Do finale
    ];

    let startTime = audioCtx.currentTime;

    notes.forEach(note => {
        if (note.freq > 0) {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            
            // Onda quadra per dare quel tipico suono "Nokia 3310" retrò
            osc.type = 'square';
            osc.frequency.value = note.freq;

            gain.gain.setValueAtTime(0.1, startTime);
            gain.gain.exponentialRampToValueAtTime(0.00001, startTime + note.duration);

            osc.connect(gain);
            gain.connect(audioCtx.destination);

            osc.start(startTime);
            osc.stop(startTime + note.duration);
        }
        startTime += note.duration;
    });

    logMessage("🎵 [Audio] Suoneria 'Topolona' riprodotta con successo dal sintetizzatore WAP!");
}


// --- 3. INVIO E RICEZIONE MESSAGGI REALE (Simulazione Gateway SMS 48484) ---
const sendBtn = document.getElementById('sendSmsBtn');
const messageLog = document.getElementById('messageLog');

function logMessage(text) {
    messageLog.innerHTML += `> ${text}<br>`;
    messageLog.scrollTop = messageLog.scrollHeight;
}

sendBtn.addEventListener('click', () => {
    const code = document.getElementById('smsCode').value;
    const alias = document.getElementById('userAlias').value;

    logMessage(`Invio SMS a 48484 con testo: <b>${code}</b> per conto di <b>${alias}</b>...`);
    
    // Simula i passaggi reali dell'epoca con i ritardi di rete dei vecchi server SMS gateway
    setTimeout(() => {
        logMessage(`[Gateway SMS] Connessione stabilita con la centrale TIM/Vodafone...`);
    }, 800);

    setTimeout(() => {
        logMessage(`[Server ZIG] SMS ricevuto! Credito scalato di 5,00€. Attivazione in corso...`);
    }, 1800);

    setTimeout(() => {
        logMessage(`[OTA Push] 📦 **PACCHETTO RICEVUTO!** Logo B/N e Suoneria inviati al telefono di ${alias}!`);
        playZIGMelody(); // Suona automaticamente alla ricezione
    }, 3000);
});
