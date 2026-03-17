# AI Agent Framework

A custom-built Python framework for creating autonomous AI agents using OpenRouter (OpenAI SDK). The project implements several agent architectures, ranging from basic conversational loops to advanced ReAct and Plan-and-Execute systems.

## 🚀 Features

- **ReAct Architecture (`react.py`)**: A custom reasoning loop where the agent outputs JSON to think, act, and observe results before providing a final answer.
- **Planner Agent (`agents/planingPart.py`)**: A multi-agent framework that breaks a user's goal into discrete execution steps before attempting to execute tools.
- **Custom Tools Protocol**: Tools are defined in `tools.py` using a schema that the agents automatically parse and inject into their system prompts.
  - `whether_api`: Geocodes a city name and fetches current weather data.
  - `wikipedia_search`: Uses the Wikimedia REST API to fetch summaries of topics.
- **OpenRouter Support**: Uses OpenRouter models (`openrouter/free`) by default to generate responses, meaning it doesn't strictly depend on OpenAI's expensive proprietary endpoints. Includes error handling for rate limits.

## 📦 File Structure

- `agents/planingPart.py`: The autonomous planner and execution agent.
- `react.py`: The autonomous ReAct loop agent handling tool execution.
- `agent.py`: A basic chat agent capturing multi-turn conversations.
- `whetherAgent.py`: Agent demonstrating direct tool usage.
- `tools.py`: Definition of all available executable tools (weather, wiki search).
- `config.py`: Contains system prompts formatted for JSON-based ReAct parsing.

## 🛠️ Setup & Installation

1. Create a python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the required dependencies:
   ```bash
   pip install openai python-dotenv requests
   ```
3. Create a `.env` file in the root directory and add your OpenRouter API Key:
   ```properties
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

## 🎮 Running the Agents

Run the ReAct agent:
```bash
python3 react.py
```

Run the Plan-and-Execute module:
```bash
python3 agents/planingPart.py
```
