from libs.common import ChromaService
import pandas as pd
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import CharacterTextSplitter


class ExcelProcessorService:
    def __init__(self):
        self.vectorstore_service = ChromaService()

    def process(self, key: str):
        # First convert Excel to CSV
        file_path = f"data/{key}.xlsx"
        df = pd.read_excel(file_path)
        field_names = df.columns.tolist()
        csv_path = file_path.replace(".xlsx", ".csv")
        df.to_csv(csv_path, index=False, header=field_names, sep=";")

        # Use CSVLoader from langchain
        loader = CSVLoader(
            file_path=csv_path,
            csv_args={
                "delimiter": ";",
                "fieldnames": field_names,
            },
        )
        documents = loader.load()

        documents = ChromaService.documents_to_string_array(documents)
        # Add documents to ChromaDB
        self.vectorstore_service.add_documents(documents)
