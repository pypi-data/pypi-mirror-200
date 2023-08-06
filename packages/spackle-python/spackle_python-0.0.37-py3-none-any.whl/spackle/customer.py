import pprint

import stripe
from spackle import log
from spackle.exceptions import SpackleException


class Customer:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    @staticmethod
    def retrieve(customer_id):
        from spackle import get_store

        log.log_debug("Retrieving customer data for %s" % customer_id)
        data = get_store().get_customer_data(customer_id)
        log.log_debug("Retrieved customer data for %s: %s" % (customer_id, data))
        return Customer(customer_id, data)

    @property
    def features(self):
        return self.data["features"]

    @property
    def subscriptions(self):
        subscriptions = []
        for s in self.data["subscriptions"]:
            stripe_sub = stripe.Subscription(id=s["id"])
            stripe_sub.update(s)
            subscriptions.append(stripe_sub)
        return subscriptions

    @property
    def flag_features(self):
        return [f for f in self.data["features"] if f["type"] == 0]

    @property
    def limit_features(self):
        return [f for f in self.data["features"] if f["type"] == 1]

    def enabled(self, key):
        for feature in self.flag_features:
            if feature["key"] == key:
                return feature["value_flag"]

        raise SpackleException("Flag feature %s not found" % key)

    def limit(self, key):
        for feature in self.limit_features:
            if feature["key"] == key:
                if feature["value_limit"] is None:
                    return float("inf")
                return feature["value_limit"]

        raise SpackleException("Limit feature %s not found" % key)

    def __repr__(self):
        return f"<Customer ({self.id}):\n{pprint.pformat(self.data)}>"
