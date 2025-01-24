import streamlit as st
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import GraphCypherQAChain
from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
import pandas as pd

st.title("Q/A with Graph Database")
st.subheader("Upload a txt file, Ask questions from it and get answer from the Neo4j auradb graph database")

# Sidebar for inputs
with st.sidebar:
    st.title("Neo4j Configuration")
    st.write("get your neo4j credentials from https://neo4j.com/product/auradb/")
    NEO4J_URI = st.text_input("NEO4J_URI", type="password")
    NEO4J_USERNAME = st.text_input("NEO4J_USERNAME", type="password")
    NEO4J_PASSWORD = st.text_input("NEO4J_PASSWORD", type="password")
    
    st.title("LLM Configuration")
    st.write("this service use gpt-4-turbo for openai https://platform.openai.com/ and gemma-2b-it for groq https://groq.com/ ")
    llm_choice = st.selectbox("Choose LLM", ["OpenAI", "Groq"])  # Dropdown for LLM selection
    
    if llm_choice == "OpenAI":
        openai_api_key = st.text_input("OpenAI API Key", type="password")
    elif llm_choice == "Groq":
        groq_api_key = st.text_input("Groq API Key", type="password")
    st.write("Download the sample txt file form https://github.com/Lovi07/Q-A-from-graphdb/blob/main/abc.txt")

# Initialize Neo4j and LLM
graph, llm = None, None

# Neo4j initialization
if NEO4J_URI and NEO4J_USERNAME and NEO4J_PASSWORD:
    try:
        graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
        st.success("Connected to Neo4j!")
    except Exception as e:
        st.error(f"Failed to connect to Neo4j: {e}")

# LLM initialization based on user choice
if llm_choice == "OpenAI" and openai_api_key:
    try:
        llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4-turbo", temperature=0)
        st.success("OpenAI LLM initialized!")
    except Exception as e:
        st.error(f"Failed to initialize OpenAI: {e}")
elif llm_choice == "Groq" and groq_api_key:
    try:
        llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)
        st.success("Groq LLM initialized!")
    except Exception as e:
        st.error(f"Failed to initialize Groq: {e}")

# File upload
upload_file = st.file_uploader("Upload a file", type=["txt", "csv"])
documents = []

if upload_file:
    try:
        file_type = upload_file.name.split(".")[-1]
        if file_type == "txt":
            text = upload_file.read().decode("utf-8")
            documents = [Document(page_content=text)]
            st.success("Text file uploaded successfully!")
        elif file_type == "csv":
            # Process CSV file into documents
            df = pd.read_csv(upload_file)
            st.write("CSV Content:")
            st.dataframe(df)
            csv_content = df.to_csv(index=False)  # Convert DataFrame to CSV format as a string
            document = Document(page_content=csv_content)
            documents = [document]

            st.success("CSV file content prepared for graph conversion!")
    except Exception as e:
        st.error(f"Failed to process the uploaded file: {e}")

# Show graph schema
if st.button("Show Graph Schema") and graph and llm:
    try:
        llm_transformer = LLMGraphTransformer(llm=llm)
        graph_documents = llm_transformer.convert_to_graph_documents(documents)
        graph.add_graph_documents(graph_documents)
        graph.refresh_schema()
        st.success(graph.schema)
    except Exception as e:
        st.error(f"Failed to show graph schema: {e}")

# Delete all data
if st.sidebar.button("Delete graph data"):
    try:
        if graph:
            # Delete all nodes and relationships
            delete_query = "MATCH (n) DETACH DELETE n"
            graph.query(delete_query)
            graph.refresh_schema()
            st.success("All nodes and relationships deleted successfully!")
        else:
            st.error("No active graph connection to delete data.")
    except Exception as e:
        st.error(f"Failed to delete data: {e}")

# Q&A functionality
question = st.text_input("Ask a question")

if st.button("Get Answer") and question and graph and llm:
    try:
        chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True, allow_dangerous_requests=True)
        response = chain.invoke({"query": question})
        st.success(response)
    except Exception as e:
        st.error(f"Failed to get an answer: {e}")
