# **Crawled Data using `manual_upload`**

This document describes the **use of `manual_upload`** for organizing manually provided data (e.g., transcripts) and outlines the **metadata standardization process** using the `standardize_metadata.py` script.

---

## **Purpose**

The `manual_upload` crawler is designed to handle data that is manually uploaded into a predefined directory structure. This is particularly useful for integrating manually provided files into our metadata pipeline. The script processes the provided hierarchy into a consistent metadata format that supports downstream use cases.

---

## **Directory Structure**

The `manual_upload` platform expects data to be organized as follows:

```
crawled_data/manual_upload/
    provider_name/
        course_name/
            module_name/
                lesson_name/
                    item_name/
                        transcript.txt
                        ...
```

### **Example:**
```
crawled_data/manual_upload/
    deeplearning/
        intro-to-federated-learning/
            01@topic01-intro-to-federated-learning/
                01@lesson01-introduction/
                    01@introduction/
                        1. Introduction.txt
                02@lesson02-why-federated-learning/
                    02@why-federated-learning/
                        2. Why Federated Learning.txt
                03@lesson03-federated-training-process/
                    03@federated-training-process/
                        3. Federated Training Process.txt
            02@topic02-tuning-and-privacy/
                01@lesson01-tuning/
                    01@tuning/
                        4. Tuning.txt
                02@lesson02-data-privacy/
                    02@data-privacy/
                        5. Data Privacy.txt
            03@topic03-bandwidth/
                01@lesson01-bandwidth/
                    01@bandwidth/
                        6. Bandwidth.txt
                02@lesson02-conclusion/
                    02@conclusion/
                        7. Conclusion.txt
```

---

## **Metadata Standardization**

The **`standardize_metadata.py`** script processes the manually uploaded data and organizes it into a standardized format.  

### **Script Functionality:**
1. Extracts **course**, **module**, **lesson**, and **item** metadata based on directory structure.
2. Maps files to their respective **content types** (e.g., transcript, video).
3. Collects metadata for each file, including:
   - Content type
   - File name
   - File path
   - File size
   - File extension

---

## **Usage**

Run the script with the following command:

```bash
python crawlers/manual_upload/standardize_metadata.py \
    crawled_data/manual_upload \
    --output_dir crawled_metadata
```

### **Arguments:**
- **`input_dir`**: Path to the directory containing manually uploaded data organized by provider (default: `crawled_data/manual_upload`).
- **`--output_dir`**: Path to the output directory where the standardized metadata files will be saved (default: `crawled_metadata`).

---

## **Output**

The script generates **hierarchical metadata** for each course under its respective provider.  
The output is saved as:

```
crawled_metadata/
    provider_name/
        course_name.json
```

---

## **Example Script Output Structure**

```json
{
  "course_slug": "intro-to-federated-learning",
  "course_name": "Intro To Federated Learning",
  "modules": [
    {
      "module_name": "Topic 1 Introduction To Federated Learning",
      "module_slug": "01@topic01-introduction-to-federated-learning",
      "lessons": [
        {
          "lesson_name": "Lesson 1 Introduction",
          "lesson_slug": "01@lesson01-introduction",
          "items": [
            {
              "name": "Introduction",
              "slug": "introduction",
              "transformed_slug": "01@introduction",
              "path": "crawled_data/manual_upload/deeplearning/intro-to-federated-learning/01@topic01-introduction-to-federated-learning/01@lesson01-introduction/01@introduction",
              "content": [
                {
                  "content_type": "transcript",
                  "file_name": "1. Introduction.txt",
                  "path": "crawled_data/manual_upload/deeplearning/intro-to-federated-learning/01@topic01-introduction-to-federated-learning/01@lesson01-introduction/01@introduction/1. Introduction.txt",
                  "size": 1234,
                  "extension": ".txt"
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

---

## **Best Practices**

1. **Adhere to the expected directory structure**:
   - Organize files as `manual_upload/provider_name/course_name/module_name/lesson_name/item_name/`.
2. **Descriptive filenames**:
   - Use clear, consistent naming for transcripts and other files (e.g., `1. Introduction.txt`).
3. **Run the standardization script**:
   - Standardize metadata after every upload to keep files organized and ready for processing.
