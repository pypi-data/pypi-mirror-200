# this plug point defines all the possible access patterns and write
# patterns for the report status object
# the plugin that implements this plug point can use this information
# to define the appropriate storage and efficient ways to provide the
# handle data with that storage


class ReportStatusPlugPoint:
    def __init__(self):
        pass

    def save_status(self, report_id, status):
        pass
