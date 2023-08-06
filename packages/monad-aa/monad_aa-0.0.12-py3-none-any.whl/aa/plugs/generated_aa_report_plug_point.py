# this plug point defines all the possible access patterns and write
# patterns for the generated report file
# the plugin that implements this plug point can use this information
# to define the appropriate storage and efficient ways to provide the
# handle data with that storage


class AAReportPlugPoint:
    def __init__(self):
        pass

    def save_file(self, report_id, account_number, file) -> None:
        pass

    def retrieve_file(self, report_id) -> (str, str):
        pass
