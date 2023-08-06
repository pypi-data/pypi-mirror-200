# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DraggablePanel(Component):
    """A DraggablePanel component.


Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional)

- id (string; required)

- cnt_h (string | number; default '100%')

- cnt_overflow (string; default "auto")

- color (string; default "#ccc")

- cx0 (number; default 0)

- cy0 (number; default 0)

- edge_offset_x (number; default 0)

- edge_offset_y (number; default 20)

- ftr_color (string; default "white")

- ftr_count (number; default 0)

- ftr_h (string | number; default 0)

- hdr_h (string | number; default 20)

- height (string; default '100px')

- in_dot_distance (number; default 20)

- in_dot_offset (number; default 10)

- input_ids (list of strings; optional)

- left (string; default '50px')

- out_dot_distance (number; default 20)

- out_dot_offset (number; default 10)

- output_ids (list of strings; optional)

- output_target_lists (list of list of stringss; optional)

- output_target_pl_lists (list of list of list of list of numberssss; optional)

- parent_id (string; optional)

- strokeWidth (string; default "1.5")

- title (string; default "")

- title_color (string; default "white")

- title_font (string; default "sans-serif")

- title_size (string | number; default "10px")

- tooltip (string; default "")

- top (string; default '50px')

- ttr_color (string; default "white")

- ttr_count (number; default 0)

- ttr_h (string | number; default 0)

- width (string; default '100px')

- x0 (number; default 0)

- y0 (number; default 0)

- z_index (number; default 9)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'bubble_train'
    _type = 'DraggablePanel'
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, ttr_count=Component.UNDEFINED, ftr_count=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, left=Component.UNDEFINED, top=Component.UNDEFINED, cx0=Component.UNDEFINED, cy0=Component.UNDEFINED, x0=Component.UNDEFINED, y0=Component.UNDEFINED, cnt_h=Component.UNDEFINED, hdr_h=Component.UNDEFINED, ttr_h=Component.UNDEFINED, ftr_h=Component.UNDEFINED, input_ids=Component.UNDEFINED, output_ids=Component.UNDEFINED, output_target_lists=Component.UNDEFINED, output_target_pl_lists=Component.UNDEFINED, in_dot_offset=Component.UNDEFINED, in_dot_distance=Component.UNDEFINED, out_dot_offset=Component.UNDEFINED, out_dot_distance=Component.UNDEFINED, edge_offset_y=Component.UNDEFINED, edge_offset_x=Component.UNDEFINED, tooltip=Component.UNDEFINED, strokeWidth=Component.UNDEFINED, color=Component.UNDEFINED, ftr_color=Component.UNDEFINED, ttr_color=Component.UNDEFINED, z_index=Component.UNDEFINED, cnt_overflow=Component.UNDEFINED, title=Component.UNDEFINED, title_font=Component.UNDEFINED, title_size=Component.UNDEFINED, title_color=Component.UNDEFINED, parent_id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'cnt_h', 'cnt_overflow', 'color', 'cx0', 'cy0', 'edge_offset_x', 'edge_offset_y', 'ftr_color', 'ftr_count', 'ftr_h', 'hdr_h', 'height', 'in_dot_distance', 'in_dot_offset', 'input_ids', 'left', 'out_dot_distance', 'out_dot_offset', 'output_ids', 'output_target_lists', 'output_target_pl_lists', 'parent_id', 'strokeWidth', 'title', 'title_color', 'title_font', 'title_size', 'tooltip', 'top', 'ttr_color', 'ttr_count', 'ttr_h', 'width', 'x0', 'y0', 'z_index']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'cnt_h', 'cnt_overflow', 'color', 'cx0', 'cy0', 'edge_offset_x', 'edge_offset_y', 'ftr_color', 'ftr_count', 'ftr_h', 'hdr_h', 'height', 'in_dot_distance', 'in_dot_offset', 'input_ids', 'left', 'out_dot_distance', 'out_dot_offset', 'output_ids', 'output_target_lists', 'output_target_pl_lists', 'parent_id', 'strokeWidth', 'title', 'title_color', 'title_font', 'title_size', 'tooltip', 'top', 'ttr_color', 'ttr_count', 'ttr_h', 'width', 'x0', 'y0', 'z_index']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DraggablePanel, self).__init__(children=children, **args)
