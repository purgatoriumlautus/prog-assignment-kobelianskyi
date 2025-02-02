from datetime import date

class Issue(object):

    def __init__(self,releasedate=date.today(), pages = 1, released: bool = False,newspaper = None):
        self.issue_id = None
        self.releasedate = str(releasedate)
        self.released: bool = released
        self.pages: int = pages
        self.newspaper = newspaper
        if newspaper != None:
            self.editor = newspaper.editors[0]
        
        
    def set_editor(self, editor):
        self.editor = editor
        return editor


    # def __repr__(self) -> str:
    #     return f'''Release date: {self.releasedate},
    #     pages: {self.pages},
    #     editor: {self.editor}
    #     '''
