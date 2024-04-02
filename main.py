import RPi.GPIO as GPIO
from klara.models.vad import VAD
from klara.models.tts import TTS
from klara.models.stt import STT
from klara.models.claude import Claude
from klara.dialog_manager import DialogManager

BUTTON = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

vad = VAD()
tts = TTS()
stt = STT()
claude = Claude(api_key="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")
dm = DialogManager(model=claude)

while True:
    state = GPIO.input(BUTTON)
    if not state:
        audio = vad.start_recording()
        text = stt.process(audio)
        response = dm.get_response(text)
        tts.say(response)
