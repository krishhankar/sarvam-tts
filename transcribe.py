import os
import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm

API_KEY = "my-key-was-here"


def transcribe_folder(lang):
    audio_dir = Path(f"dataset/segments/{lang}")
    rows = []

    mode = "transcribe" if lang == "english" else "translit"

    headers = {
        "api-subscription-key": API_KEY
    }

    for audio_file in tqdm(
        list(audio_dir.glob("*.wav")),
        desc=f"Transcribing {lang}"
    ):
        try:
            with open(audio_file, "rb") as f:
                files = {
                    "file": (
                        audio_file.name,
                        f,
                        "audio/wav"
                    )
                }

                data = {
                    "model": "saaras:v3",
                    "mode": mode
                }

                response = requests.post(
                    "https://api.sarvam.ai/speech-to-text",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=120
                )

            if response.status_code != 200:
                print(f"Failed: {audio_file.name}")
                print(response.text)
                continue

            result = response.json()

            transcript = result.get("transcript","").strip()

            if transcript:
                rows.append({
                    "audio": audio_file.name,
                    "text": transcript,
                    "language": result.get("language_code", lang),
                    "confidence": result.get("language_probability")
                })

        except Exception as e:
            print(f"Failed: {audio_file.name}")
            print(e)

    df = pd.DataFrame(rows)
    df.to_csv(f"dataset/metadata_{lang}.csv",index=False,encoding="utf-8")

    print(f"Finished {lang}: {len(df)} transcripts saved.")


transcribe_folder("english")
transcribe_folder("tamil")