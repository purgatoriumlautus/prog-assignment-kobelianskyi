from typing import List
from .issue import Issue



class Editor(object):
    def __init__(self,editor_id:int = None,name:str=None,address:str =None):
        self.editor_id = editor_id
        self.name = name
        self.address = address
        self.newspapers = []
        self.issues: List[Issue] = []
    

    def add_issue(self,issue):
        self.issues.append(issue)
        
        
    def add_newspaper(self,newspaper):
        for news in self.newspapers:
            if news.paper_id == newspaper.paper_id:
                return None
        self.newspapers.append(newspaper)
        return True
    
    
    def get_issues(self):
        return self.issues