**Q/A with Graph Database Using Streamlit**
This Streamlit application allows users to upload files (TXT or CSV), convert the data into a Neo4j graph database, and perform Q&A using either the OpenAI or Groq language models (LLMs). It provides features to manage the graph database, view its schema, and interact with the data using natural language queries.

**Features**
Neo4j Integration:

Upload TXT or CSV files and convert their content into a graph database.
View the graph schema in real-time.
Delete all nodes and relationships from the database with a single click.
LLM Integration:

Choose between OpenAI (GPT-4) and Groq LLMs for graph-related Q&A.
Dynamically initialize the selected LLM using user-provided API keys.
File Support:

Upload plain text files or CSV files.
Automatically parse and process files into graph-compatible formats.
Q&A Functionality:

Ask natural language questions and retrieve answers based on graph data.
Technologies Used
**Frontend: Streamlit
Graph Database: Neo4j
LLMs: OpenAI GPT-4, Groq (gemma2-9b-it)
LangChain Modules:
Neo4jGraph: For Neo4j integration.
LLMGraphTransformer: To convert file content into graph documents.
GraphCypherQAChain: For Cypher-based Q&A using LLMs.**
