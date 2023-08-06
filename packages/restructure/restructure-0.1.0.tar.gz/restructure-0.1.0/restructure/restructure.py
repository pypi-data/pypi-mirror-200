from .locate import locate
from .merge import merge


def restructure(data: dict, specification: dict):
	"""Restructure data according to specification.

	A restructure specification is a map of keys "sources" to values "destinations", both in
	"key-path" format:

	A key-path is a dot-delimited string of keys e.g. 'key1.key2.key3', useful for indexing
	into nested dictionaries. For example, 'key1.key2.key3' is an index to 'value':

	data = {
		'key1': {
			'key2': {
				'key3': 'value'
			}
		}
	}

	In a restructure specification, both the keys and values are key-paths. The dictionary keys are
	the keys to be restructured (the "sources"), and the dictionary values are the new keys to use
	(the "destinations").

	So, for example, the restructure specification:

	spec = {
		'key1.key2.key3': 'key1.data',
	}

	Combined with the previous input data would result in a dictionary with the following structure:

	output = {
		'key1': {
			'data': 'value'
		}
	}

	Destinations can also be sets of key-paths, in which case the source value will be copied to
	all destinations. For example:

	data = {
		'key1': {
			'key2': {
				'key3': 'value1',
			}
		}
	}
	spec = {
		'key1.key2.key3': {'key1.key2.key3.key4', 'key1.key2.key5', 'key1.key6', 'key7'},
	}
	output = {
		'key1': {
			'key2': {
				'key3': {
					'key4': 'value1',
				},
				'key5': 'value1',
			},
			'key6': 'value1',
		},
		'key7': 'value1',
	}

	:param data: Data to restructure.
	:param specification: Specification of restructuring operations to perform.
	"""
	output = {}

	for source, destination in specification.items():
		source_parent, source_key = locate(source, data)
		targets = set()

		if isinstance(destination, set):
			targets = destination
		else:
			targets.add(destination)

		err_msg = f'Conflicting restructure destinations for source: {source}!'

		for target in targets:
			try:
				destination_parent, destination_key = locate(target, output, make_keys=True)

				if destination_key in destination_parent:
					# if the destination key already exists, it must be because another operation
					# put a value there i.e. a conflicting destination
					raise KeyError(err_msg)

				destination_parent[destination_key] = source_parent[source_key]
			except TypeError:
				# raised by locate() when a destination_parent is not a dict
				# if destination_parent is not a dict, it must be because another operation
				# put a value there i.e. a conflicting destination
				raise KeyError(err_msg)

	# Remove reorder sources from data
	ignore = set(specification.keys())
	data = merge(data, {}, ignore=ignore)  # clear ignored keys by merging with empty dict

	data = prune(data)
	return merge(output, data)


def prune(data: dict):
	"""Recursively remove empty dictionaries from data."""
	output = {}

	for key, nested_value in data.items():
		if isinstance(nested_value, dict):
			nested_value = prune(nested_value)

			if len(nested_value) > 0:
				output[key] = nested_value
		else:
			output[key] = nested_value

	return output
