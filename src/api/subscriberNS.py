from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields,abort
from time import time_ns
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.subscriber import Subscriber


subscriber_ns = Namespace("subscriber", description="Subscriber related operations")


paper_model = subscriber_ns.model('NewspaperForSubscriberModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')})



subscriber_model = subscriber_ns.model("SubscriberModel",{
    "subscriber_id":fields.Integer(),
    "name":fields.String(),
    })

subscriber_info_model = subscriber_ns.model("SubscriberInfoModel",{
    "subscriber_id":fields.Integer(),
    "name":fields.String(),
    "address":fields.String(),
    "newspapers":fields.List(fields.Nested(paper_model))

})

subscribe_model = subscriber_ns.model("SubscribeModel",{
    "paper_id": fields.Integer()
})

subscriber_input_model = subscriber_ns.model("SubscriberInputModel",{
    "name": fields.String(),
    "address": fields.String(),
})


@subscriber_ns.route("/")
class SubscriberApi(Resource):
   
   
    @subscriber_ns.marshal_with(subscriber_model)
    def get(self):
        return Agency.get_instance().get_subscribers()
    
    @subscriber_ns.marshal_with(subscriber_info_model)
    @subscriber_ns.expect(subscriber_input_model)
    def post(self):
        id = int(str((time_ns()))[8:15])
        subscriber = Subscriber(subscriber_id=id,name = subscriber_ns.payload["name"],address= subscriber_ns.payload["address"])
        status = Agency.get_instance().add_subscriber(subscriber)
        if status:
            return status
        else:
            abort(422,{"error":"id is already occupied"})
    


@subscriber_ns.route("/<int:subscriber_id>")
class SubscriberId(Resource):

    @subscriber_ns.marshal_with(subscriber_info_model)
    def get(self,subscriber_id):
        sub = Agency.get_instance().get_subscriber(subscriber_id)
        if sub:
            return sub
        else:
            abort(422,{"error":"id is not correct"})

    @subscriber_ns.expect(subscriber_input_model)
    def post(self,subscriber_id):
        upd_sub = Subscriber(subscriber_id=subscriber_id,name = subscriber_ns.payload["name"],address=subscriber_ns.payload["address"])
        status = Agency.get_instance().update_subscriber(subscriber_id,upd_sub)
        if status:
            return status
        else:
            abort(422,{"error":"id is not correct"})
    

    def delete(self,subscriber_id):
        status = Agency.get_instance().delete_subscriber(subscriber_id)
        if status: 
            return status
        else:
            abort(422,{"error":"id is not correct"})
    

@subscriber_ns.route('/<int:subscriber_id>/subscribe')
class SubcriberSubcribe(Resource):

    @subscriber_ns.expect(subscribe_model)
    def post(self,subscriber_id):
        status = Agency.get_instance().subscribe(subscriber_ns.payload["paper_id"],subscriber_id)
        if status:
            return status
        else:
            abort(422,{"error":"id is not correct"})

@subscriber_ns.route('/<int:subscriber_id>/stats')
class SubscriberStats(Resource):
    def get(self,subscriber_id):
        status = Agency.get_instance().get_subsriber_stats(subscriber_id)
        if status:
            return status
        else:
            abort(422,{"error":"id is not correct"})
    

@subscriber_ns.route('/<int:subscriber_id>/missingissues')
class SubscriberMissingIssues(Resource):
    
    
    def get(self,subscriber_id):
        status = Agency.get_instance().get_missing_issues(subscriber_id)
        if status:
            return status
        else:
            abort(422,{"error":"id is not correct"})
    