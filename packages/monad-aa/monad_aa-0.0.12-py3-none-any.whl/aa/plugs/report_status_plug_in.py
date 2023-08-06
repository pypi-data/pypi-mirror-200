from collections import defaultdict

from aa.plugs.report_status_plug_point import ReportStatusPlugPoint


class ReportStatusPlugIn(ReportStatusPlugPoint):
    def __init__(self):
        super().__init__()
        self.status_dict = {}

    def clear_all(self):
        # global status_dict
        self.status_dict = defaultdict(dict)

    def save_status(self, report_id, status):
        self.status_dict[report_id] = status


# This method is needed for plugin framework.
def get_implementation():
    return ReportStatusPlugIn()
