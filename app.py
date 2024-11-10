import uvicorn
from fastapi import FastAPI
from payload import UserQuery, MailQuery
from profile_rag import ProfileRAG
from draft_mail import DraftMail

app = FastAPI()

reco_obj = ProfileRAG()
reco_obj.setup_chain()
reco_obj.get_embeddings()

mail_obj = DraftMail()
mail_obj.setup_chain()


@app.get('/')
def index():
    return {'message': 'Product recommendation for banking customers'}

@app.post('/product/recommend')
def recommendations(data: UserQuery):
    data = data.dict()
    candidate_id = data['candidate_id']
    result = reco_obj.generate_recommendation(customer_id=candidate_id)
    print("Recommendation -> ", result)
    return result

@app.post('/product/mail-content')
def send_mail(data: MailQuery):
    data = data.dict()
    recommendation = data['product_recommendation']
    result = mail_obj.get_content(recommendation)
    print("Mail Content -> ", result)
    return result

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)