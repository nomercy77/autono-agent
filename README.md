# 🤖 autono-agent

A Python framework for experimenting with autonomous agents that communicate via message queues. Supports both single-agent and multi-agent modes, with customizable behaviors and message handlers.

---

## 📁 Directory Structure

```
autono-agent/
│
├── main.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── agent.py
│   ├── helpers.py
│   ├── behaviours/
│   │   └── behavior_functions.py
│   ├── data_models/
│   │   └── message_model.py
│   └── handlers/
│       └── handler_functions.py
│
├── tests/
│   ├── test_hello_handler.py
│   ├── test_integration_agents.py
│   ├── test_random_two_word_generator.py
```

---

## 🐍 Python Version

> **Recommended Python >=3.9**

---

## 📦 Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/nomercy77/autono-agent.git
    cd autono-agent
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
    - On Windows: `venv\Scripts\activate`

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

---

## 🚀 Usage

### Run the main program

```sh
python main.py
```

You will be prompted to select a mode:

- **1. Single-agent mode:**  
  - Enter the agent's name (or press Enter for default).
  - Enter the run duration in seconds (or press Enter for default 5).
  - The agent will run, and you will see its inbox and outbox messages printed live.

- **2. Multi-agent mode (default):**  
  - Enter names for both agents (or press Enter for defaults).
  - Enter the run duration in seconds (or press Enter for default 5).
  - Both agents will run, exchange messages, and you will see their inboxes and outboxes printed live.

---

## 🛠️ Customization

- **Change initial messages:**  
  Edit the `agent_init_messages` variable in `main.py` to tweak what messages agents send at startup.

- **Add new behaviors or handlers:**  
  Implement new functions in `src/behaviours/behavior_functions.py` or `src/handlers/handler_functions.py` and register them with your agents.

---

## 🧪 Running Tests

To run all tests:

```sh
pytest tests/{test_file_name}.py
```

- Tests cover agent integration, message handling, and behaviors.
