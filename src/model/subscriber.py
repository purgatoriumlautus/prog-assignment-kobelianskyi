
class Subscriber(object):
    def __init__(self,subscriber_id,name,address):
        self.subscriber_id = subscriber_id
        self.name = name
        self.address = address
        self.newspapers = []
        self.received_issues = []


    def is_subscribed(self,newspaper):
        for news in self.newspapers:
            if news.paper_id == newspaper.paper_id:
                return True
        return False
    
    
    
    def subscribe_to(self,newspaper):
        if not self.is_subscribed(newspaper):
            self.newspapers.append(newspaper)
            return True
        return False
    

    def get_stats(self):
        montly_cost = 0
        
        issues_recieved = len(self.received_issues)
        for news in self.newspapers:
            montly_cost += news.price

        yearly_cost = montly_cost*12
        return {"subscriber_id":self.subscriber_id,"name":self.name,"address":self.address,"monthly_cost":montly_cost,"yearly_cost":yearly_cost,"issues_recieved":len(self.received_issues)} 


    def receive_issue(self,issue):
        if issue not in self.received_issues:
            self.received_issues.append(issue)
            return True
        
        return False
    

    def check_issues(self):
        missing_issues = {"issues":[]}
        for news in self.newspapers:
            for issue in news.issues:
                if issue not in self.received_issues and issue.released:
                    if hasattr(issue,"editor"):
                        missing_issues["issues"].append({"issue_id":issue.issue_id,"releasedate":issue.releasedate,"newspaper":issue.newspaper.name,"editor":issue.editor.name})
                    else:
                        missing_issues["issues"].append({"issue_id":issue.issue_id,"releasedate":issue.releasedate,"newspaper":issue.newspaper.name})
        return missing_issues
    
    def quit_agency(self):
        for news in self.newspapers:
            news.subscribers.remove(self)
            news.subscriber_amount -= 1