import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)" ,text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_title(markdown: str) -> str:
    title = re.findall(r"(?<=^#{1} ).*", markdown)
    if len(title) == 0:
        raise Exception("No h1 header found!")
    return title[0]


