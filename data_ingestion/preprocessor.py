import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from data_ingestion.extraction import ArxivExtraction


class Preprocessor:
    def __init__(self):
        pass

    
    def chunk_pdf(self, pdf_path):
        splitter = RecursiveCharacterTextSplitter(chunk_size = 512, chunk_overlap = 64)
        loader = PyPDFLoader(pdf_path)

        data = loader.load()
        chunks = splitter.split_documents(data)

        return chunks
    
    
    def create_chunks_df(self, df: pd.DataFrame):
        chunks_df = []

        for idx, row in df.iterrows():
            chunks = self.chunk_pdf(row['pdf_file_name'])
            
            for i, chunk in enumerate(chunks):
                prev_chunk = i - 1 if i != 0 else ''
                next_chunk = i + 1 if i < len(chunks) - 1 else ''

                chunks_df.append({
                    'id': f"{row['arxiv_id']}_{i}",
                    'title': row['title'],
                    'summary': row['summary'],
                    'authors': row['authors'],
                    'arxiv_id': row['arxiv_id'],
                    'url': row['url'],
                    'chunk': chunk.page_content,
                    'prev_chunk_id': f'{row['arxiv_id']}_{prev_chunk}',
                    'next_chunk_id': f'{row['arxiv_id']}_{next_chunk}'
                })
        
        return pd.DataFrame(chunks_df)



arxiv = ArxivExtraction(max_results=5)
df = arxiv.extract_from_arxiv()
new_df = arxiv.download_pdfs(df)
newobj = Preprocessor()

res = newobj.create_chunks_df(new_df)
print(res.head())
