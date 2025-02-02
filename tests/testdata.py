from src.model.agency import Agency
from src.model.newspaper import Newspaper
from src.model.issue import Issue
from src.model.editor import Editor
from src.model.subscriber import Subscriber


def create_newspapers(agency: Agency):
    paper1 = Newspaper(paper_id=100, name="The New York Times", frequency=7, price=13.14)
    paper2 = Newspaper(paper_id=101, name="Heute", frequency=1, price=1.12)
    paper3 = Newspaper(paper_id=115, name="Wall Street Journal", frequency=1, price=3.00)
    paper4 = Newspaper(paper_id=125, name="National Geographic", frequency=30, price=34.00)
    paper5 = Newspaper(paper_id=195, name="Ukraine", frequency=5, price=98)
    agency.newspapers.append(paper1),agency.newspapers.append(paper2),agency.newspapers.append(paper3),agency.newspapers.append(paper4),agency.newspapers.append(paper5)
   
    issue1 = Issue(releasedate="25.07.2004",
                        pages=6,
                            newspaper=paper1)
    issue2 = Issue(releasedate="31.02.2024",
                        pages=2,
                            newspaper=paper2)
    issue3 = Issue(releasedate="11.12.2020",
                        pages=2,
                            newspaper=paper3)
    issue4 = Issue(releasedate="02.03.2017",
                        pages=2,
                            newspaper=paper4)
    agency.create_issue(paper_id=100,issue=issue1)
    agency.create_issue(paper_id=101,issue=issue2)
    agency.create_issue(paper_id=115,issue=issue3)
    agency.create_issue(paper_id=125,issue=issue4)
    
    editor1 = Editor(editor_id=33,name="Kendall",address="Lakes 21")
    editor2 = Editor(editor_id=22,name="Ben",address="Landstrasse 29")
    editor3 = Editor(editor_id=11,name="Maria",address="Morimedo-chou")
    
    agency.set_editor(paper_id=115,issue_id=1,editor_id=11)
    agency.set_editor(paper_id=100,issue_id=1,editor_id=33)
    agency.set_editor(paper_id=125,issue_id=1,editor_id=22)
    
    agency.editors.extend([editor1,editor2,editor3])
    sub1 = Subscriber(subscriber_id=1,name = "Vasiliy",address="Mihailovo 12b")
    sub2 = Subscriber(subscriber_id=21,name="Naruto",address="Ookland street")
    sub3 = Subscriber(subscriber_id=41,name = "Jakie",address="Rivermall avenue 5")
    agency.add_subscriber(sub1),agency.add_subscriber(sub2),agency.add_subscriber(sub3)



def populate(agency: Agency):
    create_newspapers(agency)

