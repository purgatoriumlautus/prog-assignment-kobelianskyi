from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields,abort
from time import time_ns
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue



newspaper_ns = Namespace("newspaper", description="Newspaper related operations")

editor_model = newspaper_ns.model('EditorNewsModel',{
    'editor_id': fields.Integer(required = True, help = "Unique editor's id"),
    'name': fields.String(required = True,help = "Name of the editor")
    })


editor_id_input_model = newspaper_ns.model("Editor_Id_InputModel",{
    "editor_id":fields.Integer(required=True,help=" Unique editor's id")
    })

issue_model =  newspaper_ns.model('IssueModel',{
    'issue_id': fields.Integer(help="Number of an issue"),
    'releasedate': fields.String(required = True,help = "Date of the release of an issue"),
    'pages': fields.Integer(required = True, help="Number of pages of an issue"),
    'released': fields.Boolean(help = "State of issue"),
    'editor': fields.Nested(editor_model)
})

issue_input_model = newspaper_ns.model('IssueInputModel',{
    'release_date': fields.String(required = True,help = "Date of the release of an issue"),
    'pages': fields.Integer(required = True, help="Number of pages of an issue")
    })


paper_model= newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)'),
    'subscriber_amount': fields.Integer()
   })

subscriber_id_model = newspaper_ns.model("SubscriberIdModel",{
    "subscriber_id": fields.Integer()})

subscriber_model = (newspaper_ns.model("SubscriberPaperModel",{
    "subscriber_id": fields.Integer(),
    'name':fields.String(),
    'received_issues':fields.List(fields.Nested(issue_model))
    }))


paper_info_model = newspaper_ns.model('NewspaperInfoModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)'),
    'issues': fields.List(fields.Nested(issue_model,required = True, help="All issues of a particular pages")),
    'editors': fields.List(fields.Nested(editor_model)),
    'subscribers': fields.List(fields.Nested(subscriber_model)),
    'subscriber_amount':fields.Integer()
   
   })


paper_input_model = newspaper_ns.model('NewspaperInputModel', {
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })









@newspaper_ns.route('/')
class NewspaperAPI(Resource):
    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_input_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        # TODO: this is not smart! you should find a better way to generate a unique ID!
        paper_id = int(str(time_ns())[9:17])

        # create a new paper object and add it
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        
        Agency.get_instance().add_newspaper(new_paper)

        # return the new paper
        return new_paper

    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()


@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):
    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_info_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        if search_result:
            return search_result
        else:
            abort(422,{"error":"id is not correct"})

    @newspaper_ns.doc(parser=paper_input_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_input_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        # TODO: update newspaper
        upd_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        new_paper = Agency.get_instance().update_newspaper(upd_paper)
        if new_paper:
            return new_paper
        else:
            abort(422,{"error":"id is not correct"})

            


    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            abort(422,{"error":"id is not correct"})

        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")


@newspaper_ns.route('/<int:paper_id>/issue')
class IssueApi(Resource):
    @newspaper_ns.doc(description="Get an issue")
    @newspaper_ns.marshal_with(issue_model)
    def get(self,paper_id):
        issues = Agency.get_instance().all_issues(paper_id)
        if issues:
            return issues
        else:
            abort(422,{"error":"id is not correct"})

    

    @newspaper_ns.expect(issue_input_model)
    def post(self,paper_id):
        news = Agency.get_instance().get_newspaper(paper_id)
        if news:
            issue = Issue(releasedate=newspaper_ns.payload['release_date'],
                        pages=newspaper_ns.payload['pages'])
            
            Agency.get_instance().create_issue(paper_id=paper_id,issue=issue)
            return jsonify(f"Issue number - {issue.issue_id} has been added to {Agency.get_instance().get_newspaper(paper_id).name} newspaper")
        
        else:
            abort(422,{"error":"id is not correct"})



@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class IssueId(Resource):
    
    @newspaper_ns.marshal_with(issue_model)
    def get(self,paper_id,issue_id):
        issue = Agency.get_instance().get_issue(paper_id,issue_id)
        if issue:
            return issue
        else:
            abort(422,{"error":"id is not correct"})
    
    

@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/release',methods=['POST'])
class ReleaseIssue(Resource):
    def post(self,paper_id,issue_id):
        issue = Agency.get_instance().release_issue(paper_id,issue_id)
        if issue:
            return issue
        else:
            abort(422,{"error":"id is not correct"})




@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/editor',methods=['POST'])
class SpecifyEditor(Resource):
    @newspaper_ns.marshal_with(issue_model)
    @newspaper_ns.expect(editor_id_input_model,validate=True)
    def post(self,paper_id,issue_id):
        status = Agency.get_instance().set_editor(paper_id,issue_id,newspaper_ns.payload["editor_id"])
        if status:
            return status
        else:
            abort(422,{"error":"id is not correct"})
    

@newspaper_ns.route('/<int:paper_id>/stats')
class NewspaperStats(Resource):


    def get(self,paper_id):
        paper = Agency.get_instance().get_newspaper_stats(paper_id)
        if paper:
            return paper
        else:
            abort(422,{"error":"id is not correct"})
    
    
        

@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>/deliver")
class DeliverIssue(Resource):
    
    @newspaper_ns.expect(subscriber_id_model)

    def post(self,paper_id,issue_id):
        sub_id = newspaper_ns.payload["subscriber_id"]
        return jsonify(Agency.get_instance().deliver_issue(paper_id,issue_id,sub_id))
