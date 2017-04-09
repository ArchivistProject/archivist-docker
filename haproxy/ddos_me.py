#!/usr/bin/python3

import sys

def get_system_groups():
    return requests.get('http://localhost:4000/public/groups', verify=False)
def post_new_doc():
    data = {'file': 'data:application/pdf;base64,VGVzdERvYzEyMwo=', 'tags': ['generated'],
            'metadata_fields':[{'id':'title', 'name':'Title','type':'string','group':'Generic', 'data':'ARC board - Agile Board - JIRA'},
                               {'id':'author', 'name':'Author', 'type':'string', 'group':'Generic', 'data':''},
                               {'id':'date added', 'name':'Date Added', 'type':'date', 'group':'Generic', 'data':'2017-03-11'}]
            }
    return requests.post('http://localhost:4000/public/documents', json={'document':data}, verify=False)

WORKERS=20
TOTAL_REQUESTS=25 # must be divisible by 20
URL = eval(sys.argv[1])

import concurrent.futures
import requests
import time
import sys
import itertools

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

def make_request(m):
    with Timer() as t:
        r = m()
    return (t.interval, r.status_code)

times = []
codes = []
# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
    futures = [executor.submit(make_request, URL) for _ in range(TOTAL_REQUESTS)]
    counter = 1
    print('0.0% => 0')
    for future in concurrent.futures.as_completed(futures):
        if counter % (TOTAL_REQUESTS/20) == 0:
            print('{}% => {}'.format(100 * counter/TOTAL_REQUESTS, counter))
        counter += 1
        try:
            t,c = future.result()
            times.append(t)
            codes.append(c)
        except Exception as exc:
            print('Generated an exception: %s' % exc)
#print(times)
#print(codes)
print('{} => Average time: {}'.format(URL.__name__, sum(times)/len(times)))
print('{} => Status codes: {}'.format(URL.__name__, set(codes)))
for c in set(codes):
    print('{} => {}: {}'.format(URL.__name__, c, len([x for x in codes if x == c])))
