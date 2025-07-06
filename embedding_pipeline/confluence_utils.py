import os
from atlassian import Confluence
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

# -----------------------------
# Initialize Confluence client
# -----------------------------
confluence = Confluence(
    url=CONFLUENCE_URL,
    # Knowledgebase is public, so this can be omitted
    # username=CONFLUENCE_USERNAME,
    # password=CONFLUENCE_API_TOKEN
)

# -----------------------------
# Functions
# -----------------------------


def get_all_pages(space_key):
    """
    Retrieve ALL pages from a Confluence space by paginating through results.
    :param space_key: Key of the Confluence space (e.g., 'DEV')
    :return: List of all page dicts
    """
    all_pages = []
    start = 0
    limit = 100  # You can adjust this batch size if needed

    while True:
        pages = confluence.get_all_pages_from_space(
            space=space_key,
            start=start,
            limit=limit,
            status=None,
            expand="ancestors,body.storage,version"
        )
        if not pages:
            break

        all_pages.extend(pages)
        start += limit

    return all_pages


def extract_page_content(page):
    """
    Extract structured text from HTML body while preserving headings and list structure.
    :param page: Confluence page dict
    :return: Cleaned, structured text string
    """
    html_content = page['body']['storage']['value']
    soup = BeautifulSoup(html_content, "html.parser")

    lines = []
    for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "pre", "code"]):
        text = element.get_text(strip=True)
        if text:
            if element.name.startswith("h"):
                # Use markdown style for headings
                header_level = int(element.name[1])
                lines.append(f"\n{'#' * header_level} {text}\n")
            else:
                lines.append(text)

    return "\n".join(lines)


def extract_metadata(page):
    """
    Extract stable metadata from a page: ID, title, correct Confluence pretty URL, ancestors, parent, last modified.
    :param page: Confluence page dict
    :return: Metadata dict
    """
    ancestors = [ancestor['id'] for ancestor in page.get('ancestors', [])]
    parent_id = ancestors[-1] if ancestors else None
    last_modified = page.get("version", {}).get("when", None)

    # Build correct URL using _links.webui
    webui_path = page.get("_links", {}).get("webui", "")
    if webui_path.startswith("/"):
        webui_path = webui_path[1:]  # Remove leading slash if present

    # Use base Confluence URL (from .env), making sure no double slashes
    full_url = f"{CONFLUENCE_URL.rstrip('/')}/{webui_path}"

    metadata = {
        "id": page["id"],
        "title": page["title"],
        "url": full_url,
        "ancestors": ",".join(ancestors) if ancestors else None,
        "parent": parent_id,
        "last_modified": last_modified,
    }
    return metadata

