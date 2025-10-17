import os
import gradio as gr
from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.metanames import GenChatParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods, EmbeddingTypes
from langchain_ibm import WatsonxEmbeddings, WatsonxLLM
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Configuaration Credentials

load_dotenv()

try:
    APIKEY = os.getenv("WATSONX_APIKEY")
    PROJECT_ID  = os.getenv("WATSONX_PROJECT_ID")
    URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

    print("WATSONX_APIKEY found?", bool(APIKEY))
    print("WATSONX_URL:", URL)
    print("WATSONX_PROJECT_ID:", PROJECT_ID)

    if not APIKEY or not PROJECT_ID:
        raise ValueError("API key or Project ID not found in environment variables.")

    creds = {
        "url": URL
    }    

    print("Credentials loaded successfully.")
except Exception as e:
    print(f"Error loading credentials: {e}")
    exit()

# Configuration Models (LLM and Embedding)

embeddings = WatsonxEmbeddings(
    model_id=EmbeddingTypes.IBM_SLATE_30M_ENG.value,
    url=URL,
    project_id=PROJECT_ID,
    apikey=APIKEY
)

#Parameters for LLM
try:
    params = {
        GenParams.MAX_NEW_TOKENS: 512,
        GenParams.MIN_NEW_TOKENS:3,
        GenParams.TEMPERATURE: 0.1,
        GenParams.REPETITION_PENALTY: 1.05,
        "decoding_method": "greedy",
    }
except Exception:
    params = {
        "decoding_method": "greedy",
        "min_new_tokens": 3,
        "max_new_tokens": 512,
        "temperature": 0.1,
        "repetition_penalty": 1.05,
    }

# Initialize LLM Granite model
watsonx_granite = WatsonxLLM(
    model_id="ibm/granite-3-2-8b-instruct",
    params=params,
    project_id=PROJECT_ID,
)
print("LLM model initialized successfully.")

# Load and process the PDF document in the fist one time
pdf_filename = 'ibm-annual-report-2024.pdf'
persist_directory = 'chroma_db_ibm'

if not os.path.exists(persist_directory):
    print(f"Creating vector store from PDF document...{pdf_filename} waiting...")
    
    loader = PyPDFLoader(pdf_filename)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    vectordb = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory=persist_directory
    )
    print("Vector store created and persisted successfully.")
else:
    print("Loading existing vector store...")
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

print("Vector store ready to use")

#  Create a chain RAG and the function to interface
qa_chain = RetrievalQA.from_chain_type(
    llm=watsonx_granite,
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
    return_source_documents=True
)
print("RAG chain ready.")

#Function to interface with Gradio
def ask_watsonx_analyst(question):
    print(f"Received question: {question}")
    try:
        result = qa_chain.invoke(question)

        # Format the response to include sources
        answer = result['result']
        source_docs = result['source_documents']

        # to get the sources from the documents
        sources_text = "\n\n-- Sources Consulting --\n"
        for doc in source_docs:
            sources_text += f"excerpt from the page {doc.metadata.get('page', 'N/A')}:\n"
            sources_text += f"{doc.page_content[:300]}...\n\n"
        
        return answer + sources_text
    except Exception as e:
        print(f"Error during QA chain invocation: {e}")
        return f"Sorry, there was an error processing your request. {e}"
    
# Gradio Interface
print("Launching Gradio interface...")

iface = gr.Interface(
    fn=ask_watsonx_analyst,
    inputs=gr.Textbox(lines=2, placeholder="Ask a question about IBM's 2024 Annual Report..."),
    outputs="text",
    title="Watsonx Analyst - IBM Annual Report 2024",
    description="Ask questions about IBM's 2024 Annual Report using IBM Watsonx AI models.",
    theme="compact"
)

iface.launch(share=True)