from typing import List


from .issue import Issue
from .editor import Editor
from random import randint


class Newspaper(object):
    
    
    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []
        self.editors: List[Editor] = [Editor(editor_id=paper_id,name=name,address=f"{name}'s office")]
        self.subscribers = []
        self.subscriber_amount = 0

    def add_issue(self,issue):
        issue.issue_id = len(self.issues)+1
        self.issues.append(issue)
        return issue


    def get_issue(self,issue_id):
        for issue in self.issues:
            if issue_id == issue.issue_id:
                return issue
        return False


    def add_editor(self,editor):
        for edit in self.editors:
            if edit.editor_id == editor.editor_id:
                return False
        else:
            self.editors.append(editor)
            return True
    

    def get_editor(self):
        if len(self.editors) == 1:
            return self.editors[0]
        elif len(self.editors) == 2:
            return self.editors[1]
        else:
            return self.editors[randint(1,len(self.editors)-1)]


    def delete_editor(self,editor):
        self.editors.remove(editor)
        

    def get_subscriber(self,subscriber_id):
        for sub in self.subscribers:
            if sub.subscriber_id == subscriber_id:
                return sub
        return None

    def add_subscriber(self,subscriber):
        if not self.get_subscriber(subscriber.subscriber_id):
            self.subscribers.append(subscriber)
            self.subscriber_amount += 1
        return subscriber
        





    def get_stats(self):
        stats = {
            "paper_id":self.paper_id,
            "name":self.name,
            "price":self.price,
            "frequency":self.frequency,
            "subscriber_amount":self.subscriber_amount,
            "montly_revenue":self.subscriber_amount*self.price,
            "annual_revenue":self.price*self.subscriber_amount*12
            }
        return stats