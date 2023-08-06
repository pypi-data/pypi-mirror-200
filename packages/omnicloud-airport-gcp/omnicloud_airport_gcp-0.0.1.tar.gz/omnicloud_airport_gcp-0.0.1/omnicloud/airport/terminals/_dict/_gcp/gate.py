"""
This module defines a class GStorageJSON inherited from _TerminalDict
that implements methods for saving and loading dictionary to/from Google
Cloud Storage in JSON format.
"""

import json
from io import BytesIO

from omnicloud.airport.tools.json import kw4json

from omnicloud.airport.terminals._dict import Terminal
from omnicloud.airport.tools.gcp import storage as stt


__all__ = ['GStorageJSON']


class GStorageJSON(Terminal.Gate):
    """
    A class for loading and saving JSON data to/from Google Cloud Storage.
    """

    @classmethod
    def arriving(cls, place: str, **options):
        """
        Loads JSON data from Google Cloud Storage.

        Args:
            place (str): A string representing the Google Cloud Storage location, in the format
                "gs://bucket-name/object-name".
            options (dict): A dictionary containing the options for loading the JSON data.

        Returns:
            The loaded JSON data as a dictionary or string.
        """

        bucket_name, object_name = stt.split_bucket_and_object_names(place)

        # Create Google Cloud Storage client
        client = stt.get_client(stt.kw4client(options))

        # Retrieve bucket and blob
        blob = client.bucket(bucket_name).blob(object_name)

        # Download JSON data
        data = BytesIO()
        blob.download_to_file(data)
        data.seek(0)

        # Load JSON data and return
        if options.get('return_string', False):
            return data.read().decode()
        else:
            return json.load(data)

    @classmethod
    def departure(cls, parcel, place: str, **options):
        """
        Saves JSON data to Google Cloud Storage.

        Args:
            parcel (dict): A dictionary representing the JSON data to be saved.
            place (str): A string representing the Google Cloud Storage location, in the format
                "gs://bucket-name/object-name".
            options (dict): A dictionary containing the options for saving the JSON data.

        Returns:
            None.
        """

        json_kwargs = kw4json(options)
        client_kwargs = stt.kw4client(options)
        blob_kwargs = stt.kw4upload_from_string(options)

        bucket_name, object_name = stt.split_bucket_and_object_names(place)
        json_data = json.dumps(parcel, **json_kwargs)

        # Upload JSON data to Google Cloud Storage
        client = stt.get_client(client_kwargs)
        blob = client.bucket(bucket_name).blob(object_name)
        blob.upload_from_string(json_data, **blob_kwargs)
