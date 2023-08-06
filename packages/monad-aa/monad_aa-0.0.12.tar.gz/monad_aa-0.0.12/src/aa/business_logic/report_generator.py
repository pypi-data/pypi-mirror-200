import json
import os
import threading

from plugin.plugin_manager import PluginManager

import aa
from aa.plugs.generated_aa_report_plug_point import AAReportPlugPoint
from aa.plugs.source_aa_data_plug_point import SourceAADataPlugPoint
from aa.plugs.initiate_report_generation_plug_point import InitiateReportGenerationPlugPoint


def initiate_generate(report_id, account_number, date):
    # we know report generation can be a time-consuming workload.
    # this is because reading data, processing it, formatting it and writing to
    # storage, takes time.
    # this means report generation needs to be a separate process invoked by a
    # queue. of course, we don't want to limit ourselves to specific queue
    # implementation. for core/default plugin we will use queue
    _get_initiate_report_generation_plugin().produce_msg_report_generate(report_id, account_number, date)


def generate_report(report_id, account_number, date):
    print(f'{os.getpid()}:{threading.get_ident()}: report_generator: started')
    # retrieve data from the backend
    # this is through a plug-point
    aa_data = retrieve_aa_data(account_number, date)
    print(f'{os.getpid()}:{threading.get_ident()}: report_generator: retrieved data')

    # apply any business logic to transform the data
    # or filter or do stuff to make the data usable.
    # copy data into a file
    file = convert_to_csv(aa_data)

    # save file
    save_aa_report(report_id, account_number, file)

    aa.business_logic.report_initiator.save_as(report_id, "COMPLETED")
    print(f'{os.getpid()}:{threading.get_ident()}: report_generator: ended')


def generate_unique_report_id() -> str:
    # TODO generate a uuid
    return "12345"


def retrieve_aa_data(account_number, date):
    print("inside retrieve data")
    return _get_aa_source_data_persistence_plugin().retrieve_data(account_number, date)


def convert_to_csv(fruits_dict):
    header_dict = {}
    for fruit_dict in fruits_dict["fruits"]:
        for key in fruit_dict.keys():
            header_dict[key] = key

    header_row = []
    for key in header_dict.keys():
        header_row.append(key)

    fruit_rows = []
    for fruit_dict in fruits_dict["fruits"]:
        fruit_row = []
        for header_col in header_row:
            fruit_row.append(fruit_dict[header_col])
        fruit_rows.append(fruit_row)

    # combine one header row and each of the fruits rows to return a "table" of rows
    return [header_row, *fruit_rows]


def save_aa_report(report_id, account_number, file):
    """

    :param report_id:
    :param account_number: we do have to save the account number along with saved report
    this allows us to verify the user requesting the report id has access to the account
    for which the report was generated.
    :param file:
    :return:
    """
    _get_aa_report_persistence_plugin().save_file(report_id, account_number, file)


def retrieve_saved_aa_report(report_id) -> (str, str):
    # call the plug point to retrieve the saved file
    account_number, report_file = _get_aa_report_persistence_plugin().retrieve_file(report_id)
    return account_number, report_file


def _get_initiate_report_generation_plugin() -> InitiateReportGenerationPlugPoint:
    """
    convinence method to get the plugin for this plug point
    :return:
    """
    # tip: don't save this in this class. when core initializes/imports this module
    # infrastructure code would not have had opportunity to override. this why it is
    # important to always go to plugin manager for the most current plugin
    return PluginManager.get_plugin("initiate_report_generation_plug_point")


def _get_aa_source_data_persistence_plugin() -> SourceAADataPlugPoint:
    """
    convinence method to get the plugin for this plug point
    :return:
    """
    # tip: don't save this in this class. when core initializes/imports this module
    # infrastructure code would not have had opportunity to override. this why it is
    # important to always go to plugin manager for the most current plugin
    return PluginManager.get_plugin("source_aa_data_plug_point")


def _get_aa_report_persistence_plugin() -> AAReportPlugPoint:
    """
    convinence method to get the plugin for this plug point
    :return:
    """
    # tip: don't save this in this class. when core initializes/imports this module
    # infrastructure code would not have had opportunity to override. this why it is
    # important to always go to plugin manager for the most current plugin
    return PluginManager.get_plugin("generated_aa_report_plug_point")
