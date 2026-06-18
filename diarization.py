from pathlib import Path
from pyannote.audio import Pipeline
import pandas as pd

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-community-1",
    token="my-token-was-here"
)

def diarize_folder(lang):
    input_dir = Path(f"dataset/standardized/{lang}")
    output_dir = Path(f"dataset/diarization/{lang}")
    output_dir.mkdir(parents=True, exist_ok=True)

    for audio in input_dir.glob("*.wav"):
        print(f"Processing {audio.name}")

        output = pipeline(str(audio))

        rows = []
        for turn, speaker in output.speaker_diarization:
            rows.append({
                "start": round(turn.start, 2),
                "end": round(turn.end, 2),
                "speaker": speaker
            })

        pd.DataFrame(rows).to_csv(output_dir/f"{audio.stem}.csv",index=False)

diarize_folder("english")
diarize_folder("tamil")