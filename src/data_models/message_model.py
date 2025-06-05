from dataclasses import dataclass

@dataclass
class Message:
    """
    Represents a message exchanged between agents.
    Attributes:
        type (str): The type/category of the message (e.g., 'string').
        content (str): The actual content of the message.
    """
    type: str      # Type/category of the message
    content: str   # Content of the message

