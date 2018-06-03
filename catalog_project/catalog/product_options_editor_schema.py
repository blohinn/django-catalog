from .models import OptionGroup


def get_product_option_json_editor_schema(widget):
    options = OptionGroup.objects.all()
    options_names = [o.name for o in options]

    _ = []
    for o in options:
        _.append('---{}---'.format(o.name.upper()))
        for v in o.values.all():
            _.append(v.name)

    schema = {
        "title": "Person",
        "type": "object",
        "properties": {
            "options": {
                "type": "array",
                "format": "table",
                "title": "Options",
                "uniqueItems": True,
                "items": {
                    "type": "object",
                    "title": "Option",
                    "properties": {
                        "option": {
                            "title": "Options",
                            "type": "string",
                            "enum": options_names
                        },
                        "values": {
                            "type": "array",
                            "format": "table",
                            "title": "Values",
                            "items": {
                                "type": "object",
                                "title": "Value",
                                "properties": {
                                    "value": {
                                        "title": "Value",
                                        "type": "string",
                                        "enum": _
                                    },
                                    "price_corrector": {
                                        "title": "Price Correction",
                                        "type": "number",
                                        "default": 0.0
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return schema