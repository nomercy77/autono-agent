import asyncio
from src.data_models.message_model import Message


class AutonomousAgent:
    """
    Represents an autonomous agent with message handling and behaviors.
    Each agent has an inbox and outbox (asyncio Queues), can register message handlers,
    and behaviors, running concurrently.
    """
    def __init__(self, name="agent"):
        self.name = name
        # State variable to control agent's running state
        self.running = False
        # Inbox and outbox for communication
        self.inbox = asyncio.Queue()
        self.outbox = asyncio.Queue()
        self.message_handlers = {} # message_type -> handler function for it
        self.behaviors = [] # list of behavior functions
        self._tasks = []  # Track background tasks

    def start(self):
        """
        Start the agent's message processing and behaviors as behavior tasks.
        """
        self.running = True
        self._tasks.append(asyncio.create_task(self.process_messages()))
        self._tasks.append(asyncio.create_task(self.start_behaviors()))

    async def start_behaviors(self):
        """
        Run all registered behaviors concurrently as long as the agent is running.
        """
        await asyncio.gather(
            *(behavior(self) for behavior in self.behaviors)
        )

    def stop(self):
        """
        Stop the agent and cancel all background tasks.
        """
        self.running = False
        # Cancel all running tasks
        for task in self._tasks:
            task.cancel()
        # Optionally, you could await these tasks for a clean shutdown

    def register_handler(self, message_type, handler_fn):
        """
        Register a handler function for a specific message type.
        """
        self.message_handlers[message_type] = handler_fn

    async def process_messages(self):
        """
        Continuously process incoming messages from the inbox and handle them using registered handlers and 
        emit to outbox
        """
        while self.running:
            try:
                message = await self.inbox.get()
                handler = self.message_handlers.get(message.type)
                if not handler:
                    await self.outbox.put(Message(type=message.type, content=message.content))
                    continue
                
                handled_message = handler(message.content)
                await self.outbox.put(handled_message)
                
            except Exception as e:
                print(f"Agent {self.name} error: {e}")
