import argparse
import os
import json
import re
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default level; switch to DEBUG to see more logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def parse_and_standardize(data, base_path):
    """
    Process course data, match with folder structure, and collect standardized metadata.
    """
    logger.info("Starting to parse and standardize course data.")
    
    course_hierarchy = {
        "course_slug": data.get("slug", "unknown-course"),
        "course_name": data.get("name", "unknown-course"),
        "modules": []
    }

    transform_slug = lambda index, slug: f"{index+1:02d}@{slug[:40]}"

    # Iterate through modules
    for module_i, module in enumerate(data.get("modules", [])):
        transformed_module_slug = transform_slug(module_i, module.get("slug", "unknown-module"))
        logger.info(f"Processing module: {module.get('name', 'unknown-module')}")

        module_data = {
            "module_name": module.get("name", "unknown-module"),
            "module_slug": transformed_module_slug,
            "lessons": []
        }

        # Iterate through lessons
        for lesson_i, lesson in enumerate(module.get("lessons", [])):
            transformed_lesson_slug = transform_slug(lesson_i, lesson.get("slug", "unknown-lesson"))
            logger.debug(f"Processing lesson: {lesson.get('name', 'unknown-lesson')}")

            lesson_data = {
                "lesson_name": lesson.get("name", "unknown-lesson"),
                "lesson_slug": transformed_lesson_slug,
                "items": []
            }

            # Iterate through items
            for item_i, item in enumerate(lesson.get("items", [])):
                transformed_item_slug = transform_slug(item_i, item.get("slug", "unknown-item"))
                logger.debug(f"Processing item: {item.get('name', 'unknown-item')}")

                item_path = find_file_in_directory(
                    base_path, course_hierarchy["course_slug"], 
                    transformed_module_slug, transformed_lesson_slug, transformed_item_slug
                )

                content_metadata = collect_content_metadata(item_path)

                item_data = {
                    "name": item.get("name", "unknown-item"),
                    "slug": item.get("slug", "unknown-item"),
                    "transformed_slug": transformed_item_slug,
                    "path": item_path,
                    "content": content_metadata
                }

                lesson_data["items"].append(item_data)

            module_data["lessons"].append(lesson_data)

        course_hierarchy["modules"].append(module_data)

    logger.info("Finished parsing and standardizing course data.")
    return course_hierarchy

def collect_content_metadata(item_path):
    """
    Collect metadata for each content type within the item folder.
    """
    logger.debug(f"Collecting content metadata from: {item_path}")
    content = []

    if not os.path.exists(item_path):
        logger.warning(f"Item path not found: {item_path}")
        return content

    for root, _, files in os.walk(item_path):
        for file in files:
            file_path = os.path.join(root, file)
            content_type = determine_content_type(file)

            metadata = {
                "content_type": content_type,
                "file_name": file,
                "path": file_path,
                "size": os.path.getsize(file_path),
                "extension": Path(file).suffix
            }
            logger.debug(f"Collected metadata: {metadata}")
            content.append(metadata)

    return content

def determine_content_type(file_name):
    """
    Determine the content type based on the file extension.
    """
    if file_name.endswith(('.mp4', '.avi', '.mov')):
        return 'video'
    elif file_name.endswith(('.pdf', '.doc', '.docx')):
        return 'document'
    elif file_name.endswith(('.html', '.htm')):
        return 'webpage'
    elif file_name.endswith(('.srt', '.txt')):
        return 'transcript'
    else:
        return 'other'

def find_file_in_directory(base_path, course_slug, module_slug, lesson_slug, item_slug):
    """
    Search for the correct file in the local folder structure.
    """
    lesson_path = os.path.join(base_path, course_slug, module_slug, lesson_slug)
    logger.debug(f"Looking for item path: {lesson_path}")

    if not os.path.exists(lesson_path):
        logger.error(f"Lesson path not found: {lesson_path}")
        return f"Path not found: {lesson_path}"

    for folder in os.listdir(lesson_path):
        if re.search(rf"(\d+@)?{re.escape(item_slug)}", folder, re.IGNORECASE):
            item_path = os.path.join(lesson_path, folder)
            logger.debug(f"Found item path: {item_path}")
            return item_path

    logger.warning(f"Item folder not found for: {item_slug}")
    return f"File not found for: {item_slug}"

if __name__ == "__main__":

    # Define the default input and output directories
    default_input_path = 'crawled_data'
    default_output_dir = 'crawled_metadata'

    parser = argparse.ArgumentParser(description="Standardize crawled Coursera data.")
    parser.add_argument(
        'json_file',
        type=str,
        nargs='?',
        default=os.path.join(default_input_path, 'dl_coursera/uol-cm2025-computer-security.crawl.json'),
        help="Path to the JSON file with crawled metadata."
    )

    # Default output directory
    output_dir = 'crawled_metadata'

    parser.add_argument(
        '--output_file',
        type=str,
        default=os.path.join(default_output_dir, 'dl_coursera/uol-cm2025-computer-security.json'),
        help="Path to the output JSON file."
    )

    args = parser.parse_args()

    try:
        logger.info(f"Loading JSON file: {args.json_file}")
        with open(args.json_file, 'r') as f:
            data = json.load(f)

        course_data = parse_and_standardize(data, Path(args.json_file).parent)

        logger.info(f"Saving standardized data to: {args.output_file}")
        output_directory = os.path.dirname(args.output_file)
        os.makedirs(output_directory, exist_ok=True)

        with open(args.output_file, 'w') as f:
            json.dump(course_data, f, indent=4)

        logger.info("Process completed successfully.")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
