class Store:
    def get_customer_data(self, customer_id):
        raise NotImplementedError(
            "get_customer_data() must be implemented by subclasses"
        )

    def set_customer_data(self, customer_id, data):
        raise NotImplementedError(
            "set_customer_data() must be implemented by subclasses"
        )

    def set_customer_feature_value(self, customer_id, key, value):
        raise NotImplementedError(
            "set_customer_feature_value() must be implemented by subclasses"
        )
