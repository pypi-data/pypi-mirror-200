"""
This python module provides information about the plug-points published by this monad.
For each plug-point, it shows the following
  plug_point_class:
    class that represents plug-point.
    it is an abstraction of the functionality expected by the business logic.
    it provides method names including inputs (method parameters), outputs (method return).
    usually the method body is empty.
    currently informational field. currently, plugin manager does not use this.
  plugin_class:
    class that represents plug-in - which is a concrete implementation of the
    abstract plug_point_class.
    it provides concrete implementation of the methods in plug_point_class.
    currently informational field.
    currently, plugin manager does not use this but will do so soon!!
  plugin_module:
    python module that defines a concrete implementation of plug_point_class.
  description:
    provide a good summary description of the intent of the plug-point.
    details can be in plug_point_class.
  pluggable:
    class or python module that uses the plug-point.
    this is also just for reference to the reader.
    currently informational field.
"""
monad_aa_plug_point_configuration = {
    "report_status_plug_point": {
        "plug_point_class": "ReportStatusPlugPoint",
        "plugin_class": "ReportStatusPlugIn",
        "plugin_module": "aa.plugs.report_status_plug_in",
        "description": "provides a core persistence for report status object",
        "pluggable": "report_initiator, report_generator"  # python module that uses the plug point
    },
    "initiate_report_generation_plug_point": {
        "plug_point_class": "InitiateReportGenerationPlugPoint",
        "plugin_class": "InitiateReportGenerationPlugIn",
        "plugin_module": "aa.plugs.initiate_report_generation_plug_in",
        "description": "provides core messaging implementation of initiate report generation."
                       "it uses queues allowing report generation to be processed asynchronously",
        "pluggable": "report_generator"
    },
    "source_aa_data_plug_point": {
        "plug_point_class": "SourceAADataPlugPoint",
        "plugin_class": "AASourceDataPersistencePlugIn",
        "plugin_module": "aa.plugs.source_aa_data_plug_in",
        "description": "provides a core persistence for the source data used for the report",
        "pluggable": "report_generator"
    },
    "generated_aa_report_plug_point": {
        "plug_point_class": "AAReportPlugPoint",
        "plugin_class": "AAReportPlugIn",
        "plugin_module": "aa.plugs.generated_aa_report_plug_in",
        "description": "provides a core persistence for generated aa report object",
        "pluggable": "report_generator"
    }
}
