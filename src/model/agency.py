from typing import List, Union, Optional
from flask import jsonify
from .newspaper import Newspaper
from .editor import Editor
from .subscriber import Subscriber



class Agency(object):
    singleton_instance = None


    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
        self.subscribers: List[Subscriber] = []
    

    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    
    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return False
    

    def add_newspaper(self, new_paper: Newspaper):
        #TODO: assert that ID does not exist  yet (or create a new one)
        
        if not self.get_newspaper(new_paper.paper_id):
            self.newspapers.append(new_paper)


    def update_newspaper(self,upd_paper):
        paper =  self.get_newspaper(upd_paper.paper_id)
        if paper:
            paper.name = upd_paper.name
            paper.frequency = upd_paper.frequency
            paper.price = upd_paper.price
            return paper
        
        return None
    
    
    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers


    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)



    def all_issues(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        paper = self.get_newspaper(paper_id)
        if paper:
            return paper.issues
        return False


    def get_issue(self, paper_id: Union[int,str],issue_id) -> Optional[Newspaper]:
        paper = self.get_newspaper(paper_id)
        if paper:
            return paper.get_issue(issue_id)
        return False
        

    def create_issue(self, paper_id: Union[int,str],issue = None) -> Optional[Newspaper]:
        paper = self.get_newspaper(paper_id)
        if paper:
            return paper.add_issue(issue)
        return False
    

    def release_issue(self,paper_id,issue_id):
        paper = self.get_newspaper(paper_id)
        if paper:
            return(jsonify(f"{paper.release_issue(issue_id)}")) #can be released now or already released
        return jsonify(f"Paper WAS NOT FOUND!")
        
        
    
    def get_editors(self):
        return self.editors


    def get_editor(self,editor_id):
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return False
    

    def add_editor(self,editor):
        if not self.get_editor(editor.editor_id):
            self.editors.append(editor)
            return editor

    
    def set_editor(self,paper_id,issue_id,editor_id):
        editor = self.get_editor(editor_id)
        issue = self.get_issue(paper_id,issue_id)
        news = self.get_newspaper(paper_id)
        if editor and issue and news:
            news.add_editor(editor)
            issue.set_editor(editor)
            editor.add_issue(issue)
            editor.add_newspaper(issue.newspaper)  
            return self.get_issue(paper_id,issue_id)
        return None


    def update_editor(self,upd_editor,editor_id):
        editor = self.get_editor(editor_id)
        if editor:
            editor.name = upd_editor.name
            editor.address = upd_editor.address
            return editor
        return Editor(editor_id=None,name = None,address=None)


    def delete_editor(self,editor_id):
        editor = self.get_editor(editor_id)
        if editor:
            editor.quit_agency()
            self.editors.remove(editor)
            return True
        return False


    def get_editor_issues(self,editor_id):
        if self.get_editor(editor_id):
            return self.get_editor(editor_id).get_issues()
        return Editor(editor_id=None,name = None,address=None)
    

    def get_subscribers(self):
        return self.subscribers
    

    def get_subscriber(self,subscriber_id):
        for sub in self.subscribers:
            if sub.subscriber_id == subscriber_id:
                return sub
        return None


    def add_subscriber(self,subscriber):
        if not self.get_subscriber(subscriber.subscriber_id):
            self.subscribers.append(subscriber)
        
        
        return subscriber
        
    
    
    def update_subscriber(self,subscriber_id,upd_subscriber):
        subscriber = self.get_subscriber(subscriber_id)
        if subscriber:
            subscriber.name = upd_subscriber.name
            subscriber.address = upd_subscriber.address
            return jsonify(f"Subscriber with id {subscriber_id} was successfully updated")
        else:
            return jsonify(f"ID {subscriber_id} WAS NOT FOUND")
        

    def delete_subscriber(self,subscriber_id):
        subscriber = self.get_subscriber(subscriber_id)
        if subscriber:
            self.subscribers.remove(subscriber)
            return jsonify(f"Subscriber {subscriber.name} with id {subscriber_id} was successfully deleted")
        
        return jsonify(f"ID {subscriber_id} was not FOUND!")
    

    def subscribe(self,paper_id,subscriber_id):
        paper = self.get_newspaper(paper_id)
        sub = self.get_subscriber(subscriber_id)
        if paper and sub:
            paper.add_subscriber(sub)
            sub.subscribe_to(paper)
            return jsonify(f"subscriber {sub.name} with id {sub.subscriber_id} successfully subscribed to {paper.name} with id {paper_id}")
        if paper and not sub:
            return jsonify(f"subscriber id {subscriber_id} WAS NOT FOUND!")
        if sub and not paper:
            return jsonify(f"paper id {paper_id} WAS NOT FOUND!")
        if not sub and not paper:
            return jsonify(f"paper id {paper_id} and subscriber id {subscriber_id} WAS NOT FOUND! ")


    def get_subsriber_stats(self,subcriber_id):
        sub = self.get_subscriber(subcriber_id)
        if sub:
            return sub.get_stats()
        return jsonify(f"subscriber id {subcriber_id} WAS NOT FOUND!")
    

    def get_newspaper_stats(self,paper_id):
        paper = self.get_newspaper(paper_id)
        if paper:
            return paper.get_stats()
        
        return jsonify(f"PAPER {paper_id} WAS NOT FOUND!")
    

    def deliver_issue(self,paper_id,issue_id,subscriber_id):
        paper = self.get_newspaper(paper_id)
        issue = self.get_issue(paper_id,issue_id)
        subscriber = self.get_subscriber(subscriber_id)
        if paper and issue and subscriber:
            if issue.released:
                if subscriber.is_subscribed(paper):
                    if subscriber.receive_issue(issue):
                        return jsonify(f"Issue was delivered to subscriber {subscriber.name} id -{subscriber.subscriber_id} ")
                    else:
                        return jsonify(f"Issue was already delivered to subscriber {subscriber.name} id -{subscriber.subscriber_id} ")
                else:
                    return(jsonify(f"Subscriber {subscriber.name} id -{subscriber.subscriber_id} is not subscribed to {paper.name}\nid{paper.paper_id}"))
            else:
                return(jsonify(f"Issue id {issue_id} from {paper.name} is not released yet"))
        else:
            return(jsonify(f"Paper or Issue or Subscriber was not found please check the ID's!"))
        
    

    def get_missing_issues(self,subscriber_id):
        subscriber = self.get_subscriber(subscriber_id)
        if subscriber:
            return subscriber.check_issues()
        else:
            return(jsonify(f"Subscriber {subscriber_id} was not found!"))
