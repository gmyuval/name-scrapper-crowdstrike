HTML_HEADER = "<html><head><meta charset='utf-8'><title>Animal Collateral Adjectives</title></head>" "<body><h1>Animal Collateral Adjectives</h1><ul>"
HTML_FOOTER = "</ul></body></html>"
OUTPUT_DIR = "../out"
OUTPUT_HTML_FILE_NAME = "output.html"
IMAGE_DIR = "../out/images"
WIKIPEDIA_BASE_URL = "https://en.wikipedia.org"

# HTTP request configuration
MAX_RETRIES = 3  # Maximum number of retry attempts
RETRY_BACKOFF = 1.0  # Base backoff time in seconds (exponential backoff will be used)
CONCURRENT_REQUESTS_LIMIT = 20  # Maximum number of concurrent HTTP requests
