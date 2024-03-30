from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from time import time_ns
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editor import Editor
from .newspaperNS import paper_model


editor_ns = Namespace("editor", description="Editor related operations")

paper_model = editor_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')})

issue_model = editor_ns.model("Issuemodel",{
    "issue_id":fields.Integer(help= "id of the issue"),
    "releasedate":fields.String(help="date of release of the issue"),
    "released":fields.Boolean(help = "is the issue released"),
    "pages": fields.Integer(help="Number of the pages of an issue"),
    'newspaper':fields.Nested(paper_model)
})

editor_model = editor_ns.model('EditorModel',{
    'editor_id': fields.Integer(help = 'Unique id of the editor'),
    'name': fields.String(help = "Name of the editor"),
    'address': fields.String(help="address of living of the editor"),
    'newspapers': fields.List(fields.Nested(paper_model,required = False, help="All issues of a particular pages")),
    'issues':fields.List(fields.Nested(issue_model,help = "List of all the editor's issues"))
    })
    

editor_input_model = editor_ns.model("EditorInputModel", {
    "name": fields.String(),
    "address": fields.String(),
})




@editor_ns.route("/")
class EditorAPI(Resource):
    @editor_ns.expect(editor_input_model)
    @editor_ns.marshal_with(editor_model)
    def post(self):
        id = int(str(time_ns())[9:17][::-1])
        editor = Editor(editor_id=id, name = editor_ns.payload['name'],address=editor_ns.payload['address'])
        return Agency.get_instance().add_editor(editor)

    @editor_ns.marshal_list_with(editor_model)
    def get(self):
        return Agency.get_instance().get_editors()

@editor_ns.route("/<int:editor_id>")
class EditorId(Resource):
    
    @editor_ns.marshal_with(editor_model)
    def get(self,editor_id):
        return Agency.get_instance().get_editor(editor_id)
    

    @editor_ns.marshal_with(editor_model)
    @editor_ns.expect(editor_input_model)
    def put(self,editor_id):
        upd_editor = Editor(editor_id=editor_id,name = editor_ns.payload["name"],address=editor_ns.payload["address"])
        return Agency.get_instance().update_editor(upd_editor,editor_id)