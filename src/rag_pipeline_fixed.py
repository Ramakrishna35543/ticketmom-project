import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Check API Key
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY is missing")

try:
    # Load documents
    loader = TextLoader("company_docs.txt")
    docs = loader.load()

    # Split documents correctly
    splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    # Correct embedding model
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # Persistent vector DB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    # Stable LLM configuration
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0
    )

    # Better retrieval settings
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )

    # QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # Query
    result = qa_chain.invoke(
        {"query": "What is our refund policy?"}
    )

    print("Answer:")
    print(result["result"])

except Exception as e:
    print(f"Error: {e}")