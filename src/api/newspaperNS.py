from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from time import time_ns
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from datetime import date,datetime


newspaper_ns = Namespace("newspaper", description="Newspaper related operations")



issue_model= newspaper_ns.model('IssueModel',{
    'issue_id': fields.Integer(help="Number of an issue"),
    'releasedate': fields.String(required = True,help = "Date of the release of an issue"),
    'pages': fields.Integer(required = True, help="Number of pages of an issue"),
    'editor': fields.String(required = True, help = "Editor of an Issue"),
    'released': fields.Boolean(help = "State of issue")
})

issue_input_model = newspaper_ns.model('IssueInputModel',{
    'release_date': fields.String(required = True,help = "Date of the release of an issue"),
    'pages': fields.Integer(required = True, help="Number of pages of an issue"),
    'editor': fields.String(required = True, help = "Editor of an Issue"),
    })


paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)'),
    'issues': fields.List(fields.Nested(issue_model,required = True, help="All issues of a particular pages"))
   
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
        paper_id = int(time_ns()*0.001)

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
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        return search_result

    @newspaper_ns.doc(parser=paper_input_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_input_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def put(self, paper_id):
        # TODO: update newspaper
        upd_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        return Agency.get_instance().update_newspaper(upd_paper)
            


    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")


@newspaper_ns.route('/<int:paper_id>/issue')
class IssueApi(Resource):
    
    @newspaper_ns.doc(description="Get an issue")
    @newspaper_ns.marshal_with(issue_model)
    def get(self,paper_id):
        issues = Agency.get_instance().all_issues(paper_id)
        return issues
    

    @newspaper_ns.expect(issue_input_model)
    def post(self,paper_id):
        issue = Issue(releasedate=newspaper_ns.payload['release_date'],
                    pages=newspaper_ns.payload['pages'],
                    editor=newspaper_ns.payload['editor'])
        
        Agency.get_instance().create_issue(paper_id=paper_id,issue=issue)
        return jsonify(f"Issue number - {issue.issue_id} has been added to {Agency.get_instance().get_newspaper(paper_id).name} newspaper")
    
@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class IssueId(Resource):
    
    @newspaper_ns.marshal_with(issue_model)
    def get(self,paper_id,issue_id):
        issue = Agency.get_instance().get_issue(paper_id,issue_id)
        return issue
    

@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/release',methods=['POST'])
class ReleaseIssue(Resource):
    def post(self,paper_id,issue_id):
        if Agency.get_instance().release_issue(paper_id,issue_id):
            return jsonify(f"Issue number - {issue_id} has been released")
    
        else:
            return jsonify(f"Issue number - {issue_id} wasn't released")