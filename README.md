# 🦜 AI SQL Assistant (Groq + LangChain)

An AI-powered Natural Language to SQL assistant built using LangChain and Groq (LLaMA 3.1).  
This application allows users to query a SQL database using plain English and automatically converts queries into executable SQL statements.

## 🚀 Features

- Natural Language → SQL conversion
- Autonomous LangChain Agent (ReAct pattern)
- Groq LLaMA 3.1 integration (free LLM)
- SQLite database backend
- Streamlit interactive UI
- Tool-using AI architecture
- Automatic schema inspection and query validation

## 🧠 Architecture

User → Streamlit UI → LangChain Agent → Groq LLM → SQL Toolkit → SQLite DB → Response

The agent follows a reasoning-based approach:
1. Inspect tables
2. Check schema
3. Generate SQL
4. Validate query
5. Execute query
6. Return structured result

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq (LLaMA 3.1)
- SQLite
- SQLAlchemy

## 📦 Installation

```bash
git clone https://github.com/arkay31/ai-sql-assistant-groq.git
cd ai-sql-assistant-groq
pip install -r requirements.txt

