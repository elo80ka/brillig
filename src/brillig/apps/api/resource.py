from django.utils.simplejson import dumps
from piston.resource import Resource as _Resource
from piston.emitters import Emitter
from piston.utils import rc

class Resource(_Resource):
    def form_validation_response(self, e):
        """Returns the validation errors as a JSON response.
        """
        resp = rc.BAD_REQUEST
        data = dict(
            (k, map(unicode, v))
            for (k, v) in e.form.errors.iteritems()
        )
        resp['Content-Type'] = 'application/json; charset=utf-8'
        resp.content = dumps(data)
        return resp
