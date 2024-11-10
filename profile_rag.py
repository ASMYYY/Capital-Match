import os
import json
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains import SequentialChain, LLMChain
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from prompts import prompt1, prompt2

os.environ["GROQ_API_KEY"] = "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"

class ProfileRAG:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=1,
            max_tokens=400,
            top_p=1
        )
        self.prompt1 = prompt1
        self.prompt2 = prompt2
        self.customer_dataset = json.load(open("data/customer_profile.json"))
        self.product_dataset = json.load(open("data/products.json"))
        self.embeddings_model_name = "BAAI/bge-small-en"
        self.documents = []

    def setup_chain(self):
        first_prompt = PromptTemplate(input_variables=["query"], template=self.prompt1)
        second_prompt = PromptTemplate(input_variables=["customer_analysis", "product_info"], template=self.prompt2)

        first_chain = LLMChain(llm=self.llm, prompt=first_prompt, output_key="customer_analysis", verbose=True)
        second_chain = LLMChain(llm=self.llm, prompt=second_prompt, output_key="final_recommendation", verbose=True)

        self.sequential_chain = SequentialChain(
            chains=[first_chain, second_chain],
            input_variables=["query", "product_info"],
            output_variables=["final_recommendation"]
        )

    def get_embeddings(self):
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.embeddings_model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        for customer in self.customer_dataset:
            self.documents.append(
                Document(page_content=json.dumps(customer, indent=4), metadata={"class": customer["CustomerID"]}))
        self.db = FAISS.from_documents(self.documents, self.embeddings)

    def generate_recommendation(self, customer_id: str):
        retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": 1})
        retrieved_documents = retriever.get_relevant_documents(customer_id)
        customer_info = "\n".join([doc.page_content for doc in retrieved_documents])

        product_info = "\n".join(
            [
                f"Name: {prod['name']}, Category: {prod['category']}, Features: {prod['features']}, Description: {prod['description']}"
                for prod in self.product_dataset]
        )

        result = self.sequential_chain({"query": customer_info, "product_info": product_info})

        return {"recommendation": result["final_recommendation"]}

# obj = ProfileRAG()
# obj.setup_chain()
# obj.get_embeddings()
# obj.generate_recommendation(customer_id="AlisonGaines78")
