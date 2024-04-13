from ..fixtures import app, client, agency
from copy import copy

def test_getting_all_subs(client,agency):
    subs = agency.get_subscribers()
    response = client.get("/subscriber/")
    
    response_body = response.get_json()
    

    assert response.status_code == 200
    assert len(response_body) == len(subs)
    
def test_adding_sub(client,agency):
    before = len(agency.get_subscribers())
    
    response = client.post("/subscriber/",json = {"name": "Indigo","address": "Igner Street"})
    
    
    response_body = response.get_json()
    sub = agency.get_subscriber(subscriber_id=response_body["subscriber_id"])
    
    assert len(agency.get_subscribers()) == before + 1
    assert response.status_code == 200
    assert sub.subscriber_id == response_body['subscriber_id']
    assert sub.name == response_body["name"]
    assert sub.address == response_body['address']
    assert sub.name == "Indigo"
    assert sub.address == "Igner Street"


def test_getting_sub_by_id(client,agency):
    
    sub = agency.get_subscriber(1)
    

    response = client.get("/subscriber/1")
    response_body = response.get_json()

    
    assert response.status_code == 200
    assert sub.subscriber_id == response_body["subscriber_id"]
    assert sub.name == response_body["name"]
    assert sub.address == response_body["address"]
    assert sub.newspapers[0].paper_id == response_body["newspapers"][0]["paper_id"]
    assert sub.newspapers[0].name == response_body["newspapers"][0]["name"]
    assert sub.newspapers[0].frequency == response_body["newspapers"][0]["frequency"]
    assert sub.newspapers[0].price == response_body["newspapers"][0]["price"]


    

def test_chaning_sub(client,agency):
    old_sub = copy(agency.get_subscriber(subscriber_id=21))

    response = client.post("/subscriber/21",json = {"name":"Jiraya","address":"Kanoha"})
    upd_sub = agency.get_subscriber(subscriber_id=21)

    assert response.status_code == 200
    assert response.get_json() == True
    assert old_sub.subscriber_id == upd_sub.subscriber_id
    assert old_sub.name != upd_sub.name
    assert old_sub.address != upd_sub.name
    assert upd_sub.name == "Jiraya"
    assert upd_sub.address == "Kanoha"
    
    response2 = client.post("/subscriber/7777",json = {"name":"aloha","address":"Osaka"}) #testing with wrong id
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"

    


def test_removing_sub(client,agency):
    before = len(agency.get_subscribers())
    sub = agency.get_subscriber(subscriber_id=41)
    
    assert sub in agency.get_subscribers()

    response = client.delete("/subscriber/41")
    
    assert response.status_code == 200
    assert response.get_json() == True
    assert sub not in agency.get_subscribers()
    assert len(agency.get_subscribers()) == before-1
    assert sub.newspapers == []


    response2 = client.delete("/subscriber/41") #testing with wrong id 
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"


def test_subscriber_subscribe(client,agency):
    paper = agency.get_newspaper(paper_id=195)
    before = len(paper.subscribers)
    sub = agency.get_subscriber(subscriber_id=41)

    assert sub not in paper.subscribers
    assert paper not in sub.newspapers
    

    response = client.post("/subscriber/41/subscribe",json ={'paper_id': 195})
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert response_body == True
    assert len(paper.subscribers) == before+1
    assert sub in paper.subscribers
    assert paper in sub.newspapers
    

    response2 = client.post("/subscriber/421/subscribe", json ={'paper_id': 195}) #testing with wrong subscriber_id 
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"

    response3 = client.post("/subscriber/41/subscribe", json ={'paper_id': 1935}) #testing with paper_id
    assert response3.status_code == 422
    assert response3.get_json()["message"] == "{'error': 'id is not correct'}"


def test_sub_stats(client,agency):
    stats = agency.get_subsriber_stats(subcriber_id=41) #this method is already tested in test_agency so it works for sure
    
    response = client.get("/subscriber/41/stats")
    response_body = response.get_json()
    assert response.status_code == 200
    assert stats == response_body
    


    response2 = client.get("/subscriber/411/stats")
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"


def test_get_missing_issues(client,agency):
    missed_iss = agency.get_missing_issues(subscriber_id=21)
    agency.release_issue(paper_id=115,issue_id=1)
    req1 = client.get('/subscriber/21/missingissues')
    ans1 = req1.get_json()
    
    assert req1.status_code == 200
    assert ans1 == missed_iss #because subscriber is not subscribed to our newspaper he has no missed issues
    assert ans1 == {"issues":[]}
    

    agency.subscribe(paper_id=115,subscriber_id=21)
    missed_iss = agency.get_missing_issues(subscriber_id=21)

    
    req2 = client.get('/subscriber/21/missingissues')
    ans2 = req2.get_json()
    assert req2.status_code == 200
    assert ans2 == missed_iss #because subscriber did not receive any issue he has to add issue 1 from paper_id = 115 to missed issues 
    

    agency.deliver_issue(paper_id=115,issue_id=1,subscriber_id=21)
    
    req3 = client.get('/subscriber/21/missingissues')
    ans3 = req3.get_json()
    assert req3.status_code == 200
    assert ans3 != missed_iss #because subscriber  received an issue it is not equal to missed issues that we defined before
    assert ans3 == {"issues":[]}
    
    missed_iss = agency.get_missing_issues(subscriber_id=21)
    assert ans3 == missed_iss


    req4 = client.get('/subscriber/211/missingissues') #testing wrong id
    assert req4.status_code == 422
    assert req4.get_json()["message"] == "{'error': 'id is not correct'}"

