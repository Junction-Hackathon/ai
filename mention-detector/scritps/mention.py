import subprocess
import os
from faster_whisper import WhisperModel
from difflib import SequenceMatcher


def extract_audio(video_path: str, out_path: str = "audio.wav"):
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-vn",
                "-ar",
                "16000",
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                out_path,
                "-y",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError("FFmpeg failed to extract audio.")

    return out_path


def fuzzy_match(text: str, donor_name: str, threshold=0.75):
    text = text.lower()
    donor_name = donor_name.lower()

    if donor_name in text:
        return True, 1.0

    ratio = SequenceMatcher(None, donor_name, text).ratio()
    return ratio >= threshold, round(ratio, 2)


def detect_donor_name(video_path: str, donor_name: str):
    try:
        audio_path = extract_audio(video_path)
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            return {
                "donor_mentioned": False,
                "match_score": 0.0,
                "error": "No audio extracted from video.",
            }

        model = WhisperModel("base", compute_type="int8")
        segments, _ = model.transcribe(audio_path)

        transcript_segments = [seg.text.strip() for seg in segments if seg.text.strip()]
        if not transcript_segments:
            return {
                "donor_mentioned": False,
                "match_score": 0.0,
                "error": "No voice or speech detected in the video.",
            }

        transcript = " ".join(transcript_segments)
        matched, score = fuzzy_match(transcript, donor_name)

        return {
            "donor_mentioned": matched,
            "match_score": score,
            "transcript": transcript,
        }

    except Exception as e:
        return {
            "donor_mentioned": False,
            "match_score": 0.0,
            "error": f"Voice detection failed: {str(e)}",
        }
