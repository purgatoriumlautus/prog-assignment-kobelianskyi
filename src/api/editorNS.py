from flask import jsonify
from flask_restx import Namespace, Resource, fields,abort

from time import time_ns
from ..model.agency import Agency


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
editor_model = editor_info_model = editor_ns.model('EditorModel',{
    'editor_id': fields.Integer(help = 'Unique id of the editor'),
    'name': fields.String(help = "Name of the editor"),
    'address': fields.String(help="address of living of the editor"),
    })

editor_info_model = editor_ns.model('EditorInfoModel',{
    'editor_id': fields.Integer(help = 'Unique id of the editor'),
    'name': fields.String(help = "Name of the editor"),
    'address': fields.String(help="address of living of the editor"),
    'newspapers': fields.List(fields.Nested(paper_model,required = False, help="All issues of a particular pages")),
    'issues': fields.List(fields.Nested(issue_model))
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
        status = Agency.get_instance().add_editor(editor)
        if status:
            return status
        else:
            abort(422,{"error":"id was already occupied"})

    @editor_ns.marshal_list_with(editor_model)
    def get(self):
        return Agency.get_instance().get_editors()

@editor_ns.route("/<int:editor_id>")
class EditorId(Resource):
    
    @editor_ns.marshal_with(editor_info_model)
    def get(self,editor_id):
        editor = Agency.get_instance().get_editor(editor_id)
        if editor:
            return editor
        else:
            abort(422,{"error":"id is not correct"})

    @editor_ns.marshal_with(editor_model)
    @editor_ns.expect(editor_input_model)
    def post(self,editor_id):
        upd_editor = Editor(editor_id=editor_id,name = editor_ns.payload["name"],address=editor_ns.payload["address"])
        status = Agency.get_instance().update_editor(upd_editor,editor_id)
        if status:
            return status
        else:
            abort(422,{"error":"id is not correct"})
    

    # @editor_ns.marshal_with(editor_model)
    def delete(self,editor_id):
        editor = Agency.get_instance().get_editor(editor_id)
        if editor:
            Agency.get_instance().delete_editor(editor_id)
            return jsonify(f"Editor {editor.name} with id {editor_id} was successfully fired!")
        else:
            return jsonify(f"Editor wasn't found")
    
@editor_ns.route("/<int:editor_id>/issues")
class EditorIssues(Resource):
    @editor_ns.marshal_list_with(issue_model)
    def get(self,editor_id):
        issues = Agency.get_instance().get_editor_issues(editor_id)
        if issues:
            return issues
        else:
            abort(422,{"error":"id is not correct"})