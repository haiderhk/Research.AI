import pandas as pd
import requests, json, os
import xml.etree.ElementTree as ET

ARXIV_NAMESPACE = '{http://www.w3.org/2005/Atom}'
FILE_PATH = "arxiv_dataset.json"
DOWNLOAD_FOLDER = "pdf_files/"

class ArxivExtraction:
    def __init__(self, max_results):
        self.max_results = max_results
        self.file_path = FILE_PATH
        self.pdfs_folder = DOWNLOAD_FOLDER


    def extract_from_arxiv(self, search_query="cat:cs.AI"):
        url = f'http://export.arxiv.org/api/query?search_query={search_query}&max_results={self.max_results}'
        response = requests.get(url)
        root = ET.fromstring(response.content)

        papers = []

        for entry in root.findall(f"{ARXIV_NAMESPACE}entry"):
            title = entry.find(f'{ARXIV_NAMESPACE}title').text.strip()
            summary = entry.find(f'{ARXIV_NAMESPACE}summary').text.strip()

            author_elements = entry.findall(f'{ARXIV_NAMESPACE}author')
            authors = [author.find(f'{ARXIV_NAMESPACE}name').text for author in author_elements]

            paper_url = entry.find(f'{ARXIV_NAMESPACE}id').text
            arxiv_id = paper_url.split('/')[-1]

            pdf_link = next((link.attrib['href'] for link in entry.findall(f'{ARXIV_NAMESPACE}link') 
                            if link.attrib.get('title') == 'pdf'), None)

            papers.append({
                'title': title,
                'summary': summary,
                'authors': authors,
                'arxiv_id': arxiv_id,
                'url': paper_url,
                'pdf_link': pdf_link
            })

        df = pd.DataFrame(papers)

        with open(self.file_path, 'w') as file:
            json.dump(papers, file, ensure_ascii=False, indent=4)
            print(f"* Data saved to {self.file_path}")

        return df


    def download_pdfs(self, df: pd.DataFrame):
        if not os.path.exists(self.pdfs_folder):
            os.makedirs(self.pdfs_folder)
            print("* Created the download directory.")

        pdf_file_names = []

        for index, row in df.iterrows():
            pdf_link = row['pdf_link']
            try:
                response = requests.get(pdf_link)
                response.raise_for_status()
                unqiue_name = pdf_link.split('/')[-1] + ".pdf"
                file_name = os.path.join(self.pdfs_folder, unqiue_name)
                pdf_file_names.append(file_name)

                with open(file_name, "wb") as file:
                    file.write(response.content)

            except Exception as e:
                print(f"Failed to download pdf: {e}")
                pdf_file_names.append(None)
        
        df['pdf_file_name'] = pdf_file_names
        return df
            

arxiv = ArxivExtraction(max_results=5)
df = arxiv.extract_from_arxiv()
new_df = arxiv.download_pdfs(df)
print(new_df.head())
