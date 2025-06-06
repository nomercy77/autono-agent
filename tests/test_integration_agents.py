import pytest
import asyncio
from main import create_concrete_agent_instance
from src.data_models.message_model import Message

'''
This test manually simulates the initial message exchange between two agents by placing messages 
in their outboxes and then swapping them into the other agents inbox — exactly as done in the main agent loop (run_concurrent_agents).

Purpose:
By checking the inboxes immediately after the swap (and before starting the agents), 
we verify that the correct messages are present in each inbox before the agent process_messages() function 
consumes them. This approach ensures the test is not affected by the asynchronous consumption of messages, 
providing a reliable way to assert the state of the inboxes right after a message swap.
'''
@pytest.mark.asyncio
async def simulate_initial_message_swap():
    # Create agents but don't start them yet
    agent1 = await create_concrete_agent_instance(agent_name="Agent1")
    agent2 = await create_concrete_agent_instance(agent_name="Agent2")

    # Each agent sends a Hello to the other agent
    await agent1.outbox.put(Message(type="string", content="Hello Agent2"))
    await agent2.outbox.put(Message(type="string", content="Hello Agent1"))

    # Manually perform the swap: outbox -> other agent's inbox, exactly how it is implemented in the run_concurrent_agents function
    agent1_outbox_msg = await agent1.outbox.get()
    agent2_outbox_msg = await agent2.outbox.get()
    await agent1.inbox.put(agent2_outbox_msg)
    await agent2.inbox.put(agent1_outbox_msg)

    # Now check the inboxes before starting the agents
    inbox1_list = list(agent1.inbox._queue)
    inbox2_list = list(agent2.inbox._queue)

    assert any(
        msg.content == "Hello Agent1" for msg in inbox1_list
    ), f"Agent1's inbox should contain 'Hello Agent1', got: {inbox1_list}"

    assert any(
        msg.content == "Hello Agent2" for msg in inbox2_list
    ), f"Agent2's inbox should contain 'Hello Agent2', got: {inbox2_list}"

    # Now start the agents and let them process the messages
    agent1.start()
    agent2.start()
    await asyncio.sleep(0.1)
    agent1.stop()
    agent2.stop()
