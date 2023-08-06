from .locate import locate
from .merge import merge


def restructure(data: dict, specification: dict):
	"""Restructure data according to specification.

	A restructure specification is a flat map of keys to values, both in "key-path" format:

	A key-path is a dot-delimited string of keys e.g. "key1.key2.key3", useful for indexing
	into nested dictionaries. For example, "key1.key2.key3" is an index to 'value':

	data = {
		'key1': {
			'key2': {
				'key3': 'value'
			}
		}
	}

	In a restructure specification, both the keys and values are key-paths. The dictionary keys are
	the keys to be restructured, and the dictionary values are the new keys to use.

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

	:param data: Data to restructure.
	:param specification: Specification of restructuring operations to perform.
	"""
	if len(specification) != len(set(specification.values())):
		raise KeyError('Restructure specification contains duplicate destinations!')

	output = {}

	for source, destination in specification.items():
		source_parent, source_key = locate(source, data)
		destination_parent, destination_key = locate(destination, output, make_keys=True)
		destination_parent[destination_key] = source_parent[source_key]

	ignore = set(specification.keys())  # ignore keys that have moved (i.e. the sources from the specification)
	data_sanitized = merge(data, {}, ignore=ignore)  # clear ignored keys by merging with empty dict
	data_sanitized = prune(data_sanitized)

	return merge(output, data_sanitized)  # merge sanitized data with output without ignoring any keys from the output


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
