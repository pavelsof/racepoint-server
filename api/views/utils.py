from django.core.serializers.json import DjangoJSONEncoder

import json


def make_json(dictionary):
	"""
	Converts the given object to a json object.
	"""
	return json.dumps(dictionary, cls=DjangoJSONEncoder)


def read_json(json_data):
	"""
	Converts the given json object to a Python thing.
	"""
	if isinstance(json_data, bytes):
		json_data = json_data.decode()
	return json.loads(json_data)

