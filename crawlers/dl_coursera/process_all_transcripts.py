import os
import json
import argparse
import logging
from pathlib import Path
from transcript_formatter import parse_srt, generate_json_format, generate_txt_format

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Adjust to DEBUG when detailed logs are needed
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def create_output_path(base_output_dir, course_slug, module_slug, lesson_slug, item_slug):
    """Create directory structure based on course metadata."""
    path = os.path.join(base_output_dir, course_slug, module_slug, lesson_slug, item_slug)
    Path(path).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Created output path: {path}")
    return path

def process_all_transcripts(metadata_file, output_base_dir):
    """Process all transcripts from the metadata JSON file."""
    logger.info(f"Loading metadata from: {metadata_file}")

    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    course_slug = metadata['course_slug']
    logger.debug(f"Processing course: {course_slug}")

    for module in metadata['modules']:
        module_slug = module['module_slug']
        logger.info(f"Processing module: {module_slug}")

        for lesson in module['lessons']:
            lesson_slug = lesson['lesson_slug']
            logger.debug(f"Processing lesson: {lesson_slug}")

            for item in lesson['items']:
                item_slug = item['transformed_slug']
                logger.debug(f"Processing item: {item_slug}")

                for content in item['content']:
                    if content['content_type'] == 'transcript':
                        transcript_path = content['path']
                        logger.debug(f"Processing transcript: {transcript_path}")

                        # Parse the transcript and generate outputs
                        segments = parse_srt(transcript_path)

                        output_path = create_output_path(
                            output_base_dir, course_slug, module_slug, lesson_slug, item_slug
                        )

                        output_json = os.path.join(output_path, 'transcript.json')
                        output_txt = os.path.join(output_path, 'transcript.txt')

                        # Generate both JSON and TXT formats
                        generate_json_format(segments, output_json)
                        generate_txt_format(segments, output_txt)

                        logger.debug(f"Saved JSON: {output_json}")
                        logger.debug(f"Saved TXT: {output_txt}")

    logger.info("All transcripts processed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and format transcripts from metadata.")
    parser.add_argument(
        '--metadata_file',
        type=str,
        default="crawled_metadata/dl_coursera/uol-cm2025-computer-security.json",
        help="Path to the metadata JSON file containing the transcript information."
    )
    parser.add_argument(
        '--output_base_dir',
        type=str,
        default='outputs/structured_transcripts/dl_coursera',
        help="Base directory to store structured transcripts (default: outputs/structured_transcripts/dl_coursera)."
    )

    args = parser.parse_args()

    try:
        logger.info(f"Starting transcript processing with metadata: {args.metadata_file}")
        process_all_transcripts(args.metadata_file, args.output_base_dir)
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
