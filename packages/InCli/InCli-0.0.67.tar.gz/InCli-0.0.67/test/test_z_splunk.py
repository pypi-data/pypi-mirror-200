import unittest
from InCli import InCli
from InCli.SFAPI import file,file_csv


class Test_Splunk(unittest.TestCase):
    def test_merge_files(self):
        J = file_csv.read('/Users/uormaechea/Downloads/Jw.csv',separator=',')
        apars = file_csv.read('/Users/uormaechea/Downloads/aparsw.csv',separator=',')

        lenJ = len(J)
        num = 0
        for ra in apars:
            found = False
            for i,rj in enumerate(J):
                if rj['parentRequestId'] == ra['parentRequestId']:
                    ra['bandwidth'] = rj['bandwidth']
                    J.pop(i)
                    found = True
                   # print('',sep='.')
                    num = num +1
                    break
            if found: continue
           # else: print(f"Not found: {ra['parentRequestId']}")
        print(f"J {len(J)} {lenJ} apars {len(apars)}  found {num}")
        file_csv.write('/Users/uormaechea/Downloads/output_week.csv',apars)
        print()


#(index=CS189) CASE(00D7a0000005DzR) sourcetype=CASE(applog*:J) | stats count by timestamp,bandwidth,runTime,logName,parentRequestId