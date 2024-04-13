# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency
from copy import copy

def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")   # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)

    # act
    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200
    # verify

    assert len(agency.newspapers) == paper_count_before + 1
    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14




def test_get_paper_byid(client,agency):
    response = client.get("/newspaper/100")
    assert response.status_code == 200
    parsed = response.get_json()
    paper_response = parsed["newspaper"]
    assert paper_response["paper_id"] == 100
    assert paper_response['name'] == "The New York Times"
    assert paper_response['frequency'] == 7
    assert paper_response['price'] == 13.14
    

def test_get_paper_by_wrong_id(client):
    response = client.get("/newspaper/8687")
    assert response.status_code == 422
    assert response.get_json()["message"] == "{'error': 'id is not correct'}"


def test_changing_paper(client,agency):
    paper_before =  copy(agency.get_newspaper(paper_id=125))
    response = client.post("/newspaper/125",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    
    assert response.status_code == 200
    upd_paper = response.get_json()["newspaper"]
    
    assert upd_paper["name"] == "Simpsons Comic"
    assert upd_paper['frequency'] == 7
    assert upd_paper["price"] == 3.14
    
    upd_from_agency = agency.get_newspaper(paper_id=125)
   
    assert paper_before.name != upd_from_agency.name
    assert paper_before.frequency != upd_from_agency.frequency
    assert paper_before.price != upd_from_agency.price
    
    response2 = client.post("/newspaper/1266",  # WRONG ID
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"



def test_removing_paper(client,agency):
    response = client.delete("/newspaper/115")  #
    assert response.status_code == 200
    assert response.get_json() == "Newspaper with ID 115 was removed"
    
    response2 = client.delete("/newspaper/125")# <-- will return 422 - id not found as we already deleted the paper with this id
    response2.status_code == 422
    response2.get_json() == "{'error': 'id is not correct'}"
   


def test_creating_issue(client,agency):
    response = client.post("/newspaper/195/issue",
                           json={
                                "release_date": "today",
                                "pages": 12
                                 }     # <-- note the slash at the end!
    )
    
    assert response.status_code == 200
    assert response.get_json() == "Issue number - 1 has been added to Ukraine newspaper"
    issue = agency.get_issue(paper_id=195,issue_id=1)
    assert issue.releasedate == "today"
    assert issue.pages == 12
    assert issue.newspaper == agency.get_newspaper(paper_id=195)

    response2 = client.post("/newspaper/1665/issue",
                           json={
                                "release_date": "today",
                                "pages": 12
                                 }     # <-- note the slash at the end!
    )
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"


def test_getting_paper_issues(client,agency):
    adding_second_issue = client.post("/newspaper/195/issue",
                           json={
                                "release_date": "12.12.2024",
                                "pages": 1
                                 }     # <-- note the slash at the end!
    )
    assert adding_second_issue.status_code == 200

    response = client.get("/newspaper/195/issue")

    
    assert response.status_code == 200
    issue = response.get_json()
    
    assert issue[0]["issue_id"] == 1
    assert issue[0]["releasedate"] == "today"
    assert issue[0]["pages"] == 12
    assert issue[0]["released"] == False
    
    assert issue[1]["issue_id"] == 2
    assert issue[1]["releasedate"] == "12.12.2024"
    assert issue[1]["pages"] == 1
    assert issue[1]["released"] == False

    response2 = client.get("/newspaper/29594/issue")
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"
    

def test_getting_issue_byid(client,agency):
    response = client.get("/newspaper/195/issue/1")
    assert response.status_code == 200
    issue = response.get_json()

    assert issue["issue_id"] == 1
    assert issue["releasedate"] == "today"
    assert issue["pages"] == 12
    assert issue["released"] == False

    response2 = client.get("/newspaper/195/issue/2")
    assert response2.status_code == 200
    issue = response2.get_json()

    assert issue["issue_id"] == 2
    assert issue["releasedate"] == "12.12.2024"
    assert issue["pages"] == 1
    assert issue["released"] == False

    response3 = client.get("/newspaper/14242/issue/1")
    assert response3.status_code == 422
    assert response3.get_json()["message"] == "{'error': 'id is not correct'}"

    response4 = client.get("/newspaper/195/issue/4")
    assert response4.status_code == 422
    assert response4.get_json()["message"] == "{'error': 'id is not correct'}"



def test_releasing_issue(client,agency):
    assert not agency.get_issue(paper_id=195,issue_id=1).released
    response = client.post("/newspaper/195/issue/1/release")
    assert response.status_code == 200
    assert response.get_json() == True
    assert agency.get_issue(paper_id=195,issue_id=1).released 


    response2 = client.post("/newspaper/195/issue/12/release")    
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"

    response3 = client.post("/newspaper/19555/issue/1/release")    
    assert response3.status_code == 422
    assert response3.get_json()["message"] == "{'error': 'id is not correct'}"


def test_deliver_issue(client,agency):

    subscriber = agency.get_subscriber(subscriber_id=1)
    paper = agency.get_newspaper(paper_id=195)
    assert len(subscriber.received_issues)==0
    
    
    response = client.post("/newspaper/195/issue/1/deliver",json={"subscriber_id": 1}) #trying to send to unsubscribed
    pars1 = response.get_json()
    assert pars1 == f"Subscriber {subscriber.name} id -{subscriber.subscriber_id} is not subscribed to {paper.name} id{paper.paper_id}"
    
    agency.subscribe(paper_id=195,subscriber_id=1)
    
    response2 = client.post("/newspaper/195/issue/1/deliver",json={"subscriber_id": 1}) #successfull send
    pars2 = response2.get_json()
    assert pars2 == f"Issue was delivered to subscriber {subscriber.name} id -{subscriber.subscriber_id}"

    response3 = client.post("/newspaper/195/issue/2/deliver",json={"subscriber_id": 1}) #trying to send unreleased issue
    pars3 = response3.get_json()
    assert pars3 == f"Issue id 2 from {paper.name} is not released yet"

    response4 = client.post("/newspaper/195/issue/1/deliver",json={"subscriber_id": 1}) #trying to send issue for 2nd time
    pars4 = response4.get_json()
    assert pars4 == f"Issue was already delivered to subscriber {subscriber.name} id -{subscriber.subscriber_id}"

    response5 = client.post("/newspaper/1955/issue/1/deliver",json={"subscriber_id": 1}) #testing wrong paper id
    assert response5.get_json() == "Paper or Issue or Subscriber was not found please check the ID's!"

    response6 = client.post("/newspaper/195/issue/12/deliver",json={"subscriber_id": 1}) #testing wrong issue_id
    assert response6.get_json() == "Paper or Issue or Subscriber was not found please check the ID's!"

    response7 = client.post("/newspaper/195/issue/12/deliver",json={"subscriber_id": 890}) #testing wrong subscriber id
    assert response7.get_json() == "Paper or Issue or Subscriber was not found please check the ID's!"


def test_editor_for_issue(client,agency):
    issue = agency.get_issue(paper_id=195,issue_id=1)
    editor = agency.get_editor(editor_id=11)
    paper = agency.get_newspaper(paper_id=195)
    assert not hasattr(issue,"editor")
    assert editor not in paper.editors
    assert issue not in editor.issues
    assert paper not in editor.newspapers
    
    response = client.post("/newspaper/195/issue/1/editor",json={'editor_id':editor.editor_id})
    pars = response.get_json()
    assert response.status_code == 200
    
    assert pars["issue_id"] == 1
    assert pars["releasedate"] == "today"
    assert pars["pages"] == 12
    assert pars["released"] == True
    assert pars["editor"]['editor_id']== editor.editor_id
    assert pars["editor"]["name"] == editor.name

    assert editor in paper.editors
    assert issue in editor.issues
    assert paper in editor.newspapers
    assert hasattr(issue,"editor")

    response2 = client.post("/newspaper/1955/issue/1/editor",json={'editor_id':editor.editor_id}) # testing wrong paper id
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"

    response3 = client.post("/newspaper/195/issue/24/editor",json={'editor_id':editor.editor_id}) #testing wrong issue id
    assert response3.status_code == 422
    assert response3.get_json()["message"] == "{'error': 'id is not correct'}"

    response4 = client.post("/newspaper/195/issue/1/editor",json={'editor_id':editor.editor_id+24}) # testing wrong editor_id
    assert response4.status_code == 422
    assert response4.get_json()["message"] == "{'error': 'id is not correct'}"


def test_paper_stats(client,agency):
    paper = agency.get_newspaper(paper_id=195)
    stats = paper.get_stats()
    response = client.get("/newspaper/195/stats")
    pars = response.get_json()
    assert pars["paper_id"] == stats["paper_id"]
    assert pars["name"] == stats["name"]
    assert pars["frequency"] == stats["frequency"]
    assert pars['subscriber_amount'] == stats["subscriber_amount"]
    assert pars['montly_revenue'] == stats['montly_revenue']
    assert pars['annual_revenue'] == stats["annual_revenue"]
   
    response2 = client.get("/newspaper/19555/stats") #testing wrong id
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"

    
    
    



    # stats = {
    #         "paper_id":self.paper_id,
    #         "name":self.name,
    #         "price":self.price,
    #         "frequency":self.frequency,
    #         "subscriber_amount":self.subscriber_amount,
    #         "montly_revenue":self.subscriber_amount*self.price,
    #         "annual_revenue":self.price*self.subscriber_amount*12
    #         }
    #   