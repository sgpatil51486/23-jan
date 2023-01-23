import time
from aifc import Error

import requests
import json
import sys


class Test_Failed(Error):
    pass

token = sys.argv[1]

def login(token):
    s = requests.Session()
    head = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    head["Authorization"] = "Bearer " + token
    suiteid = 'SUITE1258'
    baseUrl = 'https://backend.fireflink.com'

    run = s.get(baseUrl + ':8102/optimize/v1/suite/runSetting/run/' + suiteid, headers=head)
    runout = json.loads(run.content)
    rob = runout['responseObject']
    pes = s.post(baseUrl+':8109/optimize/v1/dashboard/execution/suite/' + suiteid, headers=head, json=rob)
    out = json.loads(pes.content)
    exid = out['responseObject']['id']

    time.sleep(3)
    sc = 0
    while (sc < 1):
        r1 = s.get(baseUrl + ':8109/optimize/v1/dashboard/execution/' + exid, headers=head)
        c1 = json.loads(r1.content)
        fr1 = c1['responseObject']['executionStatus']
        print('status : ' + fr1 + '......')
        if (fr1 == "Completed" or fr1 == "Terminated"):
            if fr1 == 'Completed':
                r2 = s.get(baseUrl + ':8110/optimize/v1/executionResponse/result/' + exid, headers=head)
                c2 = json.loads(r2.content)
                fr2 = c2['responseObject']['suiteStatus']
                if fr2 == 'FAIL':
                    raise Test_Failed
                elif fr2 == 'WARNING':
                    print('End Result : ' + 'Warning')
                elif fr2 == 'Aborted':
                    print('End Result : ' + 'Aborted')
                else:
                    print("End Result : " + 'Test Passed')
                sc = 1
            elif (fr1 == 'Terminated'):
                print("End Result : " + fr1)
                sc = 1
        time.sleep(10)

login(token)
