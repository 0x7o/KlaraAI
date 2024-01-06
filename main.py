import RPi.GPIO as GPIO
from klara.models.vad import VAD
from klara.models.tts import TTS
from klara.models.stt import STT
from klara.models.nanofialka import NanoFialka
from klara.dialog_manager import DialogManager

BUTTON = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

vad = VAD()
tts = TTS()
stt = STT()
nf = NanoFialka()
dm = DialogManager(model=nf)

while True:
    state = GPIO.input(BUTTON)
    if not state:
        audio = vad.start_recording()
        text = stt.process(audio)
        response = dm.get_response(text)
        tts.say(response)
