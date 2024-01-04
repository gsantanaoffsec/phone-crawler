#  TEST FILE, THERE IS NO USEFUL FUNCTION

from time import sleep

import threading


def make_web_request():
    print('Making requisition...')
    sleep(3)
    print('Finished request!')


thread_1 = threading.Thread(target=make_web_request)
thread_1.start()
thread_2 = threading.Thread(target=make_web_request)
thread_2.start()
thread_3 = threading.Thread(target=make_web_request)
thread_3.start()
