import subprocess
from pathlib import Path
import pandas as pd

MIN_DURATION = 3
MAX_DURATION = 30

def segment_folder(lang):
    audio_dir = Path(f"dataset/standardized/{lang}")
    diar_dir = Path(f"dataset/diarization/{lang}")
    out_dir = Path(f"dataset/segments/{lang}")

    out_dir.mkdir(parents=True, exist_ok=True)

    for csv_file in diar_dir.glob("*.csv"):
        audio_file = audio_dir / f"{csv_file.stem}.wav"

        if not audio_file.exists():
            print(f"Missing: {audio_file.name}")
            continue

        df = pd.read_csv(csv_file)

        df["duration"] = df["end"] - df["start"]

        df = df[(df["duration"] >= MIN_DURATION) & (df["duration"] <= MAX_DURATION)].reset_index(drop=True)

        for i, row in df.iterrows():
            start = row["start"]
            duration = row["duration"]
            speaker = row["speaker"]

            output_file = out_dir/ f"{csv_file.stem}_{speaker}_{i}.wav"

            cmd = [
                "ffmpeg",
                "-y",
                "-ss", str(start),
                "-i", str(audio_file),
                "-t", str(duration),
                str(output_file),
            ]

            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        print(f"Done: {csv_file.stem}")


segment_folder("english")
segment_folder("tamil")