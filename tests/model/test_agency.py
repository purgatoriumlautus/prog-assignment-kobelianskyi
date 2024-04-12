import pytest
from src.model.agency import Agency
from src.model.newspaper import Newspaper
from src.model.issue import Issue
from src.model.editor import Editor
from src.model.subscriber import Subscriber
from ..fixtures import app, client, agency


def test_add_newspaper(agency: Agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1

@pytest.mark.xfail(raises=ValueError)
def test_add_newspaper_same_id_should_raise_error(agency):
   
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)

    # first adding of newspaper should be okay
    agency.add_newspaper(new_paper)
    
    
    new_paper2 = Newspaper(paper_id=999,
                          name="Superman Comic",
                          frequency=7,
                          price=13.14)
    agency.add_newspaper(new_paper2)
    

       



def test_if_all_newspapers(agency: Agency):

    assert agency.newspapers == agency.all_newspapers()

def test_getting_paper_by_id(agency: Agency):
    new_paper = Newspaper(paper_id=865,
                          name="Marvel",
                          frequency=4,
                          price=3)
    agency.add_newspaper(new_paper)
    
    assert agency.get_newspaper(865) == new_paper


def test_removing_NS(agency: Agency):
    new_paper = Newspaper(paper_id=11,
                          name="Laslo",
                          frequency=6,
                          price=2)
    agency.add_newspaper(new_paper)
    agency.remove_newspaper(new_paper)
    assert new_paper not in agency.all_newspapers()
    assert agency.get_newspaper(11) == False


def test_getting_wrong_id(agency: Agency):
    new_paper = Newspaper(paper_id=911,
                          name="Persona-X",
                          frequency=1,
                          price=12)
    agency.add_newspaper(new_paper)
    agency.remove_newspaper(new_paper) #SO WE DON'T HAVE ANY NEWSPAPER WITH ID 911 FOR SURE
    assert agency.get_newspaper(911) == False




def test_changing_newspaper(agency: Agency):
    old_paper = Newspaper(paper_id=776,
                          name="Learn English",
                          frequency=15,
                          price=77)
    
    agency.add_newspaper(old_paper)
    new_paper = Newspaper(paper_id=776, #hass to be with the same ID
                          name="Vogue",
                          frequency=4,
                          price=5)
    
    upd_paper = agency.update_newspaper(new_paper) #update_newspaper returns an updated paper

    assert agency.get_newspaper(776) == upd_paper



def test_wrongid_changing_newspaper(agency: Agency):
    old_paper = Newspaper(paper_id=899,
                          name="ChinaTownNews",
                          frequency=5,
                          price=19)
    
    agency.add_newspaper(old_paper)
    new_paper = Newspaper(paper_id=898, #has to be with the same ID but here we test for the wrong one
                          name="Vogue",
                          frequency=2,
                          price=8)
    
    upd_paper = agency.update_newspaper(new_paper) #update_newspaper returns Falsewhen paper id is not found
    
    assert upd_paper == False

    #NOW WE HAVE TO ASSERT THAT THE OLD PAPER DID NOT CHANGE
    assert old_paper.paper_id == agency.get_newspaper(899).paper_id
    assert old_paper.name == agency.get_newspaper(899).name
    assert old_paper.frequency == agency.get_newspaper(899).frequency
    assert old_paper.price == agency.get_newspaper(899).price
# 



def test_adding_an_issue(agency: Agency):
    paper = agency.get_newspaper(100)
    before = len(paper.issues) #already exists an has only 1 issue
    issue1 = Issue(releasedate="02.03.2017",
                        pages=2,
                            newspaper=paper)
    agency.create_issue(paper_id=paper.paper_id,issue=issue1)
    assert len(paper.issues) == before+1
    assert issue1 in paper.issues


def test_adding_an_issue_to_wrong_paperid(agency: Agency):
    
    issue1 = Issue(releasedate="22.06.2012",
                        pages=4)
    assert agency.create_issue(paper_id=1439459,issue= issue1) == False #Should return false if paper was not found


def test_getting_all_paper_issues_and_by_id_and_wrong_id(agency: Agency):
    paper = Newspaper(paper_id=555,
                          name="Air Japan",
                          frequency=3,
                          price=150)
    issue1 = Issue(releasedate="4.12.2024",pages=22,newspaper=paper)
    issue2 = Issue(releasedate="02.02.2001",pages=11,newspaper=paper)
    agency.add_newspaper(paper)
    agency.create_issue(paper_id=paper.paper_id,issue=issue1)
    agency.create_issue(paper_id=paper.paper_id,issue=issue2)
    all_issues = agency.all_issues(paper_id=paper.paper_id)
    
    
    assert len(all_issues) == 2
    assert issue1 in all_issues and issue2 in all_issues
    assert issue1 == agency.get_issue(paper.paper_id,issue_id=1)
    assert issue2 == agency.get_issue(paper.paper_id,issue_id=2) 
    assert agency.get_issue(paper.paper_id,issue_id=5565) == False #IF ISSUE OR PAPER BY ID IS NOT FOUND RETURNS FALSE HERE ISSUE_ID IS WRONG
    assert agency.get_issue(paper_id=1332,issue_id=5565) == False  # HERE PAPER_ID IS WRONG



def test_adding_editor(agency: Agency):
    before = len(agency.editors)
    editor1 = Editor(editor_id=112,name="Jake",address="Baker street 21")
    agency.add_editor(editor1)

    assert before+1 == len(agency.editors) 
    assert editor1 in agency.editors
    assert agency.add_editor(editor=Editor(editor_id=112,name="Arsenii",address="Quiet street 12b")) == False # SHOULD RETURN FALSE AS EDITOR WITH ID 112 ALREADY EXISTS


def test_getting_all_editors_and_by_id(agency: Agency):
    editor228 = Editor(editor_id=228,name="Lin",address="China Town 1")
    agency.add_editor(editor228)

    
    assert agency.editors == agency.get_editors()
    assert agency.get_editor(editor_id=228) == editor228
    assert not agency.get_editor(editor_id=90202020) #editor with this id does not exist so it should return False


def test_changing_editor(agency: Agency):
    editor1337 = Editor(editor_id=1337,name="Olof",address="Stadtgraben 21/2")
    agency.add_editor(editor1337)
    
    new_editor = Editor(editor_id=1337,name="Jule",address="Dresdner Strasse 17") #ID HAS TO BE THE SAME
    agency.update_editor(new_editor,editor_id=1337)
    updated_editor = agency.get_editor(editor_id=1337)
    
    assert updated_editor.name == new_editor.name
    assert updated_editor.address == new_editor.address
    assert agency.update_editor(new_editor,editor_id=7577) == False #THIS ID IS WRONG SO IT SOULD RETURN False



def test_removing_an_editor(agency: Agency):
    reditor = Editor(editor_id=192,name="Max",address="Obere 12b")
    paper = agency.get_newspaper(paper_id=100)
    issue = agency.get_issue(paper_id=100,issue_id=1)
    agency.add_editor(reditor)
    agency.set_editor(paper_id=paper.paper_id,issue_id=1,editor_id=reditor.editor_id)
    before = len(agency.editors)
    agency.delete_editor(editor_id=reditor.editor_id)
    assert len(agency.editors) == before-1
    assert reditor not in agency.editors
    assert not agency.delete_editor(editor_id=192) # ID 192 NOT PRESENT IN EDITORS NOW SO IT SHOULD RETURN FALSE
    assert reditor not in paper.editors #CHEKS FOR HIS PRESENCE IN NEWSPAPER'S EDITORS LIST
    assert paper not in reditor.newspapers #checks if paper is deleted from editor's newspapers
    assert issue.editor != reditor #asserts that the issue's editor has changed


def test_getting_all_editor_issues(agency: Agency):
    paper1 = agency.get_newspaper(100)
    issue1 = agency.get_issue(paper_id=100,issue_id=1)
    paper2 = agency.get_newspaper(101)
    issue2 = agency.get_issue(paper_id=101,issue_id=1)
    editor = agency.get_editor(editor_id=33)
    
    agency.set_editor(paper_id=100,issue_id=1,editor_id=33)
    agency.set_editor(paper_id=101,issue_id=1,editor_id=33)
    assert issue1 in editor.issues
    assert issue2 in editor.issues
    assert len(editor.issues) == len(agency.get_editor_issues(editor_id=33))
    assert agency.get_editor_issues(editor_id=33) == editor.issues
    assert agency.get_editor_issues(editor_id=59493) == False #as our editor with id 59493 does not exist and was not found it should return False


def test_setting_editor_for_issue(agency: Agency):
    issue1 = agency.get_issue(paper_id=555,issue_id=1)
    paper = agency.get_newspaper(paper_id=555)
    editor = agency.get_editor(editor_id=11)
    agency.set_editor(paper_id=paper.paper_id,issue_id=issue1.issue_id,editor_id=editor.editor_id)
    assert issue1.editor == editor
    assert editor in paper.editors
    assert paper in editor.newspapers
    #now trying to plug in wrong values of paper_id or issue_id or editor_id
    assert agency.set_editor(paper_id=paper.paper_id,issue_id=54,editor_id=editor.editor_id) == False
    assert agency.set_editor(paper_id=paper.paper_id,issue_id=issue1.issue_id,editor_id=99932) == False
    assert agency.set_editor(paper_id=129394,issue_id=issue1.issue_id,editor_id=editor.editor_id) == False
    

def test_release_issue(agency):
    issue1 = Issue(releasedate="13.11.2014",pages=53)
    paper = Newspaper(paper_id=844,name="KyivTimes",frequency=4,price=99)
    agency.add_newspaper(paper)
    agency.create_issue(paper_id=844,issue=issue1)
    agency.release_issue(paper_id=844,issue_id=1)
    
    assert issue1.released == True
    assert agency.release_issue(paper_id=31293192392,issue_id = 1) == False # false if paper was not found
    assert agency.release_issue(paper_id=844,issue_id=45) == False #if issue was not found



def test_adding_subscriber(agency):
    before = len(agency.subscribers)
    sub = Subscriber(subscriber_id=61,name = "Leo",address="Bilder 54a")
    agency.add_subscriber(sub)
    assert len(agency.subscribers) == before +1
    assert agency.add_subscriber(Subscriber(subscriber_id=61,name = "Theo",address="Washington 1")) == False #IF WE TRY TO ADD SUBSCRIBER WITH ID WHICH ALREADY EXISTS IT RETURNS FALSE


def test_all_subs(agency):
    counter = len(agency.subscribers)
    all_subs = agency.get_subscribers()
    assert len(all_subs) == counter
    assert all_subs == agency.subscribers


def test_get_sub_by_id(agency):
    subscriber = Subscriber(subscriber_id=228,name="Iann",address="Lower Danube strasse")
    agency.add_subscriber(subscriber)
    test_sub = agency.subscribers[0]
    assert agency.get_subscriber(test_sub.subscriber_id) == test_sub
    assert agency.get_subscriber(subscriber_id=228) == subscriber
    assert agency.get_subscriber(subscriber_id=1030) == False #It returns False if subscriber was not found



def test_remove_subscriber(agency):
    before = len(agency.subscribers)
    sub = agency.subscribers[1]
    agency.delete_subscriber(sub.subscriber_id)
    assert len(agency.subscribers) == before - 1
    assert agency.subscribers[1] != sub
    assert agency.delete_subscriber(subscriber_id=1232131) == False # it returns false if subscriber was not found


def test_update_sub(agency):
    subscriber = Subscriber(subscriber_id=7,name="Kianu",address="Lizard street")
    agency.add_subscriber(subscriber)
    new_subscriber = Subscriber(subscriber_id=7,name='victor',address="wizard tower") #id has to remain the same
    agency.update_subscriber(7,new_subscriber)
  
    assert agency.get_subscriber(subscriber_id=7).name == new_subscriber.name
    assert agency.get_subscriber(subscriber_id=7).address == new_subscriber.address
    assert agency.get_subscriber(subscriber_id=7).name != "Kianu"
    assert agency.get_subscriber(subscriber_id=7).address != 'Lizard street'
    assert agency.update_subscriber(subscriber_id=6666,upd_subscriber=new_subscriber) == False # if id is not present it returns false



def test_subscribe(agency):
    subscriber = Subscriber(subscriber_id=2507,name="Simon",address="Spittelau")
    agency.add_subscriber(subscriber)
    paper = agency.get_newspaper(paper_id=555)
    
    before_in_ns = len(paper.subscribers)
    before_in_sub = len(subscriber.newspapers)
    agency.subscribe(paper_id=555,subscriber_id=2507)
    assert len(paper.subscribers) == before_in_ns+1
    assert len(subscriber.newspapers) == before_in_sub+1
    assert paper in subscriber.newspapers
    assert subscriber in paper.subscribers
    assert agency.subscribe(paper_id=594394,subscriber_id=2507) == False #will return fALSE WHEN paper or subscriber id was not found
    assert agency.subscribe(paper_id=555,subscriber_id=30549349) == False


def test_deliver_issue(agency):
    paper = Newspaper(paper_id=533,name = "Kharkiv News",frequency=5,price = 80)
    issue = Issue(releasedate="Today",pages=5)
    sub = Subscriber(subscriber_id=4567,name = "Hlib",address="Olofmeister strasse 93c")
    
    agency.add_newspaper(paper)
    agency.add_subscriber(sub)
    agency.create_issue(paper_id=533,issue=issue)
    assert agency.deliver_issue(paper_id=533,issue_id=1,subscriber_id=4567) == f"Issue id {issue.issue_id} from {paper.name} is not released yet" # when trying to deliver unreleased issue
    agency.release_issue(paper_id=533,issue_id=1)
    assert agency.deliver_issue(paper_id=533,issue_id=1,subscriber_id=4567) == f"Subscriber {sub.name} id -{sub.subscriber_id} is not subscribed to {paper.name} id{paper.paper_id}" #when trying to send the issue to the subscriber who is not subscribed to the newspaper
    agency.subscribe(paper_id=533,subscriber_id=4567)
    assert agency.deliver_issue(paper_id=533,issue_id=1,subscriber_id=4567) == f"Issue was delivered to subscriber {sub.name} id -{sub.subscriber_id}"
    assert agency.deliver_issue(paper_id=533,issue_id=1,subscriber_id=4567) == f"Issue was already delivered to subscriber {sub.name} id -{sub.subscriber_id}" #IF WE TRY TO DELIVER ONCE AGAIN IT WILL NOTIFY THAT THE ISSUE WAS ALREADY DELIVERED TO SUB
    assert issue in sub.received_issues
    assert len(sub.received_issues)== 1
    assert agency.deliver_issue(paper_id=1494994,issue_id=1,subscriber_id=4567) == "Paper or Issue or Subscriber was not found please check the ID's!" #returns when something is missing
    assert agency.deliver_issue(paper_id=533,issue_id=2,subscriber_id=4567) == "Paper or Issue or Subscriber was not found please check the ID's!"
    assert agency.deliver_issue(paper_id=533,issue_id=1,subscriber_id=456777) == "Paper or Issue or Subscriber was not found please check the ID's!"





def test_sub_stats(agency):
    paper1 = Newspaper(paper_id=7777,name="Space X",frequency=4,price=10)
    paper2 = Newspaper(paper_id=888,name="Cinema News",frequency=2,price=30)
    sub = Subscriber(subscriber_id=666,name="Lukas",address="Manchester street")
    issue1 = Issue(releasedate="12.4.2012",pages=12)
    issue2 = Issue(releasedate="08.11.2006",pages=4)
    
    agency.add_newspaper(paper1)
    agency.add_newspaper(paper2)
    agency.add_subscriber(sub)
    agency.create_issue(paper_id=888,issue=issue1)
    agency.create_issue(paper_id=7777,issue=issue2)
    
    agency.subscribe(paper_id=888,subscriber_id=666)
    agency.release_issue(paper_id=888,issue_id=1)
    agency.release_issue(paper_id=7777,issue_id=1)
    
    agency.deliver_issue(paper_id=888,issue_id=1,subscriber_id=666)
    stats = agency.get_subsriber_stats(subcriber_id=666)
    
    assert stats == {"subscriber_id":sub.subscriber_id,"name":sub.name,"address":sub.address,"monthly_cost":30,"yearly_cost":360,"issues_recieved":1}
 
    agency.subscribe(paper_id=7777,subscriber_id=666)
    agency.deliver_issue(paper_id=7777,issue_id=1,subscriber_id=666)
    stats_with_2 = agency.get_subsriber_stats(subcriber_id=666)
    
    
    assert stats_with_2 == {"subscriber_id":sub.subscriber_id,"name":sub.name,"address":sub.address,"monthly_cost":40,"yearly_cost":480,"issues_recieved":2}
    assert not agency.get_subsriber_stats(subcriber_id=3129394) # will return false as ID was not found


def test_paper_stats(agency):
    paper = Newspaper(paper_id=57,name = "Lokomotiv",frequency=4,price=100)
    sub1 = Subscriber(subscriber_id=953,name = "Felix",address="Kilimajaro")
    sub2 = Subscriber(subscriber_id=593,name = "Ulrich",address="Untere 21")
    sub3 = Subscriber(subscriber_id=395,name = "Luke",address="Wien Heilgenstadt")
    agency.add_newspaper(paper)
    agency.add_subscriber(sub1),agency.add_subscriber(sub2),agency.add_subscriber(sub3)
    assert agency.get_newspaper_stats(paper_id=57) == {
            "paper_id":paper.paper_id,
            "name":paper.name,
            "price":paper.price,
            "frequency":paper.frequency,
            "subscriber_amount":0,
            "montly_revenue":0,
            "annual_revenue":0
            }
    agency.subscribe(paper_id=57,subscriber_id=953)
    assert agency.get_newspaper_stats(paper_id=57) == {
            "paper_id":paper.paper_id,
            "name":paper.name,
            "price":paper.price,
            "frequency":paper.frequency,
            "subscriber_amount":1,
            "montly_revenue":100,
            "annual_revenue":1200
            }
    agency.subscribe(paper_id=57,subscriber_id=593)
    agency.subscribe(paper_id=57,subscriber_id=395)
    assert agency.get_newspaper_stats(paper_id=57) == {
            "paper_id":paper.paper_id,
            "name":paper.name,
            "price":paper.price,
            "frequency":paper.frequency,
            "subscriber_amount":3,
            "montly_revenue":300,
            "annual_revenue":3600
            }
    assert agency.get_newspaper_stats(paper_id=392949) == False # If no paper with this ID FOUND IT RETURNS FALSE



def test_missing_issues(agency):
    paper = Newspaper(paper_id=69,name = "Oxford",frequency=2,price=10)
    agency.add_newspaper(paper)
    issue1 = Issue(releasedate="25.07.2004",pages=19)
    issue2 = Issue(releasedate="Tomorrow",pages=1)
    agency.create_issue(paper_id=69,issue=issue1)
    agency.create_issue(paper_id=69,issue=issue2)
    sub = Subscriber(subscriber_id=46,name= "Valentina",address="Lomanosova 24b")
    agency.add_subscriber(sub)
    
    assert agency.get_missing_issues(subscriber_id=46) == {"issues":[]} # it is empty as our sub is not subscribed to anything
    
    agency.subscribe(paper_id=69,subscriber_id=46)
   
    assert agency.get_missing_issues(subscriber_id=46) == {"issues":[]} #still empty as no issues were released
    
    agency.release_issue(paper_id=69,issue_id=1)
    assert agency.get_missing_issues(subscriber_id=46) == {"issues":[{"issue_id":issue1.issue_id,
                                                                      "releasedate":issue1.releasedate,
                                                                      "newspaper":issue1.newspaper.name}]} 
    
    agency.release_issue(paper_id=69,issue_id=2)

    assert agency.get_missing_issues(subscriber_id=46) == {"issues":[{"issue_id":issue1.issue_id,
                                                                      "releasedate":issue1.releasedate,
                                                                      "newspaper":issue1.newspaper.name},
                                                                      {"issue_id":issue2.issue_id,
                                                                       "releasedate":issue2.releasedate,
                                                                       "newspaper":issue2.newspaper.name}]} 

    agency.deliver_issue(paper_id=69,issue_id=1,subscriber_id=46)

    assert agency.get_missing_issues(subscriber_id=46) == {"issues":[{"issue_id":issue2.issue_id,
                                                                       "releasedate":issue2.releasedate,
                                                                       "newspaper":issue2.newspaper.name}]}

   
    agency.deliver_issue(paper_id=69,issue_id=2,subscriber_id=46)
    
    assert agency.get_missing_issues(subscriber_id=46) == {"issues":[]} 
    assert agency.get_missing_issues(subscriber_id=493599593) == "Subscriber 493599593 was not found!"


    