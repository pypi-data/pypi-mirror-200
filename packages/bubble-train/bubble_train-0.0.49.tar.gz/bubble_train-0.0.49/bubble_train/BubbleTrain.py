# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class BubbleTrain(Component):
    """A BubbleTrain component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional)

- id (string; optional)

- height (string; default '100%')

- overflow (string; default 'auto')

- path_list (list of boolean | number | string | dict | lists; optional)

- position (string; default 'absolute')

- width (string; default '100%')"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'bubble_train'
    _type = 'BubbleTrain'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, overflow=Component.UNDEFINED, position=Component.UNDEFINED, path_list=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'height', 'overflow', 'path_list', 'position', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'height', 'overflow', 'path_list', 'position', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(BubbleTrain, self).__init__(children=children, **args)
