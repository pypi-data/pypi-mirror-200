import os
import threading
from collections import defaultdict

from aa.plugs.generated_aa_report_plug_point import AAReportPlugPoint
from aa.plugs.report_status_plug_point import ReportStatusPlugPoint


# this must be defined globally (module level) so both consumer thread can update the same
# variable that is visible to producer thread
# key report_id, value tuple (account_number, file)
saved_files = defaultdict(lambda: (None, None))


class AAReportPlugIn(AAReportPlugPoint):
    def __init__(self):
        super().__init__()

    def save_file(self, report_id, account_number, file) -> None:
        print(f'{os.getpid()}:{threading.get_ident()}: AAReportPlugin:save_file started')
        saved_files[report_id] = (account_number, file)
        print(f'{os.getpid()}:{threading.get_ident()}: AAReportPlugin:save_file ended. {saved_files[report_id]}')

    def retrieve_file(self, report_id) -> (str, str):
        # clients may call this method even before the report file is saved,
        # so we should gracefully return rather than throw KeyError
        print(f'{os.getpid()}:{threading.get_ident()}: AAReportPlugin:retrieve_file {saved_files[report_id]=}')
        return saved_files[report_id]


# This method is needed for plugin framework.
def get_implementation():
    return AAReportPlugIn()
