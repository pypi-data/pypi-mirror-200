"""
    Alchemite

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501
    Contact: support@intellegens.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from alchemite_apiclient.model_utils import (  # noqa: F401
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
    OpenApiModel
)
from alchemite_apiclient.exceptions import ApiAttributeError


def lazy_import():
    from alchemite_apiclient.model.sample_def_continuous import SampleDefContinuous
    globals()['SampleDefContinuous'] = SampleDefContinuous


class SampleDefCompositionAllOf(ModelNormal):
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
            'COMPOSITION': "composition",
        },
    }

    validations = {
        ('values',): {
            'min_properties': 2,
            'min_items': 2,
        },
        ('min',): {
            'inclusive_minimum': 0,
        },
        ('max',): {
            'inclusive_minimum': 0,
        },
    }

    @cached_property
    def additional_properties_type():  # noqa
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():  # noqa
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'type': (str,),  # noqa: E501
            'values': ({str: (SampleDefContinuous,)},),  # noqa: E501
            'total': (float,),  # noqa: E501
            'min': (int,),  # noqa: E501
            'max': (int,),  # noqa: E501
            'hard_limit': (bool,),  # noqa: E501
        }

    @cached_property
    def discriminator():  # noqa
        return None


    attribute_map = {
        'type': 'type',  # noqa: E501
        'values': 'values',  # noqa: E501
        'total': 'total',  # noqa: E501
        'min': 'min',  # noqa: E501
        'max': 'max',  # noqa: E501
        'hard_limit': 'hardLimit',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, values, *args, **kwargs):  # noqa: E501
        """SampleDefCompositionAllOf - a model defined in OpenAPI

        Args:
            values ({str: (SampleDefContinuous,)}): Define the continuous columns and their ranges. Sum of lower bound values must be less than or equal to `total`. Sum of upper bound values must be greater than or equal to `total`. Columns defined here cannot be defined in another sampleDefinition type. 

        Keyword Args:
            type (str): Constrain two or more columns to sum up to `total`. Only supported for global optimization methods. . defaults to "composition", must be one of ["composition", ]  # noqa: E501
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
            total (float): The value the columns defined in `values` should sum up to. If not specified, then no total constraint will be applied.. [optional]  # noqa: E501
            min (int): The minimum columns defined in `values` to be non-zero.. [optional] if omitted the server will use the default value of 0  # noqa: E501
            max (int): The maximum columns defined in `values` to be non-zero. If not specified, it will default to the number of properties in `values`. [optional]  # noqa: E501
            hard_limit (bool): Whether min/max are strictly enforced. Unused if no min or max set. . [optional] if omitted the server will use the default value of False  # noqa: E501
        """

        type = kwargs.get('type', "composition")
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

        self.type = type
        self.values = values
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
    def __init__(self, values, *args, **kwargs):  # noqa: E501
        """SampleDefCompositionAllOf - a model defined in OpenAPI

        Args:
            values ({str: (SampleDefContinuous,)}): Define the continuous columns and their ranges. Sum of lower bound values must be less than or equal to `total`. Sum of upper bound values must be greater than or equal to `total`. Columns defined here cannot be defined in another sampleDefinition type. 

        Keyword Args:
            type (str): Constrain two or more columns to sum up to `total`. Only supported for global optimization methods. . defaults to "composition", must be one of ["composition", ]  # noqa: E501
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
            total (float): The value the columns defined in `values` should sum up to. If not specified, then no total constraint will be applied.. [optional]  # noqa: E501
            min (int): The minimum columns defined in `values` to be non-zero.. [optional] if omitted the server will use the default value of 0  # noqa: E501
            max (int): The maximum columns defined in `values` to be non-zero. If not specified, it will default to the number of properties in `values`. [optional]  # noqa: E501
            hard_limit (bool): Whether min/max are strictly enforced. Unused if no min or max set. . [optional] if omitted the server will use the default value of False  # noqa: E501
        """

        type = kwargs.get('type', "composition")
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

        self.type = type
        self.values = values
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
