from plugin.plugin_manager import PluginManager

from aa.plugs.report_status_plug_point import ReportStatusPlugPoint


def save_as(report_id, status):
    _get_report_status_plugin().save_status(report_id, status)
    pass


def _get_report_status_plugin() -> ReportStatusPlugPoint:
    """
    convenience method to get the plugin for this plug point
    :return:
    """
    # tip: don't save this in this class. when core initializes/imports this module
    # infrastructure code would not have had opportunity to override. this why it is
    # important to always go to plugin manager for the most current plugin
    return PluginManager.get_plugin("report_status_plug_point")
