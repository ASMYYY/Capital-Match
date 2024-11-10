import os
import json
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain, LLMChain

from prompts import mail_prompt, sample_reco


os.environ["GROQ_API_KEY"] = "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"

class DraftMail:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=1,
            max_tokens=400,
        )
        self.prompt = mail_prompt
        self.customer_dataset = json.load(open("data/customer_profile.json"))
        self.product_dataset = json.load(open("data/products.json"))

    def setup_chain(self):
        prompt = PromptTemplate(input_variables=["product_recommendation"], template=self.prompt)
        self.llmchain = LLMChain(llm=self.llm, prompt=prompt, output_key="mail", verbose=True)


    def get_content(self, recommendation: str):
        email = "xyz@dfgh.com"
        product_recommendation = recommendation
        result = self.llmchain({"product_recommendation": product_recommendation})
        return {"mail": result["mail"]}


# obj = DraftMail()
# obj.setup_chain()
# mail_content = obj.get_content(sample_reco)
# print(mail_content)