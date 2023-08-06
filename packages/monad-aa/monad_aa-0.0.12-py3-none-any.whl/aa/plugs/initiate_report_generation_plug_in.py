import os
import queue
import sys
import threading
import traceback

from aa import entry_points
from aa.business_logic.report_generator import generate_report

from aa.plugs.initiate_report_generation_plug_point import InitiateReportGenerationPlugPoint

qq = queue.Queue()


class InitiateReportGenerationPlugIn(InitiateReportGenerationPlugPoint):
    def __init__(self):
        super().__init__()
        # self.q = queue.Queue()
        self.q = qq

    def consume_msg_report_generate(self):
        # consider moving this logic to framework.
        # it will be nice if we can create a function something like
        #    read_from_queue(
        #                       self.q, # queue name
        #                       entry_points.generate_report, # function to call
        #                       (report_id, account_number, date) # payload read from queue
        try:
            # this loop is similar to what AWS lambda does with SQS.
            # AWS lambda runtime polls SQS, reads messages and invokes target function
            # synchronously. See https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html
            while True:
                report_id, account_number, date = self.q.get()
                print(f'{os.getpid()}:{threading.get_ident()}: consume_msg_report_generate: working on {report_id}')
                entry_points.generate_report(report_id, account_number, date)
                self.q.task_done()
                print(f'{os.getpid()}:{threading.get_ident()}: consume_msg_report_generate: finished {report_id}')
        except Exception as excep:
            print(f'{os.getpid()}:{threading.get_ident()}: consume_msg_report_generate: caught exception {excep=}')
            print(f'{sys.exc_info()[2]}')
            print(f'{traceback.format_exc()}')
            sys.exit(1)

    def produce_msg_report_generate(self, report_id, account_number, date):
        threading.Thread(target=self.consume_msg_report_generate, daemon=True).start()
        self.q.put((report_id, account_number, date))
        print(f'{os.getpid()}:{threading.get_ident()}: initiate_report_generate: {report_id=}')


# This method is needed for plugin framework.
def get_implementation():
    return InitiateReportGenerationPlugIn()
