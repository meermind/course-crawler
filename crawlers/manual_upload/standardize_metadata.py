import os
import json
import argparse
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_course(course_path):
    course_slug = os.path.basename(course_path.strip("/"))
    course_name = course_slug.replace("-", " ").title()

    metadata = {
        "course_slug": course_slug,
        "course_name": course_name,
        "modules": []
    }

    # Iterate through module directories
    for module_dir in sorted(os.listdir(course_path)):
        module_path = os.path.join(course_path, module_dir)
        if not os.path.isdir(module_path):
            continue

        # Extract module name and slug
        module_slug, module_name_raw = module_dir.split("@", 1)
        module_name = module_name_raw.replace("-", " ").title()

        lessons = []

        # Iterate through lesson directories in the module
        for lesson_dir in sorted(os.listdir(module_path)):
            lesson_path = os.path.join(module_path, lesson_dir)
            if not os.path.isdir(lesson_path):
                continue

            # Extract lesson name and slug
            lesson_slug_id, lesson_name_raw = lesson_dir.split("@", 1)
            lesson_name = f"Lesson {lesson_slug_id} {lesson_name_raw.replace('-', ' ').title()}"
            full_lesson_slug = f"{lesson_slug_id}@{lesson_name_raw}"

            items = []

            # Iterate through item directories in the lesson
            for item_dir in sorted(os.listdir(lesson_path)):
                item_path = os.path.join(lesson_path, item_dir)
                if not os.path.isdir(item_path):
                    continue

                # Extract item name and slug
                item_slug_id, item_name_raw = item_dir.split("@", 1)
                item_name = item_name_raw.replace("-", " ").title()
                item_full_slug = f"{item_slug_id}@{item_name_raw}"

                # Look for transcript files in the item directory
                content = []
                for file_name in sorted(os.listdir(item_path)):
                    file_path = os.path.join(item_path, file_name)
                    if file_name.endswith(".txt"):
                        content.append({
                            "content_type": "transcript",
                            "file_name": file_name,
                            "path": file_path,
                            "size": os.path.getsize(file_path),
                            "extension": ".txt"
                        })
                    elif file_name.endswith(".mp4"):
                        content.append({
                            "content_type": "video",
                            "file_name": file_name,
                            "path": file_path,
                            "size": os.path.getsize(file_path),
                            "extension": ".mp4"
                        })

                # Build item metadata
                items.append({
                    "name": item_name,
                    "slug": item_name_raw,
                    "transformed_slug": item_full_slug,
                    "path": item_path,
                    "content": content
                })

            # Append lesson metadata
            lessons.append({
                "lesson_name": lesson_name,
                "lesson_slug": full_lesson_slug,
                "items": items
            })

        # Append module metadata
        metadata["modules"].append({
            "module_name": module_name,
            "module_slug": f"{module_slug}@{module_name_raw}",
            "lessons": lessons
        })

    return metadata


def parse_provider(provider_path, output_base_path):
    provider_slug = os.path.basename(provider_path.strip("/"))
    provider_name = provider_slug.replace("-", " ").title()

    # Iterate through courses under the provider
    for course_dir in sorted(os.listdir(provider_path)):
        course_path = os.path.join(provider_path, course_dir)
        if not os.path.isdir(course_path):
            continue

        # Parse the course metadata
        logger.info(f"Processing course: {course_dir}")
        course_metadata = parse_course(course_path)

        # Save course metadata to the appropriate path
        output_dir = os.path.join(output_base_path, provider_slug)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{course_metadata['course_slug']}.json")

        with open(output_file, "w") as f:
            json.dump(course_metadata, f, indent=4)

        logger.info(f"Metadata saved to: {output_file}")


if __name__ == "__main__":
    # Define the default input and output directories
    default_input_path = 'crawled_data/manual_upload'
    default_output_dir = 'crawled_metadata'

    parser = argparse.ArgumentParser(description="Standardize manually uploaded data with provider and course hierarchy.")
    parser.add_argument(
        'input_dir',
        type=str,
        nargs='?',
        default=default_input_path,
        help="Path to the directory containing manually uploaded data organized by provider."
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default=default_output_dir,
        help="Path to the output directory for metadata."
    )

    args = parser.parse_args()

    try:
        logger.info(f"Processing directory: {args.input_dir}")
        for provider_dir in sorted(os.listdir(args.input_dir)):
            provider_path = os.path.join(args.input_dir, provider_dir)
            if not os.path.isdir(provider_path):
                continue

            logger.info(f"Processing provider: {provider_dir}")
            parse_provider(provider_path, args.output_dir)

        logger.info("Process completed successfully.")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
