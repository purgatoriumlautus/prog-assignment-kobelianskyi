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
            return(jsonify(f"{paper.release_issue(issue_id)}"))
        
        # if paper:
        #     if paper.release_issue(issue_id) == "already released":
        #         return jsonify(f"Issue number {issue_id} is already released")
        #     if not paper.release_issue(issue_id) == "released":
        #         return jsonify(f"Issue number {issue_id} was succesfully released")
        #     if paper.release_issue(issue_id) == "not found":
        #         return jsonify(f"Issue WAS NOT FOUND!")
        else:
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