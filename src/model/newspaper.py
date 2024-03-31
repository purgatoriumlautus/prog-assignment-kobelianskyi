from typing import List

from flask_restx import Model

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
        

    def release_issue(self,issue_id):
        issue = self.get_issue(issue_id)
        if issue:
            return issue.release() #released or already released

        return f"ID - {issue_id} WAS NOT FOUND"