from src.handlers.handler_functions import hello_handler
from src.data_models.message_model import Message

def test_hello_found():
    msg = "Hello there!"
    result = hello_handler(msg)
    assert isinstance(result, Message)
    assert result.type == "string"
    assert result.content == msg

def test_hello_not_found():
    msg = "Goodbye!"
    result = hello_handler(msg)
    assert isinstance(result, Message)
    assert result.type == "string"
    assert result.content == "Hello_not_found"

def test_hello_case_insensitivity():
    msg = "hElLo, how are you?"
    result = hello_handler(msg)
    assert result.content == msg

def test_hello_with_punctuation():
    msg = "Well, hello!"
    result = hello_handler(msg)
    assert result.content == msg

def test_hello_embedded_word():
    msg = "shelloworld"
    result = hello_handler(msg)
    # Should match 'hello' inside the word
    assert result.content == msg

def test_empty_string():
    msg = ""
    result = hello_handler(msg)
    assert result.content == "Hello_not_found"

def test_numbers_and_symbols():
    msg = "1234!@#$"
    result = hello_handler(msg)
    assert result.content == "Hello_not_found"

def test_non_string_input():
    msg = 12345
    result = hello_handler(msg)
    assert result.content == "Hello_not_found" 