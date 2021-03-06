import flask
from flask.ext.classy import FlaskView, route, request
from annotator_supreme.controllers.dataset_controller import DatasetController
from annotator_supreme.controllers.image_controller import ImageController
from annotator_supreme.views import view_tools
from annotator_supreme.views import error_views
import json

class DatasetView(FlaskView):
    route_base = '/'

    def __init__(self):
        self.controller = DatasetController()
        self.image_controller = ImageController()

    @route('/dataset/all', methods=['GET'])
    def get_all_datasets(self):
        obj = self.controller.get_datasets()
        return flask.jsonify({"datasets": obj})

    @route('/dataset/<dataset>', methods=['GET'])
    def get_dataset(self, dataset):
        # obj = self.image_controller.all_images(dataset)
    
        d = self.controller.get_dataset(dataset)
        if d == None:
            return "Dataset not found", 404
        else:
            return flask.jsonify({"dataset": d})



    @route('/dataset/<dataset>/size', methods=['GET'])
    def get_dataset_size(self, dataset):
        obj = self.image_controller.all_images(dataset)
        print("obj", obj)
        # return flask.jsonify({"dataset_size": len(obj)})
        print('returning', flask.jsonify({"dataset_size": len(obj)}))
        return flask.jsonify({"dataset_size": len(obj)})

    @route('/dataset/<dataset>', methods=['DELETE'])
    def delete_dataset(self, dataset):
        ok, error = self.controller.purge_dataset(dataset)
        if not ok:
            raise error_views.InvalidParametersError(error)
        else:
            return '', 200

    @route('/dataset/<dataset>/partition', methods=['POST'])
    def create_partition(self, dataset):
        (ok, error, partitions) = view_tools.get_param_from_request(request, "partitions")
        if not ok:
            raise error_views.InvalidParametersError(error)

        (ok, error, percentages) = view_tools.get_param_from_request(request, "percentages")
        if not ok:
            raise error_views.InvalidParametersError(error)

        (ok, error) = self.controller.set_partition(dataset, partitions, percentages)
        if not ok:
            raise error_views.InvalidParametersError(error)

        return '', 200

    @route('/dataset/create', methods=['POST'])
    def create_datasets(self):
        (ok, error, name) = view_tools.get_param_from_request(request, "name")
        if not ok:
            raise error_views.InvalidParametersError(error)

        (ok, error, tags) = view_tools.get_param_from_request(request, "tags")
        if not ok:
            raise error_views.InvalidParametersError(error)

        self.controller.create_dataset(name, tags)
        return flask.jsonify({"ok": "to-do"})

    