import asyncio
from src.data_models.message_model import Message
from src.helpers import create_concrete_agent_instance, run_concurrent_agents


if __name__ == "__main__":
    print("Choose mode:")
    print("1. Single-agent mode")
    print("2. Multi-agent mode (default)")
    mode = input("Enter 1 or 2: ").strip()

    if mode == "1": # Single-agent mode
        agent_name = input("Enter agent name (default: Agent1): ").strip() or "Agent1"
        run_duration = input("Enter run duration in seconds (default: 5): ").strip()
        
        try:
            run_duration = float(run_duration) if run_duration else 5.0
        except ValueError:
            run_duration = 5.0
        
        async def run_single_agent():
            """
            Run a single agent for the specified duration, printing its inbox and outbox each second.
            """
            agent = await create_concrete_agent_instance(agent_name=agent_name)
            if agent is None:
                print("Error: Could not create agent.")
                return
            agent.start()
            print(f"Single agent '{agent_name}' started. Will run for {run_duration} seconds.")
            
            try:
                start_time = asyncio.get_event_loop().time()
                cycle = 1
                while True:
                    now = asyncio.get_event_loop().time()
                    if now - start_time >= run_duration:
                        break
                    print(f"Cycle {cycle} 🚀\n")
                    print(f"📥 {agent.name} inbox:  {list(agent.inbox._queue)}")
                    print(f"📤 {agent.name} outbox: {list(agent.outbox._queue)}\n")
                    print(f"{'='*60}\n")
                    cycle += 1
                    await asyncio.sleep(1)            
            except KeyboardInterrupt:
                print("\nStopping agent...")
            agent.stop()
            # Print inbox and outbox messages after run
            print(f"\n📥 {agent.name} inbox:  {list(agent.inbox._queue)}")
            print(f"📤 {agent.name} outbox: {list(agent.outbox._queue)}\n")
        asyncio.run(run_single_agent())
    
    else: # Multi-agent mode (default)
        agent1_name = input("Enter first agent name (default: Agent1): ").strip() or "Agent1"
        agent2_name = input("Enter second agent name (default: Agent2): ").strip() or "Agent2"
        run_duration = input("Enter run duration in seconds (default: 5): ").strip()
        
        try:
            run_duration = float(run_duration) if run_duration else 5.0
        except ValueError:
            run_duration = 5.0
        agent_names = [agent1_name, agent2_name]
        agent_init_messages = [ 
            Message(type = "string", content = f"Hello {agent_names[1]}"),
            Message(type = "string", content = f"Hello {agent_names[0]}"),                                                                      
        ] 
        asyncio.run(run_concurrent_agents(agent_names, agent_init_messages, run_duration))

