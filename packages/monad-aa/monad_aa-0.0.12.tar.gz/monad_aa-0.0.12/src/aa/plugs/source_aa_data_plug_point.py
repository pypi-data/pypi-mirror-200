# this plug point defines all the possible access patterns and write
# patterns for the source of the data used for generating the report.
# the plugin that implements this plug point can use this information
# to define the appropriate storage and efficient ways to provide the
# handle data with that storage


class SourceAADataPlugPoint:
    def __init__(self):
        pass

    def retrieve_data(self, account_nbr, date):
        pass
