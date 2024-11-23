import re
import json
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Switch to DEBUG during development, INFO for production
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def parse_srt(file_path):
    """Parse an SRT file and extract segments with timestamps."""
    logger.debug(f"Attempting to parse SRT file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []

    pattern = r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?:\n\n|\n*$)"
    matches = re.findall(pattern, content, re.DOTALL)

    segments = [
        {
            "sequence": int(match[0]),
            "start_time": match[1],
            "end_time": match[2],
            "text": match[3].replace('\n', ' ').strip()
        }
        for match in matches
    ]

    logger.debug(f"Parsed {len(segments)} segments from {file_path}")
    return segments

def generate_json_format(segments, output_file):
    """Generate a JSON file with transcript metadata."""
    transcript_data = {"language": "en", "segments": segments}

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transcript_data, f, indent=4)
    logger.debug(f"JSON transcript saved: {output_file}")

def generate_txt_format(segments, output_file):
    """Generate a plain text transcript file."""
    transcript_text = "\n".join([seg["text"] for seg in segments])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transcript_text)
    logger.debug(f"Plain text transcript saved: {output_file}")

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Process an SRT transcript into JSON and TXT formats.")
    parser.add_argument(
        '--input_file',
        type=str,
        default='crawled_data/dl_coursera/uol-cm2025-computer-security/01@topic-1-introduction-to-computer-securit/01@lesson-1-introduction-to-the-course/01@introduction-to-the-course/01@.srt',
        help="Path to the SRT file to be processed."
    )
    parser.add_argument(
        '--output_json',
        type=str,
        default='tmp/transcript.json',
        help="Path to save the JSON transcript (default: transcript.json)."
    )
    parser.add_argument(
        '--output_txt',
        type=str,
        default='tmp/transcript.txt',
        help="Path to save the plain text transcript (default: transcript.txt)."
    )

    args = parser.parse_args()

    try:
        logger.debug(f"Processing SRT file: {args.input_file}")
        segments = parse_srt(args.input_file)

        if segments:
            generate_json_format(segments, args.output_json)
            generate_txt_format(segments, args.output_txt)
            logger.debug("Transcript processing completed successfully.")
        else:
            logger.warning(f"No segments found in: {args.input_file}")

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
