import flask
from flask.ext.classy import FlaskView, route, request
from annotator_supreme.models.bbox_model import BBox
from annotator_supreme.controllers.image_controller import ImageController
from annotator_supreme.views import view_tools
from annotator_supreme.views import error_views
import cv2

class AnnoView(FlaskView):
    route_base = '/'

    def __init__(self):
        self.controller = ImageController()

    @route('/image/anno/<dataset>/<imageid>', methods=['GET'])
    def get_image_anno(self, dataset, imageid):
        anno = self.controller.get_image_anno(dataset, imageid)
        anno_dict = view_tools.anno_to_dict(anno)

        return flask.jsonify(anno_dict)

    @route('/image/anno/<dataset>/<imageid>', methods=['POST'])
    def post_image_anno(self, dataset, imageid):
        (ok, error, anno) = view_tools.get_param_from_request(request, 'anno')

        try:
            bbs_vec = []
            for bb in anno:
                bbox_o = BBox(bb['top'], bb['left'], bb['bottom'], bb['right'], bb['labels'], bb['ignore'])
                bbs_vec.append(bbox_o)
        except BaseException as e:
            print('Problem with provided annotation', anno, str(e))
            return 'Problem with provided annotation',500

        self.controller.change_annotations(dataset, imageid, bbs_vec)

        return '', 200