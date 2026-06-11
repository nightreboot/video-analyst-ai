import whisper

model = whisper.load_model('base')

def transcribe_audio(audio_chunks : list) -> str:
    transcribe = []
    for i, chunk in enumerate(audio_chunks):
         
         print(f"Transcribing chunk "f"{i + 1}/"f"{len(audio_chunks)}")

         result = model.transcribe(
              chunk,
               fp16=False,
               beam_size=1,
               best_of=1
         )
         if result['language'] == 'en' or result['language'] == 'hi':
              text = result['text']
              transcribe.append(text)

    return "\n".join(
        transcribe
    )

         