# Sarvam TTS Dataset Pipeline

This repository contains the data curation pipeline for creating a high-quality, 60-minute Text-to-Speech (TTS) dataset. The pipeline is designed to extract audio from YouTube, process it into clean single-speaker segments, and transcribe the audio for both English and Tamil.

## File Structure

```text
.
├── dataset/
│   ├── diarization/         
│   ├── downloads/           
│   ├── segments/            
│   ├── standardized/        
│   ├── metadata_english.csv 
│   └── metadata_tamil.csv   
├── urls/
│   ├── eng_yt_urls.txt      
│   └── tamil_yt_urls.txt    
├── diarization.py           
├── download_urls.py         
├── segmentation.py          
├── standardize.py           
└── transcribe.py            
```

## Pipeline

The dataset creation process follows a straightforward, automated 5-step pipeline:

1. **Download (`download_urls.py`)**: Fetches audio from the curated YouTube links in the `urls/` directory using `yt-dlp`.
2. **Standardize (`standardize.py`)**: Normalizes the downloaded files to 24kHz, single-channel (mono) WAV format using `ffmpeg`.
3. **Diarization (`diarization.py`)**: `pyannote` is used to identify speaker turns and generate timestamps for single-speaker regions.
4. **Segmentation (`segmentation.py`)**: The audio is split into individual speaker clips, retaining segments between 3 and 30 seconds.
5. **Transcription (`transcribe.py`)**: Sarvam AI's `saaras:v3` model is used to transcribe the audio segments, and the results are saved to CSV metadata files.

## Command to run the pipeline

```bash
python download_urls.py
python standardize.py
python diarization.py
python segmentation.py
python transcribe.py
