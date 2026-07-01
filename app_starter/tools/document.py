from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path
from pydantic import Field

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    path: str = Field(description="Absolute or relative path to a PDF or DOCX file"),
) -> str:
    """Convert a PDF or DOCX file at the given path to markdown text.

    Reads the file from disk and returns its contents as a markdown-formatted
    string. Useful when the caller has a file path rather than binary data.

    When to use:
    - When you have a local file path to a document and need its text content
    - As an alternative to binary_document_to_markdown when working with files on disk

    Examples:
    >>> document_path_to_markdown("/docs/report.pdf")
    "# Report\\n\\nContent here..."
    """
    p = Path(path)

    if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{p.suffix}'. Must be one of: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    if not p.exists():
        raise FileNotFoundError(f"No file found at '{path}'")

    binary_data = p.read_bytes()

    if not binary_data:
        return ""

    return binary_document_to_markdown(binary_data, p.suffix.lstrip("."))
