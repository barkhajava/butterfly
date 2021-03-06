from tornado.web import RequestHandler
from urllib.error import HTTPError
import tifffile
import numpy as np
import io
import zlib
import json
import cv2

from bfly.logic import settings


class RestAPIHandler(RequestHandler):
    '''Request handler for the documented public Butterfly REST API'''

    # Query params
    #
    Q_EXPERIMENT = "experiment"
    Q_SAMPLE = "sample"
    Q_DATASET = "dataset"
    Q_CHANNEL = "channel"
    '''Encode image/mask in this image format (e.g. "tif")'''
    Q_FORMAT = "format"
    Q_VIEW = "view"
    Q_X = "x"
    Q_Y = "y"
    Q_Z = "z"
    Q_WIDTH = "width"
    Q_HEIGHT = "height"
    Q_RESOLUTION = "resolution"
    #
    # Hierarchy of data organization in config file
    #
    EXPERIMENTS = "experiments"
    SAMPLES = "samples"
    DATASETS = "datasets"
    CHANNELS = "channels"

    NAME = "name"
    PATH = "path"
    SHORT_DESCRIPTION = "short-description"
    DATA_TYPE = "data-type"
    DIMENSIONS = "dimensions"
    X = "x"
    Y = "y"
    Z = "z"

    def initialize(self, core):
        '''Override of RequestHandler.initialize

        Initializes the RestAPI request handler

        :param core: the butterfly.core instance used to fetch images
        '''
        self.core = core

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET')

    def get(self, command):
        '''Handle an HTTP GET request'''

       # rh_logger.logger.report_event("GET " + self.request.uri)
        try:
            if command == "experiments":
                result = self.get_experiments()
            elif command == "samples":
                result = self.get_samples()
            elif command == "datasets":
                result = self.get_datasets()
            elif command == "channels":
                result = self.get_channels()
            elif command == "channel_metadata":
                result = self.get_channel_metadata()
            elif command == "data":
                self.get_data()
                return
            elif command == "mask":
                self.get_mask()
                return
            else:
                raise HTTPError(self.request.uri, 400,
                                "Unsupported command: " + command,
                                [], None)
            data = json.dumps(result)
            self.set_header("Content-Type", "application/json")
            self.write(data)
        except HTTPError as http_error:
            self.set_status(http_error.code)
            self.set_header('Content-Type', "text/plain")
            self.write(http_error.msg)

    def _get_config(self,kind):
        '''Get the config dictionary for a named kind'''
        target = self._get_necessary_param(kind['param'])
        for d in kind['parent'].get(kind['plural'],[]):
            if d[self.NAME] == target:
                return d
        else:
            msg = 'Unknown '+kind['name']+': '+ target
          #  rh_logger.logger.report_event(msg)
            raise HTTPError(self.request.uri, 400, msg, [], None)

    def get_experiments(self):
        '''Handle the /api/experiments GET request'''
        experiments = settings.BFLY_CONFIG.get(self.EXPERIMENTS, [])
        return [_[self.NAME] for _ in experiments]

    def _get_experiment_config(self):
        return self._get_config({
            'parent': settings.BFLY_CONFIG,
            'plural': self.EXPERIMENTS,
            'param': self.Q_EXPERIMENT,
            'name': 'experiment name'
        })

    def get_samples(self):
        '''Handle the /api/samples GET request'''
        experiment = self._get_experiment_config()
        return [_[self.NAME] for _ in experiment.get(self.SAMPLES, [])]

    def _get_sample_config(self):
        return self._get_config({
            'parent': self._get_experiment_config(),
            'plural': self.SAMPLES,
            'param': self.Q_SAMPLE,
            'name': 'sample name'
        })

    def get_datasets(self):
        '''Handle the /api/datasets GET request'''
        sample = self._get_sample_config()
        return [_[self.NAME] for _ in sample.get(self.DATASETS, [])]

    def _get_dataset_config(self):
        return self._get_config({
            'parent': self._get_sample_config(),
            'plural': self.DATASETS,
            'param': self.Q_DATASET,
            'name': 'dataset name'
        })

    def get_channels(self):
        '''Handle the /api/channels GET request'''
        dataset = self._get_dataset_config()
        return [_[self.NAME] for _ in dataset.get(self.CHANNELS, [])]

    def _get_channel_config(self):
        return self._get_config({
            'parent': self._get_dataset_config(),
            'plural': self.CHANNELS,
            'param': self.Q_CHANNEL,
            'name': 'channel'
        })

    def get_channel_metadata(self):
        '''Handle the /api/channel_metadata GET request'''
        channel = self._get_channel_config().copy()
        # if self.PATH in channel:
        #     del channel[self.PATH]
        return channel

    def _except(self,kwargs):
    #    rh_logger.logger.report_event(kwargs['msg'])
        raise HTTPError(self.request.uri, 400, kwargs['msg'], [], None)

    def _match_condition(self,result,kwargs):
        if kwargs['condition']: self._except(kwargs)
        return result

    def _try_condition(self,result,kwargs):
        try: return kwargs['condition'](result)
        except: self._except(kwargs)

    def _try_typecast_int(self,qparam,result):
        return self._try_condition(result, {
            'condition' : int,
            'msg' : "Received non-integer %s: %s" % (qparam, result)
        })

    def _get_necessary_param(self, qparam):
        result = self.get_query_argument(qparam, default=None)
        return self._match_condition(result, {
            'condition' : result is None,
            'msg' : "Missing %s parameter" % qparam
        })

    def _get_list_query_argument(self, qparam, default, whitelist):
        result = self.get_query_argument(qparam, default)
        return self._match_condition(result, {
            'condition': result not in whitelist,
            'msg': "The %s must be one of %s." % (qparam, whitelist)
        })

    def _get_int_necessary_param(self, qparam):
        result = self._get_necessary_param(qparam)
        return self._try_typecast_int(qparam, result)

    def _get_int_query_argument(self, qparam):
        result = self.get_query_argument(qparam, 0)
        return self._try_typecast_int(qparam, result)

    def get_data(self):
        channel = self._get_channel_config()
        dtype = channel[self.DATA_TYPE]

        defaultFormat = settings.DEFAULT_OUTPUT
        defaultView = settings.DEFAULT_VIEW
        views = settings.SUPPORTED_IMAGE_VIEWS
        formats = settings.SUPPORTED_IMAGE_FORMATS

        fmt = self._get_list_query_argument(self.Q_FORMAT, defaultFormat, formats)
        if 'float' not in dtype and 'uint8' not in dtype:
            if fmt in ['png']:
                defaultView = 'colormap'

        x = self._get_int_necessary_param(self.Q_X)
        y = self._get_int_necessary_param(self.Q_Y)
        z = self._get_int_necessary_param(self.Q_Z)
        width = self._get_int_necessary_param(self.Q_WIDTH)
        height = self._get_int_necessary_param(self.Q_HEIGHT)
        resolution = self._get_int_query_argument(self.Q_RESOLUTION)
        view = self._get_list_query_argument(self.Q_VIEW, defaultView, views)

        slice_define = [channel[self.PATH], [x, y, z], [width, height, 1]]
    #    rh_logger.logger.report_event("Encoding image as dtype %s" % repr(dtype))
        vol = self.core.get(*slice_define, w=resolution, view=view)
        self.set_header("Content-Type", "image/"+fmt)
        if fmt in ['zip']:
            output = io.StringIO()
            volstring = vol[:,:,0].T.astype(np.uint32).tostring('F')
            output.write(zlib.compress(volstring))
            content = output.getvalue()
        elif fmt in ['tif','tiff']:
            output = io.StringIO()
            tiffvol = vol[:,:,0].astype(np.uint32)
            tifffile.imsave(output, tiffvol)
            content = output.getvalue()
        else:
            if vol.dtype.itemsize == 4:
                vol = vol.view(np.uint8).reshape(vol.shape[0], vol.shape[1], 4)
            content = cv2.imencode(  "." + fmt, vol)[1].tostring()

        self.write(content)

    def get_mask(self):
        # TODO: implement this
        raise HTTPError(self.request.uri, 501, "The server does not yet support /api/mask requests", [], None)
