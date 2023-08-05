
from copy import deepcopy
from .stencils import get_list_of_stencils
from .database import DeviceData, CableMatrixData
from .entities import ItemObjects, Connectors
from .visio import VisioObject
from .gui import UserForm


# ------------------------------------------------------------------------- 
# ## DICTIONARY - DEFAULT INPUTS 
# ------------------------------------------------------------------------- 

DEFAULT_DIC = {

	# Optional
	'default_stencil': None,
	'op_file': 'None',										# some visio versions doesn't support file save.

	# Optional / edit only if differ from actual database
	'devices_sheet_name': 'Devices',
	'x-coordinates_col': 'x-axis',
	'y-coordinates_col': 'y-axis',
	'stencils_col': 'stencils',
	'device_type_col': 'device_type',

	# Optional / edit only if differ from actual database
	'cabling_sheet_name': 'Cablings',
	'a_device_col': 'a_device',
	'a_device_port_col': 'a_device_port',
	'b_device_col': 'b_device',
	'color_col': 'color',
	'connector_type_col': 'connector_type',
	'weight_col': 'weight',
	'pattern_col': 'pattern',


	# Optional /  if differ from actual database
	'cols_to_merge': [],									## add manually if any more..
	'filter_on_cable': True,
	'filter_on_include_col': False,
	'is_sheet_filter': False,

	'sheet_filters': { }
}


# ------------------------------------------------------------------------- 
# ## pyvig boiler plate code.
# ------------------------------------------------------------------------- 
def cabling_data_operations(dic):
	"""create and return cabling data object

	Args:
		dic (dict): cabling tab column names idenfier dictionary

	Returns:
		CableMatrixData: Cablings data object
	"""	
	cable_matrix_data = CableMatrixData(
		dic['data_file'],               # mandatory: file name (with full path)
		sheet_name=dic['cabling_sheet_name'],           # mandatory: tab/sheet name
		a_device_colname=dic['a_device_col'],           # mandatory: a side device of cable
		b_device_colname=dic['b_device_col'],           # mandatory: b side device of cable
		a_device_port_colname=dic['a_device_port_col'],
		connector_type_colname=dic['connector_type_col'],
		cable_color_colname=dic['color_col'],
		cable_weight_colname=dic['weight_col'],
		cable_line_pattern_colname=dic['pattern_col'],)

	return cable_matrix_data


def device_data_operations(dic):
	"""creates and returns devices data object after merging columns of the list provided for `cols_to_merge` key  

	Args:
		dic (dict): devices tab column names identifier dictionary.

	Returns:
		DeviceData: Devices data object
	"""	
	devices_data = DeviceData(
		dic['data_file'],
		sheet_name=dic['devices_sheet_name'],
		x=dic['x-coordinates_col'],
		y=dic['y-coordinates_col'],
		stencil_colname=dic['stencils_col'],
		device_type_colname=dic['device_type_col'],
		default_stencil=dic['default_stencil'], )

	devices_data.add_description(dic['cols_to_merge'])
	return devices_data

def visio_operations(dic, devices_data, cable_matrix_data, stencils):
	"""create a VisioObject

	Args:
		dic (dict): dictionary with sheet filters (if needed), for multi page output
		devices_data (DeviceData): Devices data object
		cable_matrix_data (CableMatrixData): Cablings data object
		stencils (list): list of visio stencils 

	Returns:
		None: None
	"""	
	with VisioObject(stencils=stencils, outputFile=dic['op_file']) as v:
		print("Visio Drawing Inprogress, Do not close Visio Drawing while its running...")
		if dic['sheet_filters']:
			for kv in dic['sheet_filters'].items():
				if isinstance(kv[1], str):
					repeat_for_filter(v, devices_data, cable_matrix_data, dic, kv[0], kv[1], kv[0])
				elif isinstance(kv[1], (list, tuple, set)):
					for _kv in kv[1]:
						repeat_for_filter(v, devices_data, cable_matrix_data, dic, kv[0], _kv, kv[0] + '_' + _kv)
		else:
			visio_page_operation(v, devices_data, cable_matrix_data, {}, dic)
	return None


def repeat_for_filter(v, devices_data, cable_matrix_data,
	dic, filt_key, filt_value, page_key):
	"""starts visio page operation for the given filter

	Args:
		v (VisioObject): Visio Object
		devices_data (DeviceData): Devices data object
		cable_matrix_data (CableMatrixData): Cablings data object
		dic (dict): input dictionary
		filt_key (str): filter key
		filt_value (str, tuple, list, set): filter value(s)
		page_key (str): page key (suffix for filter values in case if multiple filt_values)
	"""	
	flt ={filt_key:filt_value}
	cmd = deepcopy(cable_matrix_data)
	visio_page_operation(v, devices_data, cmd, flt, dic, page_key=page_key)


def visio_page_operation(v, devices_data, cable_matrix_data, flt, dic, page_key=None):
	"""operate on visio page

	Args:
		v (VisioObject): Visio Object
		devices_data (DeviceData): Devices data object
		cable_matrix_data (CableMatrixData): Cablings data object
		flt (dict): filters {key: value} pairs
		dic (dict): input dictionary
		page_key (str, optional): page key (suffix for filter values in case if multiple filt_values). Defaults to None.
	"""	
	if dic['filter_on_include_col']:
		cable_matrix_data.filter_eligible_cables_only() # [Optional]
	if dic['is_sheet_filter']:
		cable_matrix_data.filter(**flt)               # [Optional] column=records
	cable_matrix_data.calc_slop(devices_data)       # [Mandatory] calculate cable slop/angle
	if flt:
		v.insert_new_page(page_key)
	else:
		v.insert_new_page("PhysicalDrawing")
	item_objects = ItemObjects(v, devices_data, cable_matrix_data, filterOnCables=dic['filter_on_cable'])
	Connectors(cable_matrix_data, item_objects)
	v.fit_to_draw(item_objects.page_height, item_objects.page_width)


def pyVig(dic):
	"""main function starting the python based cli - visio generation

	Args:
		dic (dict): inputs dictionary ( valid and mandatory keys = stencil_folder, data_file ) (valid but optional keys = default_stencil, cols_to_merge, is_sheet_filter, sheet_filters ... and many more from DEFAULT_DIC )

	Returns:
		None: None
	"""	
	DEFAULT_DIC.update(dic)
	devices_data = device_data_operations(DEFAULT_DIC)
	cable_matrix_data = cabling_data_operations(DEFAULT_DIC)
	stencils = get_list_of_stencils(
		folder=DEFAULT_DIC['stencil_folder'],
		devices_data=devices_data,
	)
	visio_operations(DEFAULT_DIC, devices_data, cable_matrix_data, stencils)
	return None

def pyVig_gui():
	"""main function starting the gui input - visio generation

	Returns:
		None: None
	"""	
	u = UserForm()
	try: dic = u.dic
	except: return None
	devices_data = device_data_operations(dic)
	cable_matrix_data = cabling_data_operations(dic)
	stencils = get_list_of_stencils(
		folder=dic['stencil_folder'], 
		devices_data=devices_data, 
	)
	visio_operations(dic, devices_data, cable_matrix_data, stencils)
	return None


# ------------------------------------------------------------------------- 


