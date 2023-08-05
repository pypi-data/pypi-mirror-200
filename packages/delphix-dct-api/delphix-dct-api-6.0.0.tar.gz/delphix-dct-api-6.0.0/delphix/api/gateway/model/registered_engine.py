"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.1.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from delphix.api.gateway.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)
from ..model_utils import OpenApiModel
from delphix.api.gateway.exceptions import ApiAttributeError


def lazy_import():
    from delphix.api.gateway.model.tag import Tag
    globals()['Tag'] = Tag


class RegisteredEngine(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
        ('type',): {
            'None': None,
            'VIRTUALIZATION': "VIRTUALIZATION",
            'MASKING': "MASKING",
            'BOTH': "BOTH",
            'UNSET': "UNSET",
        },
        ('status',): {
            'None': None,
            'CREATED': "CREATED",
            'DELETING': "DELETING",
        },
        ('connection_status',): {
            'None': None,
            'ONLINE': "ONLINE",
            'OFFLINE': "OFFLINE",
        },
    }

    validations = {
        ('truststore_filename',): {
            'max_length': 1024,
            'min_length': 1,
            'regex': {
                'pattern': r'^[a-zA-Z0-9_\.]+$',  # noqa: E501
            },
        },
        ('truststore_password',): {
            'max_length': 1024,
            'min_length': 1,
        },
        ('username',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('password',): {
            'max_length': 4096,
            'min_length': 1,
        },
        ('masking_username',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('masking_password',): {
            'max_length': 4096,
            'min_length': 1,
        },
        ('hashicorp_vault_username_command_args',): {
            'max_items': 100,
            'min_items': 1,
        },
        ('hashicorp_vault_masking_username_command_args',): {
            'max_items': 100,
            'min_items': 1,
        },
        ('hashicorp_vault_password_command_args',): {
            'max_items': 100,
            'min_items': 1,
        },
        ('hashicorp_vault_masking_password_command_args',): {
            'max_items': 100,
            'min_items': 1,
        },
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'name': (str,),  # noqa: E501
            'hostname': (str,),  # noqa: E501
            'id': (str,),  # noqa: E501
            'uuid': (str, none_type,),  # noqa: E501
            'type': (str, none_type,),  # noqa: E501
            'version': (str, none_type,),  # noqa: E501
            'ssh_public_key': (str,),  # noqa: E501
            'cpu_core_count': (int, none_type,),  # noqa: E501
            'memory_size': (int, none_type,),  # noqa: E501
            'data_storage_capacity': (int, none_type,),  # noqa: E501
            'data_storage_used': (int, none_type,),  # noqa: E501
            'insecure_ssl': (bool,),  # noqa: E501
            'unsafe_ssl_hostname_check': (bool,),  # noqa: E501
            'truststore_filename': (str, none_type,),  # noqa: E501
            'truststore_password': (str, none_type,),  # noqa: E501
            'status': (str, none_type,),  # noqa: E501
            'connection_status': (str, none_type,),  # noqa: E501
            'connection_status_details': (str, none_type,),  # noqa: E501
            'username': (str, none_type,),  # noqa: E501
            'password': (str, none_type,),  # noqa: E501
            'masking_username': (str, none_type,),  # noqa: E501
            'masking_password': (str, none_type,),  # noqa: E501
            'hashicorp_vault_username_command_args': ([str], none_type,),  # noqa: E501
            'hashicorp_vault_masking_username_command_args': ([str], none_type,),  # noqa: E501
            'hashicorp_vault_password_command_args': ([str], none_type,),  # noqa: E501
            'hashicorp_vault_masking_password_command_args': ([str], none_type,),  # noqa: E501
            'masking_hashicorp_vault_id': (int, none_type,),  # noqa: E501
            'hashicorp_vault_id': (int, none_type,),  # noqa: E501
            'tags': ([Tag],),  # noqa: E501
            'masking_memory_used': (int, none_type,),  # noqa: E501
            'masking_allocated_memory': (int, none_type,),  # noqa: E501
            'masking_jobs_running': (int, none_type,),  # noqa: E501
            'masking_max_concurrent_jobs': (int, none_type,),  # noqa: E501
            'masking_available_cores': (int, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'name': 'name',  # noqa: E501
        'hostname': 'hostname',  # noqa: E501
        'id': 'id',  # noqa: E501
        'uuid': 'uuid',  # noqa: E501
        'type': 'type',  # noqa: E501
        'version': 'version',  # noqa: E501
        'ssh_public_key': 'ssh_public_key',  # noqa: E501
        'cpu_core_count': 'cpu_core_count',  # noqa: E501
        'memory_size': 'memory_size',  # noqa: E501
        'data_storage_capacity': 'data_storage_capacity',  # noqa: E501
        'data_storage_used': 'data_storage_used',  # noqa: E501
        'insecure_ssl': 'insecure_ssl',  # noqa: E501
        'unsafe_ssl_hostname_check': 'unsafe_ssl_hostname_check',  # noqa: E501
        'truststore_filename': 'truststore_filename',  # noqa: E501
        'truststore_password': 'truststore_password',  # noqa: E501
        'status': 'status',  # noqa: E501
        'connection_status': 'connection_status',  # noqa: E501
        'connection_status_details': 'connection_status_details',  # noqa: E501
        'username': 'username',  # noqa: E501
        'password': 'password',  # noqa: E501
        'masking_username': 'masking_username',  # noqa: E501
        'masking_password': 'masking_password',  # noqa: E501
        'hashicorp_vault_username_command_args': 'hashicorp_vault_username_command_args',  # noqa: E501
        'hashicorp_vault_masking_username_command_args': 'hashicorp_vault_masking_username_command_args',  # noqa: E501
        'hashicorp_vault_password_command_args': 'hashicorp_vault_password_command_args',  # noqa: E501
        'hashicorp_vault_masking_password_command_args': 'hashicorp_vault_masking_password_command_args',  # noqa: E501
        'masking_hashicorp_vault_id': 'masking_hashicorp_vault_id',  # noqa: E501
        'hashicorp_vault_id': 'hashicorp_vault_id',  # noqa: E501
        'tags': 'tags',  # noqa: E501
        'masking_memory_used': 'masking_memory_used',  # noqa: E501
        'masking_allocated_memory': 'masking_allocated_memory',  # noqa: E501
        'masking_jobs_running': 'masking_jobs_running',  # noqa: E501
        'masking_max_concurrent_jobs': 'masking_max_concurrent_jobs',  # noqa: E501
        'masking_available_cores': 'masking_available_cores',  # noqa: E501
    }

    read_only_vars = {
        'id',  # noqa: E501
        'status',  # noqa: E501
        'connection_status',  # noqa: E501
        'connection_status_details',  # noqa: E501
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, name, hostname, *args, **kwargs):  # noqa: E501
        """RegisteredEngine - a model defined in OpenAPI

        Args:
            name (str): The name of this engine.
            hostname (str): The hostname of this engine.

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            id (str): The Engine object entity ID.. [optional]  # noqa: E501
            uuid (str, none_type): The unique identifier generated by this engine.. [optional]  # noqa: E501
            type (str, none_type): The type of this engine.. [optional]  # noqa: E501
            version (str, none_type): The engine version.. [optional]  # noqa: E501
            ssh_public_key (str): The ssh public key of this engine.. [optional]  # noqa: E501
            cpu_core_count (int, none_type): The total number of CPU cores on this engine.. [optional]  # noqa: E501
            memory_size (int, none_type): The total amount of memory on this engine, in bytes.. [optional]  # noqa: E501
            data_storage_capacity (int, none_type): The total amount of storage allocated for engine objects and system metadata, in bytes.. [optional]  # noqa: E501
            data_storage_used (int, none_type): The amount of storage used by engine objects and system metadata, in bytes.. [optional]  # noqa: E501
            insecure_ssl (bool): Allow connections to the engine over HTTPs without validating the TLS certificate. Even though the connection to the engine might be performed over HTTPs, setting this property eliminates the protection against a man-in-the-middle attach for connections to this engine. Instead, consider creating a truststore with a Certificate Authority to validate the engine's certificate, and set the truststore_path propery. . [optional] if omitted the server will use the default value of False  # noqa: E501
            unsafe_ssl_hostname_check (bool): Ignore validation of the name associated to the TLS certificate when connecting to the engine over HTTPs. Setting this value must only be done if the TLS certificate of the engine does not match the hostname, and the TLS configuration of the engine cannot be fixed. Setting this property reduces the protection against a man-in-the-middle attack for connections to this engine. This is ignored if insecure_ssl is set. . [optional] if omitted the server will use the default value of False  # noqa: E501
            truststore_filename (str, none_type): File name of a truststore which can be used to validate the TLS certificate of the engine. The truststore must be available at /etc/config/certs/<truststore_filename> . [optional]  # noqa: E501
            truststore_password (str, none_type): Password to read the truststore. . [optional]  # noqa: E501
            status (str, none_type): the status of the engine . [optional]  # noqa: E501
            connection_status (str, none_type): The status of the connection to the engine.. [optional]  # noqa: E501
            connection_status_details (str, none_type): If set, details about the status of the connection to the engine.. [optional]  # noqa: E501
            username (str, none_type): The virtualization domain admin username.. [optional]  # noqa: E501
            password (str, none_type): The virtualization domain admin password.. [optional]  # noqa: E501
            masking_username (str, none_type): The masking admin username.. [optional]  # noqa: E501
            masking_password (str, none_type): The masking admin password.. [optional]  # noqa: E501
            hashicorp_vault_username_command_args ([str], none_type): Arguments to pass to the Vault CLI tool to retrieve the virtualization username for the engine.. [optional]  # noqa: E501
            hashicorp_vault_masking_username_command_args ([str], none_type): Arguments to pass to the Vault CLI tool to retrieve the masking username for the engine.. [optional]  # noqa: E501
            hashicorp_vault_password_command_args ([str], none_type): Arguments to pass to the Vault CLI tool to retrieve the virtualization password for the engine.. [optional]  # noqa: E501
            hashicorp_vault_masking_password_command_args ([str], none_type): Arguments to pass to the Vault CLI tool to retrieve the masking password for the engine.. [optional]  # noqa: E501
            masking_hashicorp_vault_id (int, none_type): Reference to the Hashicorp vault to use to retrieve masking engine credentials.. [optional]  # noqa: E501
            hashicorp_vault_id (int, none_type): Reference to the Hashicorp vault to use to retrieve virtualization engine credentials.. [optional]  # noqa: E501
            tags ([Tag]): The tags to be created for this engine.. [optional]  # noqa: E501
            masking_memory_used (int, none_type): The current amount of memory used by running masking jobs in bytes.. [optional]  # noqa: E501
            masking_allocated_memory (int, none_type): The maximum amount of memory available for running masking jobs in bytes.. [optional]  # noqa: E501
            masking_jobs_running (int, none_type): The number of masking jobs currently running.. [optional]  # noqa: E501
            masking_max_concurrent_jobs (int, none_type): The maximum number of masking jobs that can be running at the same time.. [optional]  # noqa: E501
            masking_available_cores (int, none_type): The number of CPU cores available to the masking engine.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.name = name
        self.hostname = hostname
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, name, hostname, *args, **kwargs):  # noqa: E501
        """RegisteredEngine - a model defined in OpenAPI

        Args:
            name (str): The name of this engine.
            hostname (str): The hostname of this engine.

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            id (str): The Engine object entity ID.. [optional]  # noqa: E501
            uuid (str, none_type): The unique identifier generated by this engine.. [optional]  # noqa: E501
            type (str, none_type): The type of this engine.. [optional]  # noqa: E501
            version (str, none_type): The engine version.. [optional]  # noqa: E501
            ssh_public_key (str): The ssh public key of this engine.. [optional]  # noqa: E501
            cpu_core_count (int, none_type): The total number of CPU cores on this engine.. [optional]  # noqa: E501
            memory_size (int, none_type): The total amount of memory on this engine, in bytes.. [optional]  # noqa: E501
            data_storage_capacity (int, none_type): The total amount of storage allocated for engine objects and system metadata, in bytes.. [optional]  # noqa: E501
            data_storage_used (int, none_type): The amount of storage used by engine objects and system metadata, in bytes.. [optional]  # noqa: E501
            insecure_ssl (bool): Allow connections to the engine over HTTPs without validating the TLS certificate. Even though the connection to the engine might be performed over HTTPs, setting this property eliminates the protection against a man-in-the-middle attach for connections to this engine. Instead, consider creating a truststore with a Certificate Authority to validate the engine's certificate, and set the truststore_path propery. . [optional] if omitted the server will use the default value of False  # noqa: E501
            unsafe_ssl_hostname_check (bool): Ignore validation of the name associated to the TLS certificate when connecting to the engine over HTTPs. Setting this value must only be done if the TLS certificate of the engine does not match the hostname, and the TLS configuration of the engine cannot be fixed. Setting this property reduces the protection against a man-in-the-middle attack for connections to this engine. This is ignored if insecure_ssl is set. . [optional] if omitted the server will use the default value of False  # noqa: E501
            truststore_filename (str, none_type): File name of a truststore which can be used to validate the TLS certificate of the engine. The truststore must be available at /etc/config/certs/<truststore_filename> . [optional]  # noqa: E501
            truststore_password (str, none_type): Password to read the truststore. . [optional]  # noqa: E501
            status (str, none_type): the status of the engine . [optional]  # noqa: E501
            connection_status (str, none_type): The status of the connection to the engine.. [optional]  # noqa: E501
            connection_status_details (str, none_type): If set, details about the status of the connection to the engine.. [optional]  # noqa: E501
            username (str, none_type): The virtualization domain admin username.. [optional]  # noqa: E501
            password (str, none_type): The virtualization domain admin password.. [optional]  # noqa: E501
            masking_username (str, none_type): The masking admin username.. [optional]  # noqa: E501
            masking_password (str, none_type): The masking admin password.. [optional]  # noqa: E501
            hashicorp_vault_username_command_args ([str], none_type): Arguments to pass to the Vault CLI tool to retrieve the virtualization username for the engine.. [optional]  # noqa: E501
            hashicorp_vault_masking_username_command_args ([str], none_type): Arguments to pass to the Vault CLI tool to retrieve the masking username for the engine.. [optional]  # noqa: E501
            hashicorp_vault_password_command_args ([str], none_type): Arguments to pass to the Vault CLI tool to retrieve the virtualization password for the engine.. [optional]  # noqa: E501
            hashicorp_vault_masking_password_command_args ([str], none_type): Arguments to pass to the Vault CLI tool to retrieve the masking password for the engine.. [optional]  # noqa: E501
            masking_hashicorp_vault_id (int, none_type): Reference to the Hashicorp vault to use to retrieve masking engine credentials.. [optional]  # noqa: E501
            hashicorp_vault_id (int, none_type): Reference to the Hashicorp vault to use to retrieve virtualization engine credentials.. [optional]  # noqa: E501
            tags ([Tag]): The tags to be created for this engine.. [optional]  # noqa: E501
            masking_memory_used (int, none_type): The current amount of memory used by running masking jobs in bytes.. [optional]  # noqa: E501
            masking_allocated_memory (int, none_type): The maximum amount of memory available for running masking jobs in bytes.. [optional]  # noqa: E501
            masking_jobs_running (int, none_type): The number of masking jobs currently running.. [optional]  # noqa: E501
            masking_max_concurrent_jobs (int, none_type): The maximum number of masking jobs that can be running at the same time.. [optional]  # noqa: E501
            masking_available_cores (int, none_type): The number of CPU cores available to the masking engine.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.name = name
        self.hostname = hostname
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
