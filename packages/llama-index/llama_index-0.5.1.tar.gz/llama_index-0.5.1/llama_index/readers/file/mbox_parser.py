"""Mbox parser.

Contains simple parser for mbox files.

"""
from pathlib import Path
from typing import Any, Dict, List

from llama_index.readers.file.base_parser import BaseParser


class MboxParser(BaseParser):
    """Mbox parser.

    Extract messages from mailbox files.
    Returns string including date, subject, sender, receiver and
    content for each message.

    """

    DEFAULT_MESSAGE_FORMAT: str = (
        "Date: {_date}\n"
        "From: {_from}\n"
        "To: {_to}\n"
        "Subject: {_subject}\n"
        "Content: {_content}"
    )

    def __init__(
        self,
        *args: Any,
        max_count: int = 0,
        message_format: str = DEFAULT_MESSAGE_FORMAT,
        **kwargs: Any
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self.max_count = max_count
        self.message_format = message_format

    def _init_parser(self) -> Dict:
        """Initialize parser."""
        try:
            from bs4 import BeautifulSoup  # noqa: F401
        except ImportError:
            raise ImportError(
                "`beautifulsoup4` package not found: `pip install beautifulsoup4`"
            )
        return {}

    def parse_file(self, filepath: Path, errors: str = "ignore") -> List[str]:
        """Parse file into string."""
        # Import required libraries
        import mailbox
        from email.parser import BytesParser
        from email.policy import default

        from bs4 import BeautifulSoup

        i = 0
        results: List[str] = []
        # Load file using mailbox
        bytes_parser = BytesParser(policy=default).parse
        mbox = mailbox.mbox(filepath, factory=bytes_parser)  # type: ignore

        # Iterate through all messages
        for _, _msg in enumerate(mbox):
            msg: mailbox.mboxMessage = _msg
            # Parse multipart messages
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get("Content-Disposition"))
                    if ctype == "text/plain" and "attachment" not in cdispo:
                        content = part.get_payload(decode=True)  # decode
                        break
            # Get plain message payload for non-multipart messages
            else:
                content = msg.get_payload(decode=True)

            # Parse message HTML content and remove unneeded whitespace
            soup = BeautifulSoup(content)
            stripped_content = " ".join(soup.get_text().split())
            # Format message to include date, sender, receiver and subject
            msg_string = self.message_format.format(
                _date=msg["date"],
                _from=msg["from"],
                _to=msg["to"],
                _subject=msg["subject"],
                _content=stripped_content,
            )
            # Add message string to results
            results.append(msg_string)
            # Increment counter and return if max count is met
            i += 1
            if self.max_count > 0 and i >= self.max_count:
                break
        return results
