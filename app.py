import os

import sqlalchemy as sa
from langchain.cache import InMemoryCache
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
import langchain
import streamlit as st
from io import StringIO
import contextlib

st.markdown(
    """
    <style>
    body {
        color: #FAFAFA;
        background-color: #0E1117;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Database URLs
DATABASES = {
    "Crimes": sa.URL.create(
        "mysql+pymysql",
        username="root",
        password="nl2sql",
        host="localhost",
        port=3306,
        database="crimes",
    ),
    "Happiness": sa.URL.create(
        "mysql+pymysql",
        username="root",
        password="nl2sql",
        host="localhost",
        port=3306,
        database="happiness",
    ),
    "Hospitality": sa.URL.create(
        "mysql+pymysql",
        username="root",
        password="nl2sql",
        host="localhost",
        port=3306,
        database="hospitality",
    ),
}


# Initialize the appropriate model
def initialize_query_executor(model_name, database_name):
    db = SQLDatabase.from_uri(DATABASES[database_name])
    langchain.llm_cache = InMemoryCache()
    
    llm_completions = ChatOpenAI(
    temperature=0,
    model="gpt-4o",
    openai_api_key=os.getenv("OPENAI_KEY"),
    cache=True,
)

    if model_name == "SQLAgent":
        query_executor = create_sql_agent(
            llm=llm_completions, 
            db=db, 
            agent_type="openai-tools", 
            verbose=True
        )
    elif model_name == "SQLDatabaseChain":
        query_executor = SQLDatabaseChain(
            llm=llm_completions, 
            database=db, 
            verbose=True
        )
    else:
        raise ValueError("Invalid model name")

    return query_executor


# Function to process a query and capture verbose output
def process_query(query, model_name, database_name):
    query_executor = initialize_query_executor(model_name, database_name)

    # Capture verbose output
    verbose_output = StringIO()
    with contextlib.redirect_stdout(
        verbose_output
    ):  # Redirect stdout to capture verbose logs
        result = query_executor.invoke(query)

    return result, verbose_output.getvalue()


# Streamlit app layout
st.header("Nl2SQL", divider="orange")

# Model selection
model_name = st.selectbox("Choose the model", ("SQLDatabaseChain", "SQLAgent"))

# Database selection
database_name = st.selectbox(
    "Choose the database", ("Crimes", "Happiness", "Hospitality")
)

# Query input
user_query = st.text_input("Enter your question about the data:")

# Run query on button click
if st.button("Run Query"):
    if user_query:
        try:
            # Process query and capture verbose output
            result, verbose_logs = process_query(user_query, model_name, database_name)
            st.write("Result:", result)

            # Display verbose logs
            st.write("Verbose Logs")
            if verbose_logs.strip():
                st.code(verbose_logs)
            else:
                st.write("No verbose logs captured.")
        except Exception as e:
            st.write("Error:", e)
    else:
        st.write("Please enter a question")
