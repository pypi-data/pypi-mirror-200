import copy

from spackle import log
from spackle.constants import FEATURE_TYPE_FLAG
from spackle.exceptions import SpackleException
from spackle.stores.base import Store


class MemoryStore(Store):
    def __init__(self):
        log.log_warn("Using in-memory store. This is not recommended for production.")
        self.data = {}

    def get_customer_data(self, customer_id):
        try:
            return self.data[customer_id]
        except KeyError:
            raise SpackleException("Customer %s not found" % customer_id)

    def set_customer_data(self, customer_id, data):
        self.data[customer_id] = data

    def set_customer_feature_value(self, customer_id, key, value):
        customer_data = copy.deepcopy(self.get_customer_data(customer_id))
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
