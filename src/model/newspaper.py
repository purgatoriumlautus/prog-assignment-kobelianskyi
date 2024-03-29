from typing import List

from flask_restx import Model

from .issue import Issue


class Newspaper(object):
    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []


    def add_issue(self,issue):
        issue.issue_id = len(self.issues)+1
        self.issues.append(issue)
        return issue


    def get_issue(self,issue_id):
        for issue in self.issues:
            if issue_id == issue.issue_id:
                return issue
        return None


    def release_issue(self,issue_id):
        if self.get_issue(issue_id).release():
            return True
        return False