from typing import List, Union, Optional
from flask import jsonify
from .newspaper import Newspaper
from .editor import Editor

class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
    
    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        #TODO: assert that ID does not exist  yet (or create a new one)
        if not self.get_newspaper(new_paper.paper_id):
            self.newspapers.append(new_paper)



    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None


    def update_newspaper(self,upd_paper):
        if self.get_newspaper(upd_paper.paper_id):
            self.get_newspaper(upd_paper.paper_id).name = upd_paper.name
            self.get_newspaper(upd_paper.paper_id).frequency = upd_paper.frequency
            self.get_newspaper(upd_paper.paper_id).price = upd_paper.price
            return self.get_newspaper(upd_paper.paper_id)
        else: 
            return None
    
    
    
    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)



    def all_issues(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        return self.get_newspaper(paper_id).issues
    

    def get_issue(self, paper_id: Union[int,str],issue_id) -> Optional[Newspaper]:
        return self.get_newspaper(paper_id).get_issue(issue_id)


    def create_issue(self, paper_id: Union[int,str],issue = None) -> Optional[Newspaper]:
        return self.get_newspaper(paper_id).add_issue(issue)

    

    def release_issue(self,paper_id,issue_id):
        return self.get_newspaper(paper_id).release_issue(issue_id)

    def get_editors(self):
        return self.editors

    def get_editor(self,editor_id):
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        
    def add_editor(self,editor):
        if not self.get_editor(editor.editor_id):
            self.editors.append(editor)
            return editor
        else:
            return None
    
    

    def set_editor(self,paper_id,issue_id,editor_id):
        editor = self.get_editor(editor_id)
        issue = self.get_issue(paper_id,issue_id)
        issue.set_editor(editor)
        editor.add_issue(issue)
        editor.add_newspaper(issue.newspaper)  
        return self.get_issue(paper_id,issue_id)
        


    def update_editor(self,upd_editor,editor_id):
        editor = self.get_editor(editor_id)
        
        editor.name = upd_editor.name
        editor.address = upd_editor.address
        return edito