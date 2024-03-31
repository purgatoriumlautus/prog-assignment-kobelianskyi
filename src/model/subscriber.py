
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
        return {"subscriber_id":self.subscriber_id,"name":self.name,"address":self.address,"monthly_cost":montly_cost,"yearly_cost":yearly_cost,"issues_recieved":issues_recieved} 

