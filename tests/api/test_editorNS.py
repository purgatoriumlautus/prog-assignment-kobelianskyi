#TODO: ALL TESTS FOR API'S HERE
from ..fixtures import app, client, agency
from copy import copy


def test_getting_all_editors(client,agency):
    response = client.get("/editor/")
    assert response.status_code == 200

    editors = response.get_json()
    assert len(editors) == len(agency.editors)


def test_post_an_editor(client,agency):
    before = len(agency.editors)
    response = client.post("/editor/",json = {
                                    "name": "Alex",
                                    "address": "Khmelnitskyi street"})
    
    created_editor = response.get_json()
    
    assert response.status_code == 200
    assert len(agency.editors) == before+1
    assert agency.get_editor(editor_id=created_editor["editor_id"]).name == "Alex"
    assert agency.get_editor(editor_id=created_editor["editor_id"]).address == "Khmelnitskyi street"


def test_get_editor_by_id(client,agency):
    orig_editor = agency.get_editor(editor_id=33)
    response = client.get("/editor/33")
    assert response.status_code == 200
    editor = response.get_json()
    assert editor["editor_id"] == orig_editor.editor_id
    assert editor["name"] == orig_editor.name
    assert editor["address"] == orig_editor.address
    

    response2 = client.get("/editor/77") #testing with wrong id
    
    
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"


def test_changing_editor(client,agency):
    orig_editor = agency.get_editor(editor_id=22)
    
    assert orig_editor.name != "Mihail"
    assert orig_editor.address != "Paris"
    
    response = client.post("/editor/22",json = {"name":"Mihail","address":"Paris"})
    changed_editor = response.get_json()
    
    
    assert response.status_code == 200
    assert orig_editor.editor_id == changed_editor["editor_id"]
    assert orig_editor.name == changed_editor["name"]
    assert orig_editor.address == changed_editor["address"]
    assert orig_editor.name == "Mihail"
    assert orig_editor.address == "Paris"

    response2 = client.post("/editor/78",json = {"name":"Ivan","address":"Odessa"})
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"


def test_removing_editor(client,agency):
    
    orig_editor = agency.get_editor(editor_id=22)
    issue = orig_editor.issues[0]
    newspaper = issue.newspaper

    assert issue.editor == orig_editor
    assert orig_editor in agency.editors
    assert orig_editor in newspaper.editors
    response = client.delete("/editor/22")
    response_body = response.get_json()
    

    assert response.status_code == 200
    assert response_body == f"Editor {orig_editor.name} with id {orig_editor.editor_id} was successfully fired!"
    
    assert orig_editor not in agency.editors
    assert issue.editor != orig_editor
    assert orig_editor not in newspaper.editors
    
    response2 = client.delete("/editor/228") #is not found now as we deleted editor with this id
    assert response2.get_json() == "Editor wasn't found"

def test_getting_editor_issues(client,agency):
    orig_editor = agency.get_editor(editor_id=11)
    orig_issue = agency.get_issue(paper_id=115,issue_id=1)
    issues = orig_editor.get_issues()
    
    assert orig_issue in issues
    
    response = client.get("editor/11/issues")
    response_issues = response.get_json()
   
    
    assert response.status_code == 200 
    assert len(response_issues) == len(issues)

    assert response_issues[0]["issue_id"] == issues[0].issue_id
    assert response_issues[0]["releasedate"] == issues[0].releasedate
    assert response_issues[0]["released"] == issues[0].released
    assert response_issues[0]["pages"] == issues[0].pages
    assert response_issues[0]["newspaper"]["paper_id"] == issues[0].newspaper.paper_id
    assert response_issues[0]["newspaper"]["name"] == issues[0].newspaper.name
    assert response_issues[0]["newspaper"]["frequency"] == issues[0].newspaper.frequency
    assert response_issues[0]["newspaper"]["price"] == issues[0].newspaper.price

    response2 = client.get("editor/1111/issues") #testing wrong id
    assert response2.status_code == 422
    assert response2.get_json()["message"] == "{'error': 'id is not correct'}"


