import pytest
import asyncio
from main import create_concrete_agent_instance
from src.data_models.message_model import Message

'''
The first test manually simulates the initial message exchange between two agents by placing messages 
in their outboxes and then swapping them into the other agents inbox — exactly as done in the main agent loop (run_concurrent_agents).

Second test just extends the same logic over multiple turns (var: max_cycles, edit to change) of message passing 
by agents, not just the first swap.

Purpose:
By checking the inboxes immediately after the swap, 
we verify that the correct messages are present in each inbox before the agent process_messages() function 
consumes them. This approach ensures the test is not affected by the asynchronous consumption of messages, 
providing a reliable way to assert the state of the inboxes right after a message swap.
'''

@pytest.mark.asyncio
async def test_simulate_initial_message_swap():
    # Create agents but don't start them yet
    agent1 = await create_concrete_agent_instance(agent_name="Agent1")
    agent2 = await create_concrete_agent_instance(agent_name="Agent2")

    try:
        # Each agent sends a Hello to the other agent
        await agent1.outbox.put(Message(type="string", content="Hello Agent2"))
        await agent2.outbox.put(Message(type="string", content="Hello Agent1"))

        # Manually perform the swap: outbox -> other agent's inbox, exactly how it is implemented in the run_concurrent_agents function
        try:
            agent1_outbox_msg = await asyncio.wait_for(agent1.outbox.get(), timeout=2)
            agent2_outbox_msg = await asyncio.wait_for(agent2.outbox.get(), timeout=2)
        except Exception as e:
            pytest.fail(f"Failed to get outbox messages: {e}")

        try:
            await agent1.inbox.put(agent2_outbox_msg)
            await agent2.inbox.put(agent1_outbox_msg)
        except Exception as e:
            pytest.fail(f"Failed to put messages in inbox: {e}")

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
    
    except Exception as e:
        pytest.fail(f"Unexpected error in test_simulate_initial_message_swap: {e}")
    finally:
        agent1.stop()
        agent2.stop()

@pytest.mark.asyncio
async def test_agent_outbox_inbox_swap_consistency(max_cycles: int = 10): # change here if required to run for different number of cycles
    """
    This test starts both agents, runs a loop similar to run_concurrent_agents, and checks that after swapping,
    agent1's outbox message is not equal to agent2's inbox message (and vice versa). If the swap logic is broken,
    the test will fail.
    """
    agent1 = await create_concrete_agent_instance(agent_name="Agent1")
    agent2 = await create_concrete_agent_instance(agent_name="Agent2")

    try:
        # Each agent sends a Hello to the other agent
        await agent1.outbox.put(Message(type="string", content="Hello Agent2"))
        await agent2.outbox.put(Message(type="string", content="Hello Agent1"))

        agent1.start()
        agent2.start()

        swap_consistent = True
        cycles = 0
        while cycles < max_cycles:
            # Get outbox messages
            try:
                agent1_outbox_msg = await asyncio.wait_for(agent1.outbox.get(), timeout=2)
                agent2_outbox_msg = await asyncio.wait_for(agent2.outbox.get(), timeout=2)
            except Exception as e:
                swap_consistent = False
                pytest.fail(f"Failed to get outbox messages in cycle {cycles+1}: {e}")                

            # Swap: outbox -> other agent's inbox
            try:
                await agent1.inbox.put(agent2_outbox_msg)
                await agent2.inbox.put(agent1_outbox_msg)
            except Exception as e:
                swap_consistent = False
                pytest.fail(f"Failed to put messages in inbox in cycle {cycles+1}: {e}")
                
            # Check that after swapping, agent1's outbox message is now in agent2's inbox, and vice versa
            agent1_inbox_list = list(agent1.inbox._queue)
            agent2_inbox_list = list(agent2.inbox._queue)

            if agent1_outbox_msg not in agent2_inbox_list or agent2_outbox_msg not in agent1_inbox_list:
                swap_consistent = False
                pytest.fail(
                    f"Cycle {cycles+1}: Outbox/inbox swap logic failed.\n"
                    f"Expected agent1_outbox_msg in agent2_inbox_list: {agent2_inbox_list}\n"
                    f"Expected agent2_outbox_msg in agent1_inbox_list: {agent1_inbox_list}\n"
                )

            cycles += 1
            await asyncio.sleep(1)
    
    except Exception as e:
        pytest.fail(f"Unexpected error in test_agent_outbox_inbox_swap_consistency: {e}")
    
    finally:
        agent1.stop()
        agent2.stop()

    assert swap_consistent, "Outbox/inbox swap logic failed: swapped messages not found in the correct inbox."
