from ..data_models.message_model import Message

"""
Handler functions for processing incoming messages for agents.
"""

def hello_handler(message_content):
    """
    Processes a message and returns a Message object if 'hello' is found in the content (case-insensitive).
    If 'hello' is not found, returns a Message with content 'Hello_not_found'.
    Args:
        message_content: The content of the incoming message (any type).
    Returns:
        Message: A Message object with the appropriate content.
    """
    try:
        # Ensure the message content is a string
        if not isinstance(message_content, str):
            message_content = str(message_content)
        # Check for 'hello' in the message (case-insensitive)
        if "hello" in message_content.lower():
            return Message('string', message_content)
        else:
            return Message('string', 'hello_not_found')
    except Exception as e:
        # Handle any unexpected errors
        print(f"Error in hello_handler: {e}")
        return Message('string', message_content)
    