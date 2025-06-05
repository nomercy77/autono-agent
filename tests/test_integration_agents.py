import pytest
import asyncio
from main import run_concurrent_agents
from src.data_models.message_model import Message

@pytest.mark.asyncio
async def test_two_agents_initial_message_exchange():
    agent_names = ["Agent1", "Agent2"]
    agent_init_messages = [
        Message(type="string", content="Hello Agent2"),
        Message(type="string", content="Hello Agent1"),
    ]
    run_duration = 0.5 # to make sure we have 1 cycle 

    # Run the agents 
    agent1, agent2 = await run_concurrent_agents(
        agent_names=agent_names,
        init_agent_messages=agent_init_messages,
        run_duration_seconds=run_duration
    )

    # Give a moment for any final messages to flush
    await asyncio.sleep(0.1)

    # After running the agents
    out1_list = list(agent1.outbox._queue)
    out2_list = list(agent2.outbox._queue)

    # Agent1's outbox should contain a reply to 'Hello Agent1'
    assert any(
        msg.content == "Hello Agent1" for msg in out1_list
    ), f"Agent1's outbox should contain 'Hello Agent1', got: {out1_list}"

    # Agent2's outbox should contain a reply to 'Hello Agent2'
    assert any(
        msg.content == "Hello Agent2" for msg in out2_list
    ), f"Agent2's outbox should contain 'Hello Agent2', got: {out2_list}"

    # stop agents and let all tasks finish
    agent1.stop()
    agent2.stop()