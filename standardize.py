from pathlib import Path
import os

def standardize_audio(lang):
    input_dir = Path(f"dataset/downloads/{lang}")
    output_dir = Path(f"dataset/standardized/{lang}")

    output_dir.mkdir(parents=True, exist_ok=True)

    for audio_file in input_dir.iterdir():
        if not audio_file.is_file():
            continue

        output_file = output_dir / f"{audio_file.stem}.wav"

        command = f"ffmpeg -y -i {audio_file} -ac 1 -ar 24000 -c:a pcm_s16le {output_file}"

        os.system(command)
        print(f"Done: {output_file.name}")


standardize_audio("english")
standardize_audio("tamil")