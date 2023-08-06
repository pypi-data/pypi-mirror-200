import os
import threading
from time import sleep

print("lets test as we code")


def test_happy_path():
    """
    what it does:
    in this test we request a report and wait until it successfully generates one.

    details:
    the test calls monad's two entry-points. "request_report" and "is_report_ready".

    the first entry-point function "request_report"
        * acknowledges the request
        (i.e. authenticates, authorizes and validates the request)
        * kicks off a separate generation process (via a queue)
        * and finally responds with a report id.

    the test uses this report id to make the next entry-point call "is_report_ready"
    and it keeps trying until it gets a valid report

    (remember entry-points as lambda functions)
    """

    authentication_identifier = "cookie_value"

    import aa.entry_points
    report_id = aa.entry_points.request_report(authentication_identifier, "1234567001", "2021-04-08")
    assert report_id is not None

    wait_time = 1
    count = 0
    file = None
    while True:
        status, file = aa.entry_points.is_report_ready(authentication_identifier, report_id)
        if status:
            print(f'{os.getpid()}:{threading.get_ident()}: client: {status=}. {file=}')
            break
        else:
            print(f'{os.getpid()}:{threading.get_ident()}: client: {status=}. try again in {wait_time} seconds')
            count += 1
            if count > 5:
                break
            sleep(wait_time)

    assert file is not None
    expected_file = [['fruit', 'price'], ['apple', '2.99'], ['banana', '0.49'], ['cherry', '4.99']]
    assert file == expected_file

    print('all is well')
