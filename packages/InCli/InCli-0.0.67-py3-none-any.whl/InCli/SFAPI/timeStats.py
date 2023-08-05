from . import restClient,utils


class TimeStats:
    time_records = []
    time_record = {}

    def new(self,fields=None):
        self.time_record = {}
        self.time_records.append(self.time_record)
        if fields == None: return
        for field in fields:
            self.time_record[field] = ''
    
    def time(self,field):
        self.time_record[field] = restClient.getLastCallElapsedTime()

    def time_inner(self,field,time):
        self.time_record[field] = time

    def time_no(self,field,value):
        self.time_record[field] = value
    
    def print(self):
        utils.printFormated(self.time_records)


