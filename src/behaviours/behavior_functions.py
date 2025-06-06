import asyncio
import random
from ..data_models.message_model import Message

"""
Behavior functions for agents.
"""

async def random_two_word_generator(agent):
    """
    Periodically generates a random two-word message from a predefined vocabulary
    and puts it into the agent's outbox every 2 seconds, as long as the agent is running.
    Args:
        agent: The agent instance with an 'outbox' asyncio.Queue and a 'running' flag.
    """
    alphabet = ['hello', 'sun', 'world', 'space', 'moon', 'crypto', 'sky', 'ocean', 'universe', 'human']
    check_interval_seconds = 2
    
    # checking agent state
    while agent.running:
        word1, word2 = random.sample(alphabet, 2)  # Pick two different words
        word_combo = Message("string", f"{word1} {word2}")
        try:
            await agent.outbox.put(word_combo)  # Put the message in the outbox
        except Exception as e:
            # Handle errors, e.g., if the queue is closed
            print(f"Error putting random generate message in outbox: {e}")
        await asyncio.sleep(check_interval_seconds)  # Wait before generating the next message