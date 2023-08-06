import os
import threading
from collections import defaultdict

from aa.plugs.source_aa_data_plug_point import SourceAADataPlugPoint


class AASourceDataPersistencePlugIn(SourceAADataPlugPoint):
    def __init__(self):
        super().__init__()
        self.fruits = None

    def retrieve_data(self, account_nbr, date):
        print(f'{os.getpid()}:{threading.get_ident()}: AASourceDataPersistencePlugin:retrieve_data')
        self.fruits = {"fruits": [
            {"fruit": "apple", "price": "2.99"},
            {"fruit": "banana", "price": "0.49"},
            {"fruit": "cherry", "price": "4.99"},
        ]}
        return self.fruits


# This method is needed for plugin framework.
def get_implementation():
    return AASourceDataPersistencePlugIn()
