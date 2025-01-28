import time, logging
import pandas as pd
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from data_ingestion.preprocessor import res

load_dotenv()

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")
        self.pc = Pinecone()
        self.index = None


    def initialize_index(self):
        """Initialize the Pinecone Index"""

        try:
            index_name = "research-assistant-agent-index"
            existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]

            if index_name not in existing_indexes:
                self.pc.create_index(
                    name=index_name,
                    dimension=1536,
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                    metric="cosine"
                )

            index = self.pc.Index(index_name)
            while not self.pc.describe_index(index_name).status['ready']:
                print("Pincone Index not ready yet, please wait a while...")
                time.sleep(1)
        
            self.index = index
        except Exception as e:
            logger.error(f"Failed to Initialize index: {e}")
            raise
        

    def _create_documents(self, df: pd.DataFrame):
       documents = [
            Document(
                page_content = row['chunk'],
                metadata = {
                    'arxiv_id': row["arxiv_id"],
                    'title': row["title"],
                    'chunk': row["chunk"],
                    "prev_chunk_id": row["prev_chunk_id"],
                    "next_chunk_id": row["next_chunk_id"]
                }
            )
        for _, row in df.iterrows()]
       return documents


    def populate_vector_store(self, df: pd.DataFrame):
        """Populate the Pinecone VectorStore from a DataFrame"""

        if self.index is None:
            raise ValueError("Pincone Index not initialized, call initialize_index first.")
        vector_store = PineconeVectorStore(self.index, embedding=self.embeddings)
        documents = self._create_documents(df)
        vector_store_ids = [row['id'] for _, row in df.iterrows()]
        print("* Created the Docs and Metadata, storing in Vector DB...")
        
        vector_store.add_documents(documents=documents, ids=vector_store_ids)
        print(f"* Successfully populated the vector store: \n {self.index.describe_index_stats()}")

