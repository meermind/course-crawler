## **Logging Policy for Meermind Projects**

### **1. Log Levels and Usage**

| **Level**   | **Purpose**                           | **Example**                                |
|-------------|---------------------------------------|--------------------------------------------|
| `DEBUG`     | Internal steps and detailed info      | "Processing item: Video Introduction"      |
| `INFO`      | Key stages and progress               | "Starting standardization."               |
| `WARNING`   | Non-critical issues like missing paths| "Item path not found: topic-1"            |
| `ERROR`     | Errors needing attention              | "Failed to load JSON."                    |
| `CRITICAL`  | Fatal issues preventing execution     | "Database connection failed."            |

---

### **2. Log Configuration**

```python
import logging

logging.basicConfig(
    level=logging.INFO,  # Use DEBUG for detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
```

**Format Example:**  
`2024-10-26 22:10:01 - INFO - Standardization completed.`

---

### **3. Example Usage**

```python
logger.info("Starting function.")
try:
    logger.debug("Processing item 1...")
    raise FileNotFoundError("Sample file missing.")
except FileNotFoundError as e:
    logger.warning(f"File not found: {e}")
finally:
    logger.info("Function completed.")
```

---

### **4. Tips**

- Use **`DEBUG`** for detailed processing.
- Keep **`INFO`** logs minimal for clarity.
- Ensure **warnings and errors** provide context for troubleshooting.
- **Rotate logs** in production to prevent large files.
