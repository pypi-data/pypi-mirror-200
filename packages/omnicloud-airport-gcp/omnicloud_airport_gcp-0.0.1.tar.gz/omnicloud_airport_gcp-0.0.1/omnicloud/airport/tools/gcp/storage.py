from tempfile import NamedTemporaryFile as _Temp

from google.cloud import storage as _storage
from omnicloud.airport.tools import dict as _dt


__all__ = [
    'split_bucket_and_object_names',
    'get_client',
    'kw4upload_from_string',
    'kw4client'
]


def split_bucket_and_object_names(place: str) -> tuple[str, str]:
    """
    Extracts the bucket name and object name from a given place string.

    Args:
        place (str): A string representing the Google Cloud Storage location, in the format
            "gs://bucket-name/object-name".

    Returns:
        A tuple containing the bucket name and object name.
    """
    if not place.startswith("gs://"):
        raise ValueError("Invalid GCS location. It should start with 'gs://'")
    place = place[5:]
    parts = place.split('/')

    if len(parts) < 1 or not parts[0]:
        raise ValueError("Invalid GCS location. Bucket name is missing.")
    bucket_name = parts[0]
    object_name = '/'.join(parts[1:])

    return bucket_name, object_name


def get_client(options: dict) -> _storage.Client:
    """
    Creates a Google Cloud Storage client object.

    Args:
        options (dict): A dictionary containing the options for creating the client.

    Returns:
        A storage.Client object.
    """

    if 'key_str' in options:
        with _Temp(mode="w", delete=False) as temp_file:
            temp_file.write(options['key_str'])
            key_file = temp_file.name
        del options['key_str']
        client = _storage.Client.from_service_account_json(key_file, **options)

        return client  # type: ignore

    if 'key_file' in options:
        key_file = options['key_file']
        del options['key_file']
        client = _storage.Client.from_service_account_json(key_file, **options)

        return client  # type: ignore

    return _storage.Client(**options)


def kw4upload_from_string(options: dict, name4log: str | None = None) -> dict:

    if not name4log:
        name4log = kw4upload_from_string.__name__

    blob_params = [
        'content_type',
        'num_retries',
        'predefined_acl',
        'if_generation_match',
        'if_generation_not_match',
        'if_metageneration_match',
        'if_metageneration_not_match',
        'timeout',
        'checksum',
        'retry'
    ]
    kwargs = {}
    for k in blob_params:
        kwargs = _dt.enrich(kwargs, options, k)

    kwargs = _dt.item_converter(kwargs, "num_retries", int, name4log)

    return kwargs


def kw4client(options: dict, name4log: str | None = None) -> dict:

    if not name4log:
        name4log = kw4client.__name__

    client_params = [
        'project', 'credentials', 'client_info', 'client_options', 'use_auth_w_custom_endpoint',
        'key_file', 'key_str'
    ]
    kwargs = {}
    for k in client_params:
        kwargs = _dt.enrich(kwargs, options, k)

    kwargs = _dt.item_converter(kwargs, "use_auth_w_custom_endpoint", bool, name4log)

    return kwargs
