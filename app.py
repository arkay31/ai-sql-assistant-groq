import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import pandas as pd
import ast

# ===============================
# Load Environment Variables
# ===============================
load_dotenv()

# ===============================
# Streamlit Page Config
# ===============================
st.set_page_config(page_title="AI SQL Assistant", page_icon="🦜")
st.title("🦜 AI SQL Assistant (Groq Powered)")
st.caption("Ask questions in natural language and get results from the database.")

# ===============================
# Initialize Groq LLM
# ===============================
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant"
)

# ===============================
# Configure SQLite Database
# ===============================
@st.cache_resource
def configure_db():
    db_path = (Path(__file__).parent / "student.db").absolute()
    creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    return SQLDatabase(create_engine("sqlite:///", creator=creator))

db = configure_db()

# ===============================
# Create SQL Agent
# ===============================
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=False,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# ===============================
# Chat History
# ===============================
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi 👋 Ask me anything about the student database!"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ===============================
# User Input
# ===============================
user_query = st.chat_input("Ask a question about the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        try:
            result = agent.invoke({"input": user_query})
            response = result["output"]

            # Try converting response into table format
            try:
                data = ast.literal_eval(response)
                if isinstance(data, list) and len(data) > 0:
                    df = pd.DataFrame(data, columns=["Name", "Class", "Section", "Marks"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.write(response)
            except:
                st.write(response)

            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            error_message = f"⚠️ Error: {str(e)}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
