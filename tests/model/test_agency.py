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


# def test_add_newspaper_same_id_should_raise_error(agency):
   
#     new_paper = Newspaper(paper_id=999,
#                           name="Simpsons Comic",
#                           frequency=7,
#                           price=3.14)

#     # first adding of newspaper should be okay
#     agency.add_newspaper(new_paper)
    
    
#     new_paper2 = Newspaper(paper_id=999,
#                           name="Superman Comic",
#                           frequency=7,
#                           price=13.14)

#     with pytest.raises(ValueError, match='A newspaper with ID 999 already exists'):  # <-- this allows us to test for exceptions
#         # this one should raise an exception!
#         agency.add_newspaper(new_paper2)
    




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
    
    upd_paper = agency.update_newspaper(new_paper) #update_newspaper returns NONE when paper id is not found
    
    assert upd_paper == None

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
    assert agency.update_editor(new_editor,editor_id=7577) == None #THIS ID IS WRONG SO IT SOULD RETURN NONE



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
    assert agency.get_editor_issues(editor_id=59493) == None #as our editor with id 59493 does not exist and was not found it should return None


def test_setting_editor_for_issue(agency: Agency):
    issue1 = agency.get_issue(paper_id=555,issue_id=1)
    paper = agency.get_newspaper(paper_id=555)
    editor = agency.get_editor(editor_id=11)
    agency.set_editor(paper_id=paper.paper_id,issue_id=issue1.issue_id,editor_id=editor.editor_id)
    assert issue1.editor == editor
    assert editor in paper.editors
    assert paper in editor.newspapers
    #now trying to plug in wrong values of paper_id or issue_id or editor_id
    assert agency.set_editor(paper_id=paper.paper_id,issue_id=54,editor_id=editor.editor_id) == None
    assert agency.set_editor(paper_id=paper.paper_id,issue_id=issue1.issue_id,editor_id=99932) == None
    assert agency.set_editor(paper_id=129394,issue_id=issue1.issue_id,editor_id=editor.editor_id) == None
    

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
    assert agency.get_subscriber(subscriber_id=1030) == None #It returns None if subscriber was not found



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



#TODO: TEST SUBSCRIBER/SUBSCRIBE TEST SUBSCRIBER/STATS AND SUBSCRIBER/MISSINGISSUES 
#TEST PAPER/STATS
#TEST ISSUE/DELIVER