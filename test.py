import requests

def test_reco():
    url = "http://127.0.0.1:8000/product/recommend"
    headers = {"Content-Type": "application/json"}
    data = {"candidate_id": "AlisonGaines78"}
    recommendation = requests.post(url, headers=headers, json=data)
    print(recommendation.status_code)
    result = recommendation.json().get('recommendation')
    print("Recommendation -> ", result)
    return result

def test_mail(recommendation):
    url = "http://127.0.0.1:8000/product/mail-content"
    headers = {"Content-Type": "application/json"}
    data = {"product_recommendation": recommendation}
    mail_content = requests.post(url, headers=headers, json=data)
    print(mail_content.status_code)
    result = mail_content.json().get('mail')
    print("mail_content -> ", result)
    return result

reco = test_reco()
test_mail(reco)

