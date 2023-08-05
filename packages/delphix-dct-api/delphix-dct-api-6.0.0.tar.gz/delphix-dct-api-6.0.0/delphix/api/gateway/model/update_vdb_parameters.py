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
    from delphix.api.gateway.model.additional_mount_point import AdditionalMountPoint
    from delphix.api.gateway.model.oracle_rac_custom_env_file import OracleRacCustomEnvFile
    from delphix.api.gateway.model.oracle_rac_custom_env_var import OracleRacCustomEnvVar
    from delphix.api.gateway.model.virtual_dataset_hooks import VirtualDatasetHooks
    globals()['AdditionalMountPoint'] = AdditionalMountPoint
    globals()['OracleRacCustomEnvFile'] = OracleRacCustomEnvFile
    globals()['OracleRacCustomEnvVar'] = OracleRacCustomEnvVar
    globals()['VirtualDatasetHooks'] = VirtualDatasetHooks


class UpdateVDBParameters(ModelNormal):
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
    }

    validations = {
        ('name',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('db_username',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('db_password',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('environment_user_id',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('template_id',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('pre_script',): {
            'max_length': 1024,
            'min_length': 1,
        },
        ('post_script',): {
            'max_length': 1024,
            'min_length': 1,
        },
        ('parent_tde_keystore_path',): {
            'max_length': 1024,
            'min_length': 1,
        },
        ('parent_tde_keystore_password',): {
            'max_length': 1024,
            'min_length': 1,
        },
        ('tde_key_identifier',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('target_vcdb_tde_keystore_path',): {
            'max_length': 1024,
            'min_length': 1,
        },
        ('cdb_tde_keystore_password',): {
            'max_length': 1024,
            'min_length': 1,
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
            'db_username': (str,),  # noqa: E501
            'db_password': (str,),  # noqa: E501
            'validate_db_credentials': (bool,),  # noqa: E501
            'auto_restart': (bool,),  # noqa: E501
            'environment_user_id': (str,),  # noqa: E501
            'template_id': (str,),  # noqa: E501
            'listener_ids': ([str],),  # noqa: E501
            'new_dbid': (bool,),  # noqa: E501
            'cdc_on_provision': (bool,),  # noqa: E501
            'pre_script': (str,),  # noqa: E501
            'post_script': (str,),  # noqa: E501
            'hooks': (VirtualDatasetHooks,),  # noqa: E501
            'custom_env_vars': ({str: (str,)},),  # noqa: E501
            'custom_env_files': ([str],),  # noqa: E501
            'oracle_rac_custom_env_files': ([OracleRacCustomEnvFile],),  # noqa: E501
            'oracle_rac_custom_env_vars': ([OracleRacCustomEnvVar],),  # noqa: E501
            'parent_tde_keystore_path': (str,),  # noqa: E501
            'parent_tde_keystore_password': (str,),  # noqa: E501
            'tde_key_identifier': (str,),  # noqa: E501
            'target_vcdb_tde_keystore_path': (str,),  # noqa: E501
            'cdb_tde_keystore_password': (str,),  # noqa: E501
            'appdata_source_params': ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},),  # noqa: E501
            'additional_mount_points': ([AdditionalMountPoint], none_type,),  # noqa: E501
            'appdata_config_params': ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}, none_type,),  # noqa: E501
            'config_params': ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}, none_type,),  # noqa: E501
            'mount_point': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'name': 'name',  # noqa: E501
        'db_username': 'db_username',  # noqa: E501
        'db_password': 'db_password',  # noqa: E501
        'validate_db_credentials': 'validate_db_credentials',  # noqa: E501
        'auto_restart': 'auto_restart',  # noqa: E501
        'environment_user_id': 'environment_user_id',  # noqa: E501
        'template_id': 'template_id',  # noqa: E501
        'listener_ids': 'listener_ids',  # noqa: E501
        'new_dbid': 'new_dbid',  # noqa: E501
        'cdc_on_provision': 'cdc_on_provision',  # noqa: E501
        'pre_script': 'pre_script',  # noqa: E501
        'post_script': 'post_script',  # noqa: E501
        'hooks': 'hooks',  # noqa: E501
        'custom_env_vars': 'custom_env_vars',  # noqa: E501
        'custom_env_files': 'custom_env_files',  # noqa: E501
        'oracle_rac_custom_env_files': 'oracle_rac_custom_env_files',  # noqa: E501
        'oracle_rac_custom_env_vars': 'oracle_rac_custom_env_vars',  # noqa: E501
        'parent_tde_keystore_path': 'parent_tde_keystore_path',  # noqa: E501
        'parent_tde_keystore_password': 'parent_tde_keystore_password',  # noqa: E501
        'tde_key_identifier': 'tde_key_identifier',  # noqa: E501
        'target_vcdb_tde_keystore_path': 'target_vcdb_tde_keystore_path',  # noqa: E501
        'cdb_tde_keystore_password': 'cdb_tde_keystore_password',  # noqa: E501
        'appdata_source_params': 'appdata_source_params',  # noqa: E501
        'additional_mount_points': 'additional_mount_points',  # noqa: E501
        'appdata_config_params': 'appdata_config_params',  # noqa: E501
        'config_params': 'config_params',  # noqa: E501
        'mount_point': 'mount_point',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """UpdateVDBParameters - a model defined in OpenAPI

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
            name (str): The unique name of the VDB within a group.. [optional]  # noqa: E501
            db_username (str): The username of the database user (Oracle, ASE Only).. [optional]  # noqa: E501
            db_password (str): The password of the database user (Oracle, ASE Only).. [optional]  # noqa: E501
            validate_db_credentials (bool): Whether db_username and db_password must be validated, if present, against the VDB. This must be set to false when credentials validation is not possible, for instance if the VDB is known to be disabled.. [optional] if omitted the server will use the default value of True  # noqa: E501
            auto_restart (bool): Whether to enable VDB restart.. [optional]  # noqa: E501
            environment_user_id (str): The environment user ID to use to connect to the target environment.. [optional]  # noqa: E501
            template_id (str): The ID of the target VDB Template (Oracle Only).. [optional]  # noqa: E501
            listener_ids ([str]): The listener IDs for this provision operation (Oracle Only).. [optional]  # noqa: E501
            new_dbid (bool): Whether to enable new DBID for Oracle. [optional]  # noqa: E501
            cdc_on_provision (bool): Whether to enable CDC on provision for MSSql. [optional]  # noqa: E501
            pre_script (str): Pre script for MSSql.. [optional]  # noqa: E501
            post_script (str): Post script for MSSql.. [optional]  # noqa: E501
            hooks (VirtualDatasetHooks): [optional]  # noqa: E501
            custom_env_vars ({str: (str,)}): Environment variable to be set when the engine administers a VDB. See the Engine documentation for the list of allowed/denied environment variables and rules about substitution. Custom environment variables can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            custom_env_files ([str]): Environment files to be sourced when the Engine administers a VDB. This path can be followed by parameters. Paths and parameters are separated by spaces. Custom environment variables can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            oracle_rac_custom_env_files ([OracleRacCustomEnvFile]): Environment files to be sourced when the Engine administers an Oracle RAC VDB. This path can be followed by parameters. Paths and parameters are separated by spaces. Custom environment variables can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            oracle_rac_custom_env_vars ([OracleRacCustomEnvVar]): Environment variable to be set when the engine administers an Oracle RAC VDB. See the Engine documentation for the list of allowed/denied environment variables and rules about substitution. Custom environment variables can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            parent_tde_keystore_path (str): Path to a copy of the parent's Oracle transparent data encryption keystore on the target host. Required to provision from snapshots containing encrypted database files. (Oracle Multitenant Only). [optional]  # noqa: E501
            parent_tde_keystore_password (str): The password of the keystore specified in parentTdeKeystorePath. (Oracle Multitenant Only). [optional]  # noqa: E501
            tde_key_identifier (str): ID of the key created by Delphix. (Oracle Multitenant Only). [optional]  # noqa: E501
            target_vcdb_tde_keystore_path (str): Path to the keystore of the target vCDB. (Oracle Multitenant Only). [optional]  # noqa: E501
            cdb_tde_keystore_password (str): The password for the Transparent Data Encryption keystore associated with the CDB. (Oracle Multitenant Only). [optional]  # noqa: E501
            appdata_source_params ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}): The JSON payload conforming to the DraftV4 schema based on the type of application data being manipulated.. [optional]  # noqa: E501
            additional_mount_points ([AdditionalMountPoint], none_type): Specifies additional locations on which to mount a subdirectory of an AppData container. Can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            appdata_config_params ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}, none_type): The parameters specified by the source config schema in the toolkit. [optional]  # noqa: E501
            config_params ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}, none_type): Database configuration parameter overrides.. [optional]  # noqa: E501
            mount_point (str): Mount point for the VDB (AppData only), can only be updated while the VDB is disabled.. [optional]  # noqa: E501
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
    def __init__(self, *args, **kwargs):  # noqa: E501
        """UpdateVDBParameters - a model defined in OpenAPI

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
            name (str): The unique name of the VDB within a group.. [optional]  # noqa: E501
            db_username (str): The username of the database user (Oracle, ASE Only).. [optional]  # noqa: E501
            db_password (str): The password of the database user (Oracle, ASE Only).. [optional]  # noqa: E501
            validate_db_credentials (bool): Whether db_username and db_password must be validated, if present, against the VDB. This must be set to false when credentials validation is not possible, for instance if the VDB is known to be disabled.. [optional] if omitted the server will use the default value of True  # noqa: E501
            auto_restart (bool): Whether to enable VDB restart.. [optional]  # noqa: E501
            environment_user_id (str): The environment user ID to use to connect to the target environment.. [optional]  # noqa: E501
            template_id (str): The ID of the target VDB Template (Oracle Only).. [optional]  # noqa: E501
            listener_ids ([str]): The listener IDs for this provision operation (Oracle Only).. [optional]  # noqa: E501
            new_dbid (bool): Whether to enable new DBID for Oracle. [optional]  # noqa: E501
            cdc_on_provision (bool): Whether to enable CDC on provision for MSSql. [optional]  # noqa: E501
            pre_script (str): Pre script for MSSql.. [optional]  # noqa: E501
            post_script (str): Post script for MSSql.. [optional]  # noqa: E501
            hooks (VirtualDatasetHooks): [optional]  # noqa: E501
            custom_env_vars ({str: (str,)}): Environment variable to be set when the engine administers a VDB. See the Engine documentation for the list of allowed/denied environment variables and rules about substitution. Custom environment variables can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            custom_env_files ([str]): Environment files to be sourced when the Engine administers a VDB. This path can be followed by parameters. Paths and parameters are separated by spaces. Custom environment variables can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            oracle_rac_custom_env_files ([OracleRacCustomEnvFile]): Environment files to be sourced when the Engine administers an Oracle RAC VDB. This path can be followed by parameters. Paths and parameters are separated by spaces. Custom environment variables can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            oracle_rac_custom_env_vars ([OracleRacCustomEnvVar]): Environment variable to be set when the engine administers an Oracle RAC VDB. See the Engine documentation for the list of allowed/denied environment variables and rules about substitution. Custom environment variables can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            parent_tde_keystore_path (str): Path to a copy of the parent's Oracle transparent data encryption keystore on the target host. Required to provision from snapshots containing encrypted database files. (Oracle Multitenant Only). [optional]  # noqa: E501
            parent_tde_keystore_password (str): The password of the keystore specified in parentTdeKeystorePath. (Oracle Multitenant Only). [optional]  # noqa: E501
            tde_key_identifier (str): ID of the key created by Delphix. (Oracle Multitenant Only). [optional]  # noqa: E501
            target_vcdb_tde_keystore_path (str): Path to the keystore of the target vCDB. (Oracle Multitenant Only). [optional]  # noqa: E501
            cdb_tde_keystore_password (str): The password for the Transparent Data Encryption keystore associated with the CDB. (Oracle Multitenant Only). [optional]  # noqa: E501
            appdata_source_params ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}): The JSON payload conforming to the DraftV4 schema based on the type of application data being manipulated.. [optional]  # noqa: E501
            additional_mount_points ([AdditionalMountPoint], none_type): Specifies additional locations on which to mount a subdirectory of an AppData container. Can only be updated while the VDB is disabled.. [optional]  # noqa: E501
            appdata_config_params ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}, none_type): The parameters specified by the source config schema in the toolkit. [optional]  # noqa: E501
            config_params ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}, none_type): Database configuration parameter overrides.. [optional]  # noqa: E501
            mount_point (str): Mount point for the VDB (AppData only), can only be updated while the VDB is disabled.. [optional]  # noqa: E501
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
