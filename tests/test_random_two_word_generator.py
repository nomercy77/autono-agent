import pytest
import asyncio
from src.behaviours.behavior_functions import random_two_word_generator
from src.data_models.message_model import Message

class MockAgent:
    def __init__(self):
        self.running = True
        self.outbox = asyncio.Queue()

@pytest.mark.asyncio
async def test_random_two_word_generator():
    agent = MockAgent()
    # Run the generator for a short time, then stop
    task = asyncio.create_task(random_two_word_generator(agent))
    await asyncio.sleep(2.5)  # Should generate at least one message
    agent.running = False
    await task  # Wait for the task to finish

    # Check that at least one message was put in the outbox
    assert not agent.outbox.empty()
    msg = await agent.outbox.get()
    assert isinstance(msg, Message)
    assert msg.type == "string"
    # Check that the content is two words from the alphabet
    words = msg.content.split()
    assert len(words) == 2
    alphabet = ['hello', 'sun', 'world', 'space', 'moon', 'crypto', 'sky', 'ocean', 'universe', 'human']
    assert words[0] in alphabet and words[1] in alphabet and words[0] != words[1] 