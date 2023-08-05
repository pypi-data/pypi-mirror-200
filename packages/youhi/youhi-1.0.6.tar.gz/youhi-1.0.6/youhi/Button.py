# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional)

- text (string; default 'Submit')

- type (boolean | number | string | dict | list; default 'button')"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'youhi'
    _type = 'Button'
    @_explicitize_args
    def __init__(self, children=None, text=Component.UNDEFINED, className=Component.UNDEFINED, type=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'text', 'type']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'text', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Button, self).__init__(children=children, **args)
