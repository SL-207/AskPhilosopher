from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load documents
loader = TextLoader("philosophy_data.txt")
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# Use sentence-transformers for generating embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
# embeddings = embedding_model.embed_documents([chunk.page_content for chunk in chunks])

# Create a FAISS vector store from document embeddings
vectorstore = FAISS.from_documents(documents=chunks, embedding=embedding_model)

query = "What is the causal theory of knowledge?"
# docs = vectorstore.similarity_search(query, k=2)
# print(docs[0].page_content)