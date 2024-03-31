from datetime import date

class Issue(object):

    def __init__(self,releasedate=date.today(), pages = 1, released: bool = False,newspaper = None):
        self.issue_id = None
        self.releasedate = str(releasedate)
        self.released: bool = released
        self.pages: int = pages
        self.newspaper = newspaper
        self.editor = newspaper.editors[0]
        
        
    def set_editor(self, editor):
        self.editor = editor
        return editor

    def release(self):
        if not self.released:
            self.released = True
            return f"Issue number - {self.issue_id} was succesfully released"

        return f"Issue number - {self.issue_id} was already released"


    # def __repr__(self) -> str:
    #     return f'''Release date: {self.releasedate},
    #     pages: {self.pages},
    #     editor: {self.editor}
    #     '''
