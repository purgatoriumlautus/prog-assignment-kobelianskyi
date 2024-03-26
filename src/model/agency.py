from typing import List, Union, Optional
from flask import jsonify
from .newspaper import Newspaper


class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []

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
            self.remove_newspaper(self.get_newspaper(upd_paper.paper_id))
            self.newspapers.append(upd_paper)
            return upd_paper
        else: 
            return None
    
    
    
    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)

