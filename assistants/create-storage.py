from dotenv import load_dotenv
load_dotenv()

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage




class AddingDataToGPT:

    def __init__(self):
        self.index = None
        self.persist_dir = "./storage/infra_ui"
        self.data_dir = "./data/infra_ui"
        self.build_storage()

    def build_storage(self):

        documents = SimpleDirectoryReader(self.data_dir).load_data()
        self.index = GPTVectorStoreIndex.from_documents(documents)
        self.index.storage_context.persist(self.persist_dir)

    def read_from_storage(self):
        storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
        self.index = load_index_from_storage(storage_context)


adding_data = AddingDataToGPT()
