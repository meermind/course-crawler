# **Crawled Data using dl_coursera**

This document describes the **use of `dl_coursera`** for scraping Coursera course data and outlines the **metadata standardization process** with our `standardize_dl_coursera_metadata.py` script.

---

## **Command Used for Crawling:**

```bash
dl_coursera --cookies secrets/cookies-coursera-org.txt \
            --slug uol-cm2025-computer-security \
            --outdir crawled_data \
            --how builtin
```

---

## **Approach**

- We **leverage existing tools** (e.g., `dl_coursera`) to avoid reinventing the wheel.  
- See the **[dl_coursera GitHub](https://github.com/FLZ101/dl_coursera?tab=readme-ov-file)** for installation and usage details.  
- Our tool **extends functionality** by standardizing crawled metadata for further use and **processing transcripts** into structured formats.

---

## **Metadata Standardization**

We use the **`standardize_metadata.py`** script to process the crawled data and organize it consistently.  
The script:
1. **Processes course, module, lesson, and item metadata**.
2. **Matches files with folder paths**.
3. **Collects metadata** for each item (e.g., content type, size, path).

### **Usage**

```bash
python crawlers/dl_coursera/standardize_metadata.py \
    crawled_data/dl_coursera/uol-cm2025-computer-security.crawl.json \
    --output_file crawled_metadata/dl_coursera/uol-cm2025-computer-security.json
```

###  **Output:**  
   - A JSON file containing **hierarchical metadata** (course → module → lesson → item), including:
     - File paths
     - Content types (e.g., video, transcript)
     - File sizes

---

## **Example Script Output Structure**

```json
{
  "course_slug": "uol-cm2025-computer-security",
  "course_name": "CM2025 Computer Security",
  "modules": [
    {
      "module_name": "Introduction to Computer Security",
      "module_slug": "01@topic-1-introduction",
      "lessons": [
        {
          "lesson_name": "Lesson 1: Course Overview",
          "lesson_slug": "01@lesson-1-overview",
          "items": [
            {
              "name": "Intro Video",
              "slug": "intro-video",
              "transformed_slug": "01@intro-video",
              "path": "crawled_data/uol-cm2025/01@lesson-1/01@intro-video",
              "content": [
                {
                  "content_type": "video",
                  "file_name": "01@.mp4",
                  "path": "crawled_data/uol-cm2025/.../01@.mp4",
                  "size": 1048576,
                  "extension": ".mp4"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

Here’s a concise section focusing on **Transcript Processing**:

---

## **Transcript Processing**

We handle transcripts through two key scripts:

1. **`process_all_transcripts.py`** (Main Entry Point)  
   - Processes all transcripts listed in the **crawled metadata**.
   - **Generates structured outputs** (JSON & plain text) for each transcript.
   - **Usage**:
     ```bash
     python process_all_transcripts.py --metadata_file crawled_metadata/dl_coursera/uol-cm2025-computer-security.json \
                                       --output_base_dir outputs/structured_transcripts/dl_coursera
     ```

2. **`transcript_formatter.py`** (Individual Entry Point)  
   - Formats a **single transcript file** (SRT) into JSON and plain text.
   - **Usage**:
     ```bash
     python transcript_formatter.py --input_file raw_transcript.srt \
                                    --output_json formatted_transcript.json \
                                    --output_txt formatted_transcript.txt
     ```

Both scripts ensure transcripts are **consistently structured and integrated** into the output data.


---

## **Troubleshooting**

1. **Missing Paths:**  
   - Ensure the folder structure matches the crawled metadata.
   - Use `DEBUG` logs to verify item matching.

2. **Authentication Issues:**  
   - For the dl_coursera crawler, verify the validity of `secrets/cookies-coursera-org.txt`. This may need to be refreshed every couple of weeks.
