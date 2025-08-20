import argparse
import json
import logging
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple

from PyPDF2 import PdfReader, PdfWriter


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class ItemRange:
    item_dir_name: str
    start_page_inclusive: int
    end_page_inclusive: int


def parse_page_range(value: str) -> Tuple[int, int]:
    parts = value.split("-")
    if len(parts) != 2:
        raise ValueError(f"Invalid page range format: {value}")
    start_str, end_str = parts
    return int(start_str), int(end_str)


def load_instructions(instructions_path: str) -> List[ItemRange]:
    with open(instructions_path, "r") as f:
        raw = json.load(f)

    items: List[ItemRange] = []
    entries = raw.get("items", raw)  # allow either {items: [...]} or a raw list
    for entry in entries:
        item_dir_name = entry["item_dir"] if "item_dir" in entry else entry["item_name"]

        if "pages" in entry:
            start, end = parse_page_range(entry["pages"])  # e.g. "3-10"
        else:
            start = int(entry["start"])  # 1-based
            end = int(entry["end"])      # 1-based, inclusive

        items.append(
            ItemRange(
                item_dir_name=item_dir_name,
                start_page_inclusive=start,
                end_page_inclusive=end,
            )
        )

    return items


def write_pdf_subset(
    source_pdf_path: str,
    output_pdf_path: str,
    start_page_inclusive: int,
    end_page_inclusive: int,
) -> None:
    reader = PdfReader(source_pdf_path)
    total_pages = len(reader.pages)

    if start_page_inclusive < 1 or end_page_inclusive < 1:
        raise ValueError("Page numbers must be 1-based and positive")
    if start_page_inclusive > end_page_inclusive:
        raise ValueError("Start page must be <= end page")
    if end_page_inclusive > total_pages:
        raise ValueError(
            f"End page {end_page_inclusive} exceeds total pages {total_pages} for {source_pdf_path}"
        )

    writer = PdfWriter()
    for page_index in range(start_page_inclusive - 1, end_page_inclusive):
        writer.add_page(reader.pages[page_index])

    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    with open(output_pdf_path, "wb") as out_f:
        writer.write(out_f)


def split_week_slides(
    week_dir_path: str,
    week_pdf_filename: str,
    instructions_path: str,
    output_filename: str = "slides.pdf",
    dry_run: bool = False,
) -> List[str]:
    week_dir_path = os.path.abspath(week_dir_path)
    source_pdf_path = os.path.join(week_dir_path, week_pdf_filename)

    if not os.path.exists(source_pdf_path):
        raise FileNotFoundError(f"Week PDF not found: {source_pdf_path}")

    items = load_instructions(instructions_path)
    logger.info("Loaded %d instructions", len(items))

    written_paths: List[str] = []
    for item in items:
        item_dir = os.path.join(week_dir_path, item.item_dir_name)
        if not os.path.isdir(item_dir):
            logger.warning("Item directory missing, creating: %s", item_dir)
            if not dry_run:
                os.makedirs(item_dir, exist_ok=True)

        output_pdf_path = os.path.join(item_dir, output_filename)
        logger.info(
            "Extracting pages %s-%s -> %s",
            item.start_page_inclusive,
            item.end_page_inclusive,
            output_pdf_path,
        )

        if not dry_run:
            write_pdf_subset(
                source_pdf_path,
                output_pdf_path,
                item.start_page_inclusive,
                item.end_page_inclusive,
            )
            written_paths.append(output_pdf_path)

    return written_paths


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Split a week's lecture PDF into per-item PDFs based on JSON instructions. "
            "Outputs each subset as slides.pdf into the corresponding item directory."
        )
    )
    parser.add_argument(
        "week_dir",
        help="Path to the week directory containing the full lecture PDF and item subdirectories",
    )
    parser.add_argument(
        "week_pdf",
        help="Filename of the full lecture PDF located inside the week directory",
    )
    parser.add_argument(
        "instructions",
        help=(
            "Path to a JSON file describing items and page ranges.\n"
            "Accepted formats: {\"items\": [{\"item_dir\": \"01@foo\", \"start\": 1, \"end\": 5}, ...]} or "
            "[{\"item_dir\": \"01@foo\", \"pages\": \"1-5\"}, ...]"
        ),
    )
    parser.add_argument(
        "--output-name",
        default="slides.pdf",
        help="Filename to write for each item (default: slides.pdf)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without writing files",
    )

    args = parser.parse_args()

    split_week_slides(
        week_dir_path=args.week_dir,
        week_pdf_filename=args.week_pdf,
        instructions_path=args.instructions,
        output_filename=args.output_name,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()


