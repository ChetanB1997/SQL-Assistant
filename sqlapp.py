import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import ChatOpenAI
from db import sql_database, connection
from dotenv import load_dotenv
import os
import pandas as pd  
import pandas.io.sql as sqlio
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sqlalchemy import inspect
load_dotenv()  #path to .env file

# Ensure OPENAI_API_KEY is set
if 'OPENAI_API_KEY' not in os.environ:
    st.error("Please set your OPENAI_API_KEY in the .env file")
    st.stop()

# Initialize LLM and toolkit
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
toolkit = SQLDatabaseToolkit(db=sql_database, llm=llm)

# Create SQL agent
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_executor_kwargs={"return_intermediate_steps": True}
)

# Streamlit app
st.title("SQL Database Query Assistant")

# User input
user_query = st.text_input("Enter your question about the database:")


def get_table_schemas():
    inspector = inspect(sql_database._engine)
    schemas = {}
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schemas[table_name] = [f"{col['name']} ({col['type']})" for col in columns]
    return schemas


# Create a prompt template
prompt_template = PromptTemplate(
    input_variables=["schema", "query"],
    template="""Given the following SQL table schemas:
{schema}

Generate a SQL query to answer the following question:
{query}

Important guidelines:
1. Use appropriate JOINs between tables when necessary to retrieve the required information.
2. Use table aliases to avoid ambiguity when joining tables.
3. Make sure to use the correct join conditions based on the relationships between tables.
4. If aggregations are needed, use GROUP BY and appropriate aggregate functions.
5. Use subqueries or CTEs if they help in making the query more readable or efficient.

Return only the SQL query, without any explanations."""
)

# Create an LLM chain
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

def process_query(query):
    with st.spinner("Generating SQL query..."):
        schemas = get_table_schemas()
        schema_str = "\n".join([f"{table}: {', '.join(columns)}" for table, columns in schemas.items()])
        # import pdb;pdb.set_trace()
        result = llm_chain.run(schema=schema_str, query=query)
    # import pdb;pdb.set_trace()
    st.subheader("Generated SQL Query:")
    st.code(result, language="sql")
    
    with st.spinner("Executing query..."):
        try:
            
            cleaned_query = result.strip().removeprefix("```sql\n").removesuffix("```")
            query_result=sqlio.read_sql_query(cleaned_query, connection)
            st.subheader("Query Result:")
            
            st.dataframe(query_result)
        except Exception as e:
            st.error(f"Error executing SQL query: {e}")


if st.button("Submit"):
    if user_query:
        process_query(user_query)
    else:
        st.warning("Please enter a query.")

# Update the example query section
if st.button("Run Example Query"):
    example_query = "List the top 5 customers by total order amount"
    st.write(f"Running example query: {example_query}")
    process_query(example_query)