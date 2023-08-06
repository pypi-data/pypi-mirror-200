"""
    This file contains the helper code to handle the
    Dash App authentication.

    Currently supports the local Credentials file usage.
"""
import os

#####################################################
# Credentials SETUP
# This setup should change for deployed application.
# If deployed inside GCP, then authentication is transparent for client libs.
#####################################################
# CREDENTIALS SETUP
script_path = os.path.realpath(__file__)
root_path = os.path.dirname(script_path)
common_path = os.path.join(os.path.dirname(root_path), "common")
CREDENTIALS_PATH = os.path.join(
    os.path.join(common_path, "credentials"), "pub_sub_to_bigquery_credentials.json"
)
