import json
from pydantic import BaseModel
from base64 import b64encode, b64decode


def __fill_class(model_json, model_class):
    fields = model_class.__fields__
    new_json = {}
    for key in model_json:
        # complex type in list
        if key in fields and issubclass(fields[key].type_, BaseModel) \
            and model_json[key] is not None and isinstance(model_json[key], list):
            new_json[key] = [__fill_class(m, fields[key].type_) for m in model_json[key]]

        elif key in fields and issubclass(fields[key].type_, BaseModel) \
            and model_json[key] is not None and not isinstance(fields[key], list):
            new_json[key] = __fill_class(model_json[key], fields[key].type_)

        elif key in fields:
            new_json[key] = model_json[key]

    return model_class(**new_json)
        


def serialize(model):
    if isinstance(model, list):
        model = [m.json().encode() for m in model]
        model = b'7SQXZMcEC*W7yOgv'.join(model)
        s = str(b64encode(model))
    else:
        s = str(b64encode(model.json().encode()))
    return s[2:-1]



def deserialize(s, model_class=None):
    s = f"b'{s}'"
    model_byte = b64decode(eval(s))
    model_byte_list = model_byte.split(b'7SQXZMcEC*W7yOgv')
    if len(model_byte_list)>1:
        model_json = [json.loads(m) for m in model_byte_list]
    else:
        model_json = json.loads(model_byte_list[0])
    if model_class and isinstance(model_json, list):
        return [__fill_class(m, model_class) for m in model_json]
    elif model_class:
        return __fill_class(model_json, model_class)
    return model_json