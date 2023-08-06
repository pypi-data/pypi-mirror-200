import json

from spackle import log
from spackle.constants import FEATURE_TYPE_FLAG
from spackle.exceptions import SpackleException
from spackle.stores.base import Store


class FileStore(Store):
    def __init__(self, path):
        log.log_warn("Using file store. This is not recommended for production.")
        self.path = path

    def get_customer_data(self, customer_id):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        try:
            return data[customer_id]
        except KeyError:
            raise SpackleException("Customer %s not found" % customer_id)

    def set_customer_data(self, customer_id, customer_data):
        # TODO: Global variable could result in race conditions here
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        data[customer_id] = customer_data
        with open(self.path, "w") as f:
            f.write(json.dumps(data))

    def set_customer_feature_value(self, customer_id, key, value):
        customer_data = self.get_customer_data(customer_id)
        for feature in customer_data["features"]:
            if feature["key"] == key:
                if feature["type"] == FEATURE_TYPE_FLAG:
                    feature["value_flag"] = value
                else:
                    feature["value_limit"] = value
                break
        else:
            raise SpackleException("Feature %s not found" % key)

        self.set_customer_data(customer_id, customer_data)
