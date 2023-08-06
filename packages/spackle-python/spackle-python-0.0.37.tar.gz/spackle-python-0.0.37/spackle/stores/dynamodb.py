import boto3
import json
import requests
import uuid
from boto3 import Session
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from spackle import log

from spackle.stores.base import Store
from spackle.exceptions import SpackleException


class DynamoDBStore(Store):
    store_config = {}

    def __init__(self):
        self.client = self._bootstrap_client()

    def get_customer_data(self, customer_id):
        response = self.client.get_item(
            Key={
                "AccountId": {"S": self.store_config.get("identity_id", "")},
                "CustomerId": {"S": self._customer_key(customer_id)},
            },
            TableName=self.store_config.get("table_name", ""),
        )

        item = response.get("Item")
        if not item:
            return self._fetch_state_from_api(customer_id)

        data = json.loads(item["State"]["S"])
        log.log_debug("Retrieved customer data for %s: %s" % (customer_id, data))
        return data

    def _customer_key(self, customer_id):
        from spackle import schema_version

        return f"{customer_id}:{schema_version}"

    def _bootstrap_client(self):
        log.log_debug("Creating DynamoDB client...")

        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self._refresh_credentials(),
            refresh_using=self._refresh_credentials,
            method="sts-assume-role-with-web-identity",
        )
        session = get_session()
        session._credentials = session_credentials
        autorefresh_session = Session(botocore_session=session)
        return autorefresh_session.client(
            "dynamodb", region_name=self.store_config["region"]
        )

    def _refresh_credentials(self):
        log.log_debug("Refreshing credentials...")
        self._create_session()
        return self._fetch_credentials()

    def _create_session(self):
        from spackle import api_key, api_base

        session = requests.post(
            f"{api_base}/sessions",
            headers={"Authorization": f"Bearer {api_key}"},
        ).json()

        self.store_config = session["adapter"]
        log.log_debug("Configured adapter: %s" % session)

        return session

    def _fetch_credentials(self):
        log.log_debug("Assuming aws role %s..." % self.store_config["role_arn"])
        sts_client = boto3.client("sts")
        response = sts_client.assume_role_with_web_identity(
            RoleArn=self.store_config["role_arn"],
            RoleSessionName=str(uuid.uuid4()),
            WebIdentityToken=self.store_config["token"],
        )

        return {
            "access_key": response["Credentials"]["AccessKeyId"],
            "secret_key": response["Credentials"]["SecretAccessKey"],
            "token": response["Credentials"]["SessionToken"],
            "expiry_time": response["Credentials"]["Expiration"].isoformat(),
        }

    def _fetch_state_from_api(self, customer_id):
        from spackle import api_key, api_base

        log.log_warn("Customer %s not found in store, using API" % customer_id)
        response = requests.get(
            f"{api_base}/customers/{customer_id}/state",
            headers={"Authorization": f"Bearer {api_key}"},
        )

        if response.status_code != 200:
            raise SpackleException(
                "Customer %s not found; status code: %s; response: %s"
                % (customer_id, response.status_code, response.text)
            )

        data = response.json()
        log.log_debug("Retrieved customer data for %s: %s" % (customer_id, data))
        return data
