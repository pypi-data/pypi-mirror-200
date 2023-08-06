from slugify import slugify


def slugify_object_keys(obj, **kwargs):
    kwargs['separator'] = kwargs.get('separator', '_')
    kwargs['lowercase'] = kwargs.get('lowercase', False)

    def inner_func(data):        
        if isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                new_key = slugify(key, **kwargs)
                new_value = inner_func(value)
                new_data[new_key] = new_value
            return new_data
        elif isinstance(data, list):
            return [inner_func(item) for item in data]
        else:
            return data

    return inner_func(obj)
