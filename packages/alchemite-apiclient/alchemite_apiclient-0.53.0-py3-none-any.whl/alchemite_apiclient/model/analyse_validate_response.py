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
    from alchemite_apiclient.model.analyse_validate_response_column_analytics import AnalyseValidateResponseColumnAnalytics
    globals()['AnalyseValidateResponseColumnAnalytics'] = AnalyseValidateResponseColumnAnalytics


class AnalyseValidateResponse(ModelNormal):
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
        ('mean_validation_metric',): {
            'inclusive_maximum': 1,
        },
        ('median_validation_metric',): {
            'inclusive_maximum': 1,
        },
        ('mean_coefficient_of_determination',): {
            'inclusive_maximum': 1,
        },
        ('median_coefficient_of_determination',): {
            'inclusive_maximum': 1,
        },
        ('mean_rmse',): {
            'inclusive_minimum': 0,
        },
        ('median_rmse',): {
            'inclusive_minimum': 0,
        },
        ('total_uncertainty_divergence',): {
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
            'mean_validation_metric': (float, none_type,),  # noqa: E501
            'mean_validation_metric_uncertainty': (float, none_type,),  # noqa: E501
            'median_validation_metric': (float, none_type,),  # noqa: E501
            'median_validation_metric_uncertainty': (float, none_type,),  # noqa: E501
            'mean_coefficient_of_determination': (float, none_type,),  # noqa: E501
            'mean_coefficient_of_determination_uncertainty': (float, none_type,),  # noqa: E501
            'median_coefficient_of_determination': (float, none_type,),  # noqa: E501
            'median_coefficient_of_determination_uncertainty': (float, none_type,),  # noqa: E501
            'mean_rmse': (float, none_type,),  # noqa: E501
            'mean_rmse_uncertainty': (float, none_type,),  # noqa: E501
            'median_rmse': (float, none_type,),  # noqa: E501
            'median_rmse_uncertainty': (float, none_type,),  # noqa: E501
            'total_uncertainty_divergence': (float, none_type,),  # noqa: E501
            'column_analytics': ([AnalyseValidateResponseColumnAnalytics],),  # noqa: E501
            'predictions': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():  # noqa
        return None


    attribute_map = {
        'mean_validation_metric': 'meanValidationMetric',  # noqa: E501
        'mean_validation_metric_uncertainty': 'meanValidationMetricUncertainty',  # noqa: E501
        'median_validation_metric': 'medianValidationMetric',  # noqa: E501
        'median_validation_metric_uncertainty': 'medianValidationMetricUncertainty',  # noqa: E501
        'mean_coefficient_of_determination': 'meanCoefficientOfDetermination',  # noqa: E501
        'mean_coefficient_of_determination_uncertainty': 'meanCoefficientOfDeterminationUncertainty',  # noqa: E501
        'median_coefficient_of_determination': 'medianCoefficientOfDetermination',  # noqa: E501
        'median_coefficient_of_determination_uncertainty': 'medianCoefficientOfDeterminationUncertainty',  # noqa: E501
        'mean_rmse': 'meanRMSE',  # noqa: E501
        'mean_rmse_uncertainty': 'meanRMSEUncertainty',  # noqa: E501
        'median_rmse': 'medianRMSE',  # noqa: E501
        'median_rmse_uncertainty': 'medianRMSEUncertainty',  # noqa: E501
        'total_uncertainty_divergence': 'totalUncertaintyDivergence',  # noqa: E501
        'column_analytics': 'columnAnalytics',  # noqa: E501
        'predictions': 'predictions',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """AnalyseValidateResponse - a model defined in OpenAPI

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
            mean_validation_metric (float, none_type): Mean validation metric across all non-descriptor columns (R^2 for continuous columns, MCC for categorical columns). Will be null if the validation metric for every column is null.. [optional]  # noqa: E501
            mean_validation_metric_uncertainty (float, none_type): Uncertainty in the mean validation metric across all non-descriptor columns (R^2 for continuous columns, MCC for categorical columns). Will be null if the validation metric for every column is null.. [optional]  # noqa: E501
            median_validation_metric (float, none_type): Median validation metric across all non-descriptor columns (R^2 for continuous columns, MCC for categorical columns). Will be null if the validation metric for every column is null.. [optional]  # noqa: E501
            median_validation_metric_uncertainty (float, none_type): Uncertainty in the median validation metric across all non-descriptor columns (R^2 for continuous columns, MCC for categorical columns). Will be null if the validation metric for every column is null.. [optional]  # noqa: E501
            mean_coefficient_of_determination (float, none_type): Mean coefficient of determination across all non-descriptor columns. Will be null if the coefficient of determination for every column is null. Deprecated, see `meanValidationMetric` for information on the mean performance of columns across all columns. [optional]  # noqa: E501
            mean_coefficient_of_determination_uncertainty (float, none_type): Uncertainty in the mean coefficient of determination across all non-descriptor columns. Will be null if the coefficient of determination for every column is null. Deprecated, see `meanValidationMetricUncertainty` for information on the uncertainty of the mean performance across all columns. [optional]  # noqa: E501
            median_coefficient_of_determination (float, none_type): Median coefficient of determination across all non-descriptor columns. Will be null if the coefficient of determination for every column is null. Deprecated, see `medianValidationMetric` for information on the median performance of columns across all columns. [optional]  # noqa: E501
            median_coefficient_of_determination_uncertainty (float, none_type): Uncertainty in the median coefficient of determination across all non-descriptor columns. Will be null if the coefficient of determination for every column is null. Deprecated, see `medianValidationMetricUncertainty` for information on the median performance of columns across all columns. [optional]  # noqa: E501
            mean_rmse (float, none_type): Mean root mean squared error across all non-descriptor columns. Will be null if the RMSE for every column is null. Deprecated, see `meanValidationMetric` for information on the mean performance of columns across all columns. [optional]  # noqa: E501
            mean_rmse_uncertainty (float, none_type): Uncertainty in the mean root mean squared error across all non-descriptor columns. Will be null if the RMSE for every column is null. Deprecated, see `meanValidationMetricUncertainty` for information on the uncertainty of the performance across all columns. [optional]  # noqa: E501
            median_rmse (float, none_type): Median root mean squared error across all non-descriptor columns. Will be null if the RMSE for every column is null. Deprecated, see `medianValidationMetric` for information on the median performance of columns across all columns. [optional]  # noqa: E501
            median_rmse_uncertainty (float, none_type): Uncertainty in the median root mean squared error across all non-descriptor columns. Will be null if the RMSE for every column is null. Deprecated, see `medianValidationMetricUncertainty` for information on the median performance of columns across all columns. [optional]  # noqa: E501
            total_uncertainty_divergence (float, none_type): The root mean square of all non-descriptor's `uncertaintyDivergence`. An indication of the extent to which the uncertainty associated with those columns deviate from the expected distribution of uncertainties. Values closer to 0 indicate closer match with the expected uncertainty distribution across all columns.. [optional]  # noqa: E501
            column_analytics ([AnalyseValidateResponseColumnAnalytics]): Information about the predictions in each column.  Each object in the array corresponds to a column and is ordered according to the order in the given dataset.. [optional]  # noqa: E501
            predictions (str): Only appears if returnPredictions is true. A CSV string containing one column of row headers plus three blocks of equally sized columns:   * The first row contains the column headers if returnColumnHeaders was True in the request   * The first column contains the row headers   * The 1st third of columns after the row headers contains the original values.   * The 2nd third of columns after the row headers contains the predictions for the original values.  The column headers in this block are the column names prefixed by `predicted_`.   * The 3rd third of columns after the row headers contains the uncertainties for the predicted values.  The column headers in the block are the column names prefixed by `uncertainty_` . [optional]  # noqa: E501
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
        """AnalyseValidateResponse - a model defined in OpenAPI

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
            mean_validation_metric (float, none_type): Mean validation metric across all non-descriptor columns (R^2 for continuous columns, MCC for categorical columns). Will be null if the validation metric for every column is null.. [optional]  # noqa: E501
            mean_validation_metric_uncertainty (float, none_type): Uncertainty in the mean validation metric across all non-descriptor columns (R^2 for continuous columns, MCC for categorical columns). Will be null if the validation metric for every column is null.. [optional]  # noqa: E501
            median_validation_metric (float, none_type): Median validation metric across all non-descriptor columns (R^2 for continuous columns, MCC for categorical columns). Will be null if the validation metric for every column is null.. [optional]  # noqa: E501
            median_validation_metric_uncertainty (float, none_type): Uncertainty in the median validation metric across all non-descriptor columns (R^2 for continuous columns, MCC for categorical columns). Will be null if the validation metric for every column is null.. [optional]  # noqa: E501
            mean_coefficient_of_determination (float, none_type): Mean coefficient of determination across all non-descriptor columns. Will be null if the coefficient of determination for every column is null. Deprecated, see `meanValidationMetric` for information on the mean performance of columns across all columns. [optional]  # noqa: E501
            mean_coefficient_of_determination_uncertainty (float, none_type): Uncertainty in the mean coefficient of determination across all non-descriptor columns. Will be null if the coefficient of determination for every column is null. Deprecated, see `meanValidationMetricUncertainty` for information on the uncertainty of the mean performance across all columns. [optional]  # noqa: E501
            median_coefficient_of_determination (float, none_type): Median coefficient of determination across all non-descriptor columns. Will be null if the coefficient of determination for every column is null. Deprecated, see `medianValidationMetric` for information on the median performance of columns across all columns. [optional]  # noqa: E501
            median_coefficient_of_determination_uncertainty (float, none_type): Uncertainty in the median coefficient of determination across all non-descriptor columns. Will be null if the coefficient of determination for every column is null. Deprecated, see `medianValidationMetricUncertainty` for information on the median performance of columns across all columns. [optional]  # noqa: E501
            mean_rmse (float, none_type): Mean root mean squared error across all non-descriptor columns. Will be null if the RMSE for every column is null. Deprecated, see `meanValidationMetric` for information on the mean performance of columns across all columns. [optional]  # noqa: E501
            mean_rmse_uncertainty (float, none_type): Uncertainty in the mean root mean squared error across all non-descriptor columns. Will be null if the RMSE for every column is null. Deprecated, see `meanValidationMetricUncertainty` for information on the uncertainty of the performance across all columns. [optional]  # noqa: E501
            median_rmse (float, none_type): Median root mean squared error across all non-descriptor columns. Will be null if the RMSE for every column is null. Deprecated, see `medianValidationMetric` for information on the median performance of columns across all columns. [optional]  # noqa: E501
            median_rmse_uncertainty (float, none_type): Uncertainty in the median root mean squared error across all non-descriptor columns. Will be null if the RMSE for every column is null. Deprecated, see `medianValidationMetricUncertainty` for information on the median performance of columns across all columns. [optional]  # noqa: E501
            total_uncertainty_divergence (float, none_type): The root mean square of all non-descriptor's `uncertaintyDivergence`. An indication of the extent to which the uncertainty associated with those columns deviate from the expected distribution of uncertainties. Values closer to 0 indicate closer match with the expected uncertainty distribution across all columns.. [optional]  # noqa: E501
            column_analytics ([AnalyseValidateResponseColumnAnalytics]): Information about the predictions in each column.  Each object in the array corresponds to a column and is ordered according to the order in the given dataset.. [optional]  # noqa: E501
            predictions (str): Only appears if returnPredictions is true. A CSV string containing one column of row headers plus three blocks of equally sized columns:   * The first row contains the column headers if returnColumnHeaders was True in the request   * The first column contains the row headers   * The 1st third of columns after the row headers contains the original values.   * The 2nd third of columns after the row headers contains the predictions for the original values.  The column headers in this block are the column names prefixed by `predicted_`.   * The 3rd third of columns after the row headers contains the uncertainties for the predicted values.  The column headers in the block are the column names prefixed by `uncertainty_` . [optional]  # noqa: E501
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
