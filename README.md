# AI Agents Repository

This repository contains AI agents showcased during the 10x Meetup presentation. The project demonstrates building agents using two popular frameworks: **CrewAI** and **LangChain**.


---

## Frameworks & Agents

### Frameworks Used
- **CrewAI**
- **LangChain**

- 
### Agents
- **Researcher Agent**: A deep research agent that can search the web, gather relevant information, and then summarize the output into a comprehensive report.
- **Booking Agent**: Utilizes the CrewAI hierarchy approach to coordinate multiple agents in solving complex problems.
- **SQL Agent**: Translates natural language queries into SQL queries, executes them (including refining the query if necessary), and returns the results.

---

## Running the CrewAI Examples

Follow these steps to run the examples built with CrewAI:

```code
- cd crewai-agents
- python -m venv .venv (I used python 3.12.4)
- pip install crewai
- crewai run
```

### Running the LangChain/LangGraph example

Follow these steps to run the examples built with Langchain/LangGraph:

```code
- cd langchain-sql-agent
- python -m venv .venv (I used python 3.12.4)
- pip install -U langgraph langchain_openai langchain_community
- python sql_agent.py
```
