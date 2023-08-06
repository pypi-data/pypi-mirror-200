import typing as t
import functools
import pydantic
import flask
import ujson
import functions_framework


_ENTRY_FUNC = t.Callable[[flask.Request], t.Any]
_T_MODEL = t.TypeVar('_T_MODEL', bound=pydantic.BaseModel)
_INPUT_SOURCE = '__input_source__'

class _ConvertableDict(dict):
    _input_source_label: str = None
    
    def to(self, model: t.Type[_T_MODEL]) -> _T_MODEL:
        try:
            return model.parse_obj(self)
        except pydantic.ValidationError as e:
            setattr(e, _INPUT_SOURCE, self._input_source_label)
            raise

class Request(flask.Request):
    @property
    def json(self) -> _ConvertableDict:
        d = _ConvertableDict(super().json)
        d._input_source_label = 'json payload'
        return d
    
    @property
    def args(self) -> _ConvertableDict:
        d = _ConvertableDict(super().args)
        d._input_source_label = 'query params'
        return d

def _get_request_from_cf_func(*args, func: _ENTRY_FUNC) -> flask.Request:
    request: flask.Request = (args or (None,))[0]
    if not isinstance(request, flask.Request):
        raise RuntimeError(f'{func.__name__} is not valid CF entrypoint')
    return request

def _to_flask_response(obj: t.Any):
    if obj is None:
        return ''

    if isinstance(obj, (dict, list, tuple)):
        return flask.jsonify(obj)

    if isinstance(obj, pydantic.BaseModel):
       return flask.jsonify(ujson.loads(obj.json()))

    return obj

def error_response(*, message: str, errors: t.Any, status_code: int):
    return flask.jsonify(dict(
        message = message, 
        errors = errors if type(errors) is list else [errors]
    )), status_code

def safe_return(func: _ENTRY_FUNC):
    @functools.wraps(func)
    def wrapper(*args):
        request: flask.Request = _get_request_from_cf_func(*args, func=func)
        return_val = func(request)
        status_code = None
        
        if type(return_val) is tuple and type(return_val[1]) is int:
            return_val, status_code = return_val

        response = _to_flask_response(return_val)

        if status_code:
            return response, status_code
        return response
    return wrapper

def entry_point(func: _ENTRY_FUNC):
    func = functions_framework.http(func)
    func = safe_return(func)

    @functools.wraps(func)
    def wrapper(*args):
        request = _get_request_from_cf_func(*args, func=func)
        request.__class__ = Request
        
        try:
            return func(request)
        except pydantic.ValidationError as e:
            if hasattr(e, _INPUT_SOURCE):
                input_source: str = getattr(e, _INPUT_SOURCE)
                return error_response(message=f'Invalid {input_source}', errors=e.errors(), status_code=400)
            raise

    return wrapper

def api_key_auth(allowed_api_key: str, api_key_query_param_name: str = 'api_key'):
    def decorator(func: _ENTRY_FUNC):
        @functools.wraps(func)
        def wrapper(*args):
            request: flask.Request = _get_request_from_cf_func(*args, func=func)
            api_key = request.args.get(api_key_query_param_name)
            
            if api_key != allowed_api_key:
                return error_response(message='Forbidden', errors='Invalid API key', status_code=403)
            
            return func(request)

        return wrapper
    return decorator
