from transformers import WhisperProcessor, WhisperForConditionalGeneration
import numpy as np


class STT:
    def __init__(self, model_name="lorenzoncina/whisper-small-ru", sample_rate=16000):
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name)
        self.model.config.forced_decoder_ids = None
        self.sample_rate = sample_rate

    def process(self, audio):
        audio_floats = np.concatenate([np.frombuffer(a, dtype=np.float32) for a in audio])
        input_features = self.processor(audio_floats, sampling_rate=self.sample_rate,
                                        return_tensors="pt").input_features
        predicted_ids = self.model.generate(input_features, language="ru")
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
        return transcription[0].strip()
