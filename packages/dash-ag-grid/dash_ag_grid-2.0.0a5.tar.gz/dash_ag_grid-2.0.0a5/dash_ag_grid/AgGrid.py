# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AgGrid(Component):
    """An AgGrid component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- autoSizeAllColumns (dict; default False):
    Set to True to autosize all columns, considering both headers and
    data Or pass an object of options for how to autosize. Currently
    supports `skipHeaders`, set this True to only consider data when
    autosizing.

    `autoSizeAllColumns` is a boolean | dict with keys:

    - skipHeaders (boolean; optional)

- cellClicked (dict; optional):
    Cell is clicked.

    `cellClicked` is a dict with keys:

    - colId (boolean | number | string | dict | list; optional):
        column where the cell was clicked.

    - rowId (boolean | number | string | dict | list; optional):
        Row Id from the grid, this could be a number automatically, or
        set via getRowId.

    - rowIndex (number; optional):
        rowIndex, typically a row number.

    - timestamp (boolean | number | string | dict | list; optional):
        timestamp of last action.

    - value (boolean | number | string | dict | list; optional):
        value of the clicked cell.

- cellRendererData (dict; optional):
    Special prop to allow feedback from cell renderer to the grid.

    `cellRendererData` is a dict with keys:

    - colId (string; optional):
        Column ID from where the event was fired.

    - rowId (boolean | number | string | dict | list; optional):
        Row Id from the grid, this could be a number automatically, or
        set via getRowId.

    - rowIndex (number; optional):
        Row Index from the grid, this is associated with the row
        count.

    - timestamp (boolean | number | string | dict | list; optional):
        Timestamp of when the event was fired.

    - value (boolean | number | string | dict | list; optional):
        Value set from the function.

- cellValueChanged (dict; optional):
    Value has changed after editing.

    `cellValueChanged` is a dict with keys:

    - colId (boolean | number | string | dict | list; optional):
        column where the cell was changed.

    - data (dict; optional):
        data, data object from the row.

    - newValue (boolean | number | string | dict | list; optional):
        new value of the cell.

    - oldValue (boolean | number | string | dict | list; optional):
        old value of the cell.

    - rowId (boolean | number | string | dict | list; optional):
        Row Id from the grid, this could be a number automatically, or
        set via getRowId.

    - rowIndex (number; optional):
        rowIndex, typically a row number.

- className (string; default 'ag-theme-alpine'):
    The class for the ag-grid.  Can specify the ag-grid theme here.

- columnDefs (list of dicts; optional):
    Array of Column Definitions.

- columnSize (a value equal to: 'sizeToFit', 'autoSizeAll', null; optional):
    Size the columns autoSizeAll changes the column sizes to fit the
    column's content, sizeToFit changes the column sizes to fit the
    width of the table and None bypasses the altering of the column
    widths.

- columnState (list; optional):
    Current state of the columns.

- csvExportParams (dict; optional):
    Object with properties to pass to the exportDataAsCsv() method.

    `csvExportParams` is a dict with keys:

    - allColumns (boolean; optional):
        If True, all columns will be exported in the order they appear
        in the columnDefs.

    - appendContent (string; optional):
        Content to put at the bottom of the file export.

    - columnKeys (list of strings; optional):
        Provide a list (an array) of column keys or Column objects if
        you want to export specific columns.

    - columnSeparator (string; optional):
        Delimiter to insert between cell values.

    - fileName (string; optional):
        String to use as the file name.

    - onlySelected (boolean; optional):
        Export only selected rows.

    - onlySelectedAllPages (boolean; optional):
        Only export selected rows including other pages (only makes
        sense when using pagination).

    - prependContent (string; optional):
        Content to put at the top of the file export. A 2D array of
        CsvCell objects.

    - skipColumnGroupHeaders (boolean; optional):
        Set to True to skip include header column groups.

    - skipColumnHeaders (boolean; optional):
        Set to True if you don't want to export column headers.

    - skipPinnedBottom (boolean; optional):
        Set to True to suppress exporting rows pinned to the bottom of
        the grid.

    - skipPinnedTop (boolean; optional):
        Set to True to suppress exporting rows pinned to the top of
        the grid.

    - skipRowGroups (boolean; optional):
        Set to True to skip row group headers if grouping rows. Only
        relevant when grouping rows.

    - suppressQuotes (boolean; optional):
        Pass True to insert the value into the CSV file without
        escaping. In this case it is your responsibility to ensure
        that no cells contain the columnSeparator character.

- dangerously_allow_code (boolean; default False):
    Allow strings containing JavaScript code or HTML in certain props.
    If your app stores Dash layouts for later retrieval this is
    dangerous because it can lead to cross-site-scripting attacks.

- dashGridOptions (dict; optional):
    Other ag-grid options.

- defaultColDef (dict; optional):
    A default column definition.

- deleteSelectedRows (boolean; optional):
    If True, the internal method deleteSelectedRows() will be called.

- deselectAll (boolean; default False):
    If True, the internal method deselectAll() will be called.

- detailCellRendererParams (dict; optional):
    Specifies the params to be used by the default detail Cell
    Renderer. See Detail Grids.

    `detailCellRendererParams` is a dict with keys:

    - detailColName (string; optional):
        Column name where detail grid data is located in main dataset,
        for master-detail view.

    - detailGridOptions (boolean | number | string | dict | list; optional):
        Grid options for detail grid in master-detail view.

    - suppressCallback (boolean; optional):
        Default: True. If True, suppresses the Dash callback in favor
        of using the data embedded in rowData at the given
        detailColName.

- enableEnterpriseModules (boolean; default False):
    If True, enable ag-grid Enterprise modules. Recommended to use
    with licenseKey.

- exportDataAsCsv (boolean; default False):
    If True, the internal method exportDataAsCsv() will be called.

- filterModel (dict; optional):
    If filtering client-side rowModel, what the filter model is.
    Passing a model back to this prop will apply it to the grid.

- getDetailRequest (dict; optional):
    Request from Dash AgGrid when suppressCallback is disabled and a
    user opens a row with a detail grid.

    `getDetailRequest` is a dict with keys:

    - data (boolean | number | string | dict | list; optional):
        Details about the row that was opened.

    - requestTime (boolean | number | string | dict | list; optional):
        Datetime representing when the grid was requested.

- getDetailResponse (list of dicts; optional):
    RowData to populate the detail grid when callbacks are used to
    populate.

- getRowId (string; optional):
    This is required for change detection in rowData.

- getRowStyle (dict; optional):
    Object used to perform the row styling. See AG-Grid Row Style.

    `getRowStyle` is a dict with keys:

    - defaultStyle (dict; optional)

    - styleConditions (list of dicts; optional)

        `styleConditions` is a list of dicts with keys:

        - condition (string; required)

        - style (dict; required)

- getRowsRequest (dict; optional):
    Infinite Scroll, Datasource interface See
    https://www.ag-grid.com/react-grid/infinite-scrolling/#datasource-interface.

    `getRowsRequest` is a dict with keys:

    - context (boolean | number | string | dict | list; optional):
        The grid context object.

    - endRow (number; optional):
        The first row index to NOT get.

    - failCallback (optional):
        Callback to call when the request fails.

    - filterModel (dict; optional):
        If filtering, what the filter model is.

    - sortModel (list of dicts; optional):
        If sorting, what the sort model is.

    - startRow (number; optional):
        The first row index to get.

    - successCallback (optional):
        Callback to call when the request is successful.

- getRowsResponse (dict; optional):
    Serverside model data response object. See
    https://www.ag-grid.com/react-grid/server-side-model-datasource/.

    `getRowsResponse` is a dict with keys:

    - rowCount (number; optional):
        Current row count, if known.

    - rowData (list of dicts; optional):
        Data retreived from the server.

    - storeInfo (boolean | number | string | dict | list; optional):
        Any extra info for the grid to associate with this load.

- licenseKey (string; optional):
    License key for ag-grid enterprise. If using Enterprise modules,
    enableEnterpriseModules must also be True.

- masterDetail (boolean; optional):
    Used to enable Master Detail. See Enabling Master Detail. Default
    Value: False.

- persisted_props (list of strings; default ['selectedRows']):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (boolean | string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- resetColumnState (boolean; default False):
    If True, the internal method resetColumnState() will be called.

- rowClass (string; optional):
    The class to give a particular row. See Row Class.

- rowClassRules (dict; optional):
    Rules which can be applied to include certain CSS classes. See Row
    Class Rules.

- rowData (list of dicts; optional):
    (Client-Side Row Model only) Set the data to be displayed as rows
    in the grid.

- rowModelType (a value equal to: 'clientSide', 'infinite', 'viewport', 'serverSide'; default 'clientSide'):
    Sets the Row Model type. Default Value: 'clientSide'.

- rowStyle (dict; optional):
    The style to give a particular row. See Row Style.

- rowTransaction (dict; optional):
    If True, the internal method rowTransaction() will be used, if
    async provided as False, applyTransaction() will be called, else
    applyTransactionAsync().

    `rowTransaction` is a dict with keys:

    - add (list; optional)

    - addIndex (number; optional)

    - async (boolean; optional)

    - remove (list; optional)

    - update (list; optional)

- selectAll (dict; default False):
    Set to True to cause all rows to be selected, Or pass an object of
    options for which rows to select. Currently supports `filtered`,
    set to True to only select filtered rows.

    `selectAll` is a boolean | dict with keys:

    - filtered (boolean; optional)

- selectedRows (list of dicts; optional):
    The actively selected rows from the grid (may include filtered
    rows).

- style (dict; default {height: '400px', width: '100%'}):
    The CSS style for the component.

- suppressDragLeaveHidesColumns (boolean; default True):
    If True, when you drag a column out of the grid (e.g. to the group
    zone) the column is not hidden. Default Value: False.

- updateColumnState (boolean; default False):
    If True, the internal method updateColumnState() will be called.

- virtualRowData (list of dicts; optional):
    The rowData in the grid after inline filters are applied."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_ag_grid'
    _type = 'AgGrid'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, dangerously_allow_code=Component.UNDEFINED, resetColumnState=Component.UNDEFINED, exportDataAsCsv=Component.UNDEFINED, selectAll=Component.UNDEFINED, deselectAll=Component.UNDEFINED, autoSizeAllColumns=Component.UNDEFINED, updateColumnState=Component.UNDEFINED, deleteSelectedRows=Component.UNDEFINED, rowTransaction=Component.UNDEFINED, getRowId=Component.UNDEFINED, columnState=Component.UNDEFINED, csvExportParams=Component.UNDEFINED, columnSize=Component.UNDEFINED, getRowStyle=Component.UNDEFINED, getRowsRequest=Component.UNDEFINED, filterModel=Component.UNDEFINED, getDetailRequest=Component.UNDEFINED, getDetailResponse=Component.UNDEFINED, cellRendererData=Component.UNDEFINED, getRowsResponse=Component.UNDEFINED, licenseKey=Component.UNDEFINED, enableEnterpriseModules=Component.UNDEFINED, virtualRowData=Component.UNDEFINED, columnDefs=Component.UNDEFINED, defaultColDef=Component.UNDEFINED, rowModelType=Component.UNDEFINED, rowData=Component.UNDEFINED, masterDetail=Component.UNDEFINED, detailCellRendererParams=Component.UNDEFINED, rowStyle=Component.UNDEFINED, rowClass=Component.UNDEFINED, rowClassRules=Component.UNDEFINED, suppressDragLeaveHidesColumns=Component.UNDEFINED, cellClicked=Component.UNDEFINED, selectedRows=Component.UNDEFINED, cellValueChanged=Component.UNDEFINED, dashGridOptions=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'autoSizeAllColumns', 'cellClicked', 'cellRendererData', 'cellValueChanged', 'className', 'columnDefs', 'columnSize', 'columnState', 'csvExportParams', 'dangerously_allow_code', 'dashGridOptions', 'defaultColDef', 'deleteSelectedRows', 'deselectAll', 'detailCellRendererParams', 'enableEnterpriseModules', 'exportDataAsCsv', 'filterModel', 'getDetailRequest', 'getDetailResponse', 'getRowId', 'getRowStyle', 'getRowsRequest', 'getRowsResponse', 'licenseKey', 'masterDetail', 'persisted_props', 'persistence', 'persistence_type', 'resetColumnState', 'rowClass', 'rowClassRules', 'rowData', 'rowModelType', 'rowStyle', 'rowTransaction', 'selectAll', 'selectedRows', 'style', 'suppressDragLeaveHidesColumns', 'updateColumnState', 'virtualRowData']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'autoSizeAllColumns', 'cellClicked', 'cellRendererData', 'cellValueChanged', 'className', 'columnDefs', 'columnSize', 'columnState', 'csvExportParams', 'dangerously_allow_code', 'dashGridOptions', 'defaultColDef', 'deleteSelectedRows', 'deselectAll', 'detailCellRendererParams', 'enableEnterpriseModules', 'exportDataAsCsv', 'filterModel', 'getDetailRequest', 'getDetailResponse', 'getRowId', 'getRowStyle', 'getRowsRequest', 'getRowsResponse', 'licenseKey', 'masterDetail', 'persisted_props', 'persistence', 'persistence_type', 'resetColumnState', 'rowClass', 'rowClassRules', 'rowData', 'rowModelType', 'rowStyle', 'rowTransaction', 'selectAll', 'selectedRows', 'style', 'suppressDragLeaveHidesColumns', 'updateColumnState', 'virtualRowData']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AgGrid, self).__init__(**args)
