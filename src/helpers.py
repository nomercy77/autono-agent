import asyncio
from src.data_models.message_model import Message
from src.behaviours.behavior_functions import random_two_word_generator
from src.handlers.handler_functions import hello_handler
from src.agent import AutonomousAgent

"""
Helper functions for agents.
"""

async def init_agent(agent_name: str = "autono_agent"):
    """
    Initialize and return a new AutonomousAgent instance.
    Args:
        agent_name: The name of the agent.
    Returns:
        AutonomousAgent: A new AutonomousAgent instance.
    """
    agent = AutonomousAgent(agent_name)
    return agent


def register_custom_handler(agent, handler_for_type: str = "string", new_handler_function = None):
    """
    Register a custom handler function for a given message type on the agent.
    """
    try:
        agent.register_handler(handler_for_type, new_handler_function)
        return f"Handler: {new_handler_function.__name__} added for {agent.name}"
    except Exception as e:
        print(f"Error at register_custom_handler: {e}")


def register_custom_behavior(agent, behavior_function = None):
    """
    Register custom behavior(s) for the agent.
    Args:
        agent: The agent instance.
        behavior_function: The behavior function to register.
    """
    try:
        agent.behaviors.extend(behavior_function)
    except Exception as e:
        print(f"Error at register_custom_behavior: {e}")


async def create_concrete_agent_instance(
        agent_name: str = "agent 1",
        message_handler: dict = {"type" : "string", "function" : hello_handler}, # passing handler function as default
        behaviors: list = [random_two_word_generator]     # passing current behavior function as default   
        ):
    """
    Create an agent instance with a default handler and behavior.
    Args:
        agent_name: The name of the agent.
        message_handler: The message handler to register.
        behaviors: The behaviors to register.
    Returns:
        AutonomousAgent: A new AutonomousAgent instance.
    """
    try:
        agent = await init_agent(agent_name = agent_name)
        register_custom_handler(agent, message_handler['type'], message_handler['function'])
        register_custom_behavior(agent, behaviors)
        return agent
    except Exception as e:
        print(f"Error creating agent instance: {e}")
        return None


async def run_concurrent_agents(
        agent_names: list = None, 
        init_agent_messages: list[Message] = None, # initial message for each agent
        run_duration_seconds: float = 5 # how long to run the agent conversation
        ):
    """
    Run two agents concurrently, wiring their inboxes and outboxes for message exchange.
    Prints the state of their queues at each cycle.
    Args:
        agent_names: The names of the agents.
        init_agent_messages: The initial messages to send to the agents.
        run_duration_seconds: The duration to run the agent conversation.
    Returns:
        tuple: A tuple containing the two agents.
    """
    if isinstance(agent_names, list):
        if len(agent_names) == 2:
            agent1 = await create_concrete_agent_instance(agent_name = agent_names[0])
            agent2 = await create_concrete_agent_instance(agent_name = agent_names[1])
            if agent1 is None or agent2 is None:
                print("Error: Could not create both agents.")
                return None
            
            # start agents
            agent1.start()
            agent2.start()
            
            # Send initial message to an agent to trigger conversation between them (optional)
            if isinstance(init_agent_messages, list) and all(isinstance(m, Message) for m in init_agent_messages): # type checks
                if len(init_agent_messages) == 2:
                    await agent1.outbox.put(init_agent_messages[0])
                    await agent2.outbox.put(init_agent_messages[1])
            
            cycle = 1
            start_time = asyncio.get_event_loop().time()
            while True:
                now = asyncio.get_event_loop().time()
                if now - start_time >= run_duration_seconds:
                    break
                
                try:
                    agent1_outbox = await agent1.outbox.get()
                    agent2_outbox = await agent2.outbox.get()
                except Exception as e:
                    print(f"Error getting outbox messages: {e}")
                    break
                
                # Print the messages being swapped                    
                print(f"Cycle {cycle} 🚀\n"
                      f"🔄 Swapping: \n"
                      f"  {agent1.name} outbox: {agent1_outbox}  ➡️   {agent2.name} inbox \n"
                      f"  {agent2.name} outbox: {agent2_outbox}  ➡️   {agent1.name} inbox.\n"
                )
                
                # Perform the swap - inbox of agent 1 is the outbox of agent 2 and vice versa
                try:
                    await agent1.inbox.put(agent2_outbox)
                    await agent2.inbox.put(agent1_outbox)
                except Exception as e:
                    print(f"Error putting messages in inbox: {e}")
                
                # Print the current state of the queues - for debugging, please ignore multiple print
                print(
                    f"📥 {agent1.name} inbox:  {list(agent1.inbox._queue)}\n"
                    f"📤 {agent1.name} outbox: {list(agent1.outbox._queue)}\n"
                    f"📥 {agent2.name} inbox:  {list(agent2.inbox._queue)}\n"
                    f"📤 {agent2.name} outbox: {list(agent2.outbox._queue)}\n"
                    f"{'='*60}\n"
                )
                cycle += 1
                await asyncio.sleep(1)  # Keeps the event loop alive
            
            print("\n🛑 Stopping agents..")
            agent1.stop()
            agent2.stop()
            print("\n🏁 Stopped agents.\n")
            return (agent1, agent2)
