# **Course Crawler**

The **Course Crawler** project leverages Python tools like **Selenium, Scrapy, Requests,** and **BeautifulSoup** to efficiently scrape course data from both static and dynamic web pages. This service designs and implements the pattern for scraping course data, transforming it, and storing it in the Meermind platform.

---

## **Project Setup**

### **1. Poetry Environment Setup**

1. **Ensure Python 3.11.9 is installed with pyenv:**
   ```bash
   pyenv install 3.11.9
   pyenv local 3.11.9
   ```

2. **Set the Python version for Poetry:**
   ```bash
   poetry env use $(pyenv which python)
   ```

3. **Install Dependencies:**
   We have a `pyproject.toml` already present:
   ```bash
   poetry install
   ```

4. **Activate the Poetry Shell (Optional):**
   ```bash
   poetry shell
   ```

---

## **Tools Overview: Differences and Complementary Uses**

| **Tool**         | **Key Strength**                     | **Use Case**                               | **Limitations**                         |
|------------------|---------------------------------------|--------------------------------------------|-----------------------------------------|
| **Selenium**     | Browser automation & JavaScript rendering | Dynamic pages & interaction automation  | Slow, requires browser driver          |
| **Scrapy**       | Crawling framework with pipelines    | Large-scale data extraction, multi-page crawls | Steeper learning curve, limited JavaScript handling |
| **Requests**     | Simple HTTP requests                 | Fetch static HTML or APIs                 | Cannot handle JavaScript-heavy sites   |
| **BeautifulSoup**| HTML parsing                         | Extracting specific data from static HTML | Limited crawling capabilities          |

---

## **Which Tool Should You Use?**

- **Use Selenium**: If you need to **render JavaScript** or **automate interactions** (e.g., logging in, clicking buttons).
- **Use Scrapy**: If you need to **crawl multiple pages** and process **large amounts of data** efficiently.
- **Use Requests + BeautifulSoup**: If the site provides **static HTML** and you only need to extract **specific data** from the page.

### **Complementary Usage:**

- **Requests + BeautifulSoup**: For **fetching and parsing static pages**.
- **Scrapy + Selenium**: For **crawling JavaScript-heavy websites** with **multi-page navigation**.

---

## **Example Scripts**

1. **Selenium Script Example:**
   ```python
   from selenium import webdriver

   driver = webdriver.Chrome()
   driver.get("https://example.com")
   print(f"Title: {driver.title}")
   driver.quit()
   ```

2. **Scrapy Project Initialization:**
   ```bash
   scrapy startproject course_crawler
   cd course_crawler
   scrapy crawl example
   ```

---

## **Contribution Guidelines**

Feel free to open issues or submit pull requests to help improve the **Course Crawler** project. Follow the best practices outlined in our [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## **License**

This project is licensed under the [Apache V2 License](./LICENSE).

---