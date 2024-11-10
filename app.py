import uvicorn
from fastapi import FastAPI
from payload import UserQuery
from profile_rag import ProfileRAG

app = FastAPI()

obj = ProfileRAG()
obj.setup_chain()
obj.get_embeddings()


@app.get('/')
def index():
    return {'message': 'Product recommendation for banking customers'}

@app.post('/product/recommend')
def recommendations(data: UserQuery):
    print('????',data)
    # data = data.dict()
    candidate_id = data['input']['candidate_id']

    result = obj.generate_recommendation(customer_id=candidate_id)

    return result


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)