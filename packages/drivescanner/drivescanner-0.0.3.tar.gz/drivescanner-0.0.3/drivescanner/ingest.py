import textractplus as tp
from textractplus.exceptions import MissingFileError
from bs4 import UnicodeDammit, BeautifulSoup
import re
from typing import Tuple
from drivescanner.file_index import _replace_backslash
import PyPDF2


def _read_bytes(filepath: str) -> Tuple[bytearray, str]:
    """
    It reads the file and returns the content as a bytearray

    Args:
      filepath (str): the path to the file to be read

    Returns:
      A bytearray
    """
    try:
        content = tp.process(filepath)
        errormsg = None
    except ModuleNotFoundError:
        content = None
        errormsg = "Filetype cannot be processed"
    except MissingFileError:
        content = None
        errormsg = "File not found"
    except Exception as e:
        content = None
        errormsg = e
    return content, errormsg


def _decode_bytearray(
    bytestring: bytearray, try_encoding: list[str]
) -> Tuple[str, str]:
    """
    If the bytestring is not None, then try to decode it using the encoding derived
    from the bytestring or try to decode it using the encoding specified in the
    using some predefined encodings

    Args:
      bytestring (bytearray): the bytearray to decode
      try_encoding (list[str]): a list of encodings to try.

    Returns:
      the content of the bytestring as a decoded string
    """
    possible_encoding = UnicodeDammit(bytestring).original_encoding
    content = None
    if (possible_encoding is not None) & (possible_encoding not in try_encoding):
        try_encoding.insert(0, possible_encoding)
    for enc in try_encoding:
        if content is None:
            try:
                content = bytestring.decode(enc)
            except UnicodeDecodeError:
                pass
    if content is None:
        errormsg = "File encoding unknown"
    else:
        errormsg = None
    return content, errormsg


def _clean_text(text: str) -> Tuple[str, str]:
    """
    It removes HTML and XML characters, and replaces all new lines and white spaces like tabs with a
    space

    Args:
      text (str): the text to be cleaned

    Returns:
      A string with no new lines or tabs.
    """
    # remove HTML and XML characters
    text = BeautifulSoup(text).get_text()
    # replace all new lines and white spaces like tabs with a space
    text = re.sub(r"\s", " ", text)
    return text, None


def _pdf_to_string(pdf_file: str) -> Tuple[str, str]:
    """
    It opens the PDF file, reads the text from each page, and returns the text as a string

    Args:
      pdf_file (str): The path to the PDF file.

    Returns:
      A tuple of two strings, the content and/or the error message (if any) while processing the file.
    """
    try:
        with open(pdf_file, "rb") as pdf:
            reader = PyPDF2.PdfReader(pdf, strict=False)
            pdf_text = []

            for page in reader.pages:
                content = page.extract_text()
                pdf_text.append(content)

            content = " ".join(pdf_text)
            errormsg = None
    except FileNotFoundError:
        content = None
        errormsg = "File not found"
    except Exception as e:
        content = None
        errormsg = e
    return content, errormsg


def ingest_file(
    filepath: str, try_encoding: list[str] = ["utf-8", "iso-8859-1"]
) -> Tuple[str, str]:
    """
    It reads a file, tries to decode it, and then cleans it

    Args:
      filepath (str): str = the path to the file you want to ingest
      try_encoding (list[str]): list[str] = ["utf-8", "iso-8859-1"]

    Returns:
      A string
    """
    filepath = _replace_backslash(filepath)

    if filepath.lower().endswith(".pdf"):
        # use PyPDF2
        content, errormsg = _pdf_to_string(filepath)
    else:
        # use textractplus
        content, errormsg = _read_bytes(filepath=filepath)
        if (content is not None) and (errormsg is None):
            content, errormsg = _decode_bytearray(
                bytestring=content, try_encoding=try_encoding
            )

    if (content is not None) and (errormsg is None):
        content, errormsg = _clean_text(content)

    return content, errormsg
