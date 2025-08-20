from pathlib import Path
import json
import shutil

from crawlers.dl_coursera.standardize_metadata import parse_and_standardize


def test_parse_and_standardize_manual_upload(tmp_path: Path):
    fixtures_root = Path(__file__).parent / "data" / "manual_upload"

    # Load example input JSON
    with open(fixtures_root / "input.json", "r") as f:
        data = json.load(f)

    # Prepare a temp base path that mirrors the expected crawler layout
    # base_path/course_slug/module_slug/lesson_slug/{item_folder}
    base_path = tmp_path / "crawled_data" / "dl_coursera"
    src_fs = fixtures_root / "fs"
    shutil.copytree(src_fs, base_path, dirs_exist_ok=True)

    result = parse_and_standardize(data, str(base_path))

    # Top-level checks
    assert result["course_slug"] == "sample-course"
    assert result["course_name"] == "Sample Course"
    assert len(result["modules"]) == 1

    module = result["modules"][0]
    assert module["module_name"] == "Introduction"
    assert module["module_slug"] == "01@intro-module"
    assert len(module["lessons"]) == 1

    lesson = module["lessons"][0]
    assert lesson["lesson_name"] == "Lesson One"
    assert lesson["lesson_slug"] == "01@lesson-one"
    assert len(lesson["items"]) == 1

    item = lesson["items"][0]
    assert item["name"] == "Getting Started"
    assert item["slug"] == "getting-started"
    assert item["transformed_slug"] == "01@getting-started"

    # Content checks: compare stable fields only (type, name, extension)
    content = item["content"]
    got = {(c["content_type"], c["file_name"], c["extension"]) for c in content}
    expected = {
        ("video", "video.mp4", ".mp4"),
        ("document", "notes.pdf", ".pdf"),
        ("transcript", "transcript.srt", ".srt"),
        ("webpage", "page.html", ".html"),
    }
    assert expected.issubset(got)


