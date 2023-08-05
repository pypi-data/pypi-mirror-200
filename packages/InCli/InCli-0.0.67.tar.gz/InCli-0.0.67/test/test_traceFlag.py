import unittest
from InCli import InCli
from InCli.SFAPI import file,restClient,tooling,Sobjects,utils,traceFlag,query

class Test_TraceFlag(unittest.TestCase):
    def test_descibre(self):
        restClient.init('NOSDEV')
        tooling.describe('DebugLevel')
        tooling.describe('TraceFlag')

    #    tooling.query("a")
        userId = Sobjects.IdF('User','username:uormaechea_nosdev@nos.pt')

        call = traceFlag.get_traceflags_for_user('username:uormaechea_nosdev@nos.pt')
        id = tooling.idF('TraceFlag',f"TracedEntityId:{userId}")

        tf = tooling.get('TraceFlag',id)
        utils.printFormated(tf)

        DebugLevelId = tooling.idF('DebugLevel',"DeveloperName:InCli")   

        call = tooling.idF('TraceFlag',f"DebugLevelId:{DebugLevelId}")

        q = f"select id from TraceFlag where DebugLevelId = '{DebugLevelId}' and TracedEntityId = '{userId}'"
        call = tooling.query(q)  
        traceFlagId = call['records'][0]['Id']

        traceFlag.update_trace_flag_incli(traceFlagId)
        call = tooling.get("TraceFlag","7tf3O000001LbmoQAC")
        
        call2 =  traceFlag.create_trace_flag_incli(userId=userId,DebugLevelId=DebugLevelId)
        print()

    def test_create(self):
        restClient.init('DTI')
        traceFlag.create_debug_level_incli()

    def test_set_incli_traceFlag_for_user(self):
        restClient.init('DTI')

        userF = "username:onboarding@nosdti-parceiros.cs109.force.com"
        traceFlag.set_incli_traceFlag_for_user(userF)

    def test_debuglevel_get(self):
        restClient.init('NOSDEV')

        call = tooling.tooling_idF('DebugLevel',"DeveloperName:XXXX")   
        self.assertTrue(call==None)

        id = tooling.tooling_idF('DebugLevel',"DeveloperName:InCli")   
        if id != None:
            tooling.tooling_delete('DebugLevel',id)
            id = tooling.tooling_idF('DebugLevel',"DeveloperName:InCli")   

            print()
        if id == None:
            tooling.create_debug_level_incli()
            print()

    def test_query_who(self):

        envs = ['DTI',"NOSDEV","NOSQSM","NOSPRD"]
        for env in envs:
            try:
                restClient.init(env)

                DebugLevelId = tooling.idF('DebugLevel',"DeveloperName:InCli")   
                q = f"select TracedEntityId,StartDate,ExpirationDate from TraceFlag where DebugLevelId='{DebugLevelId}' limit 100"

                res =tooling.query(q)
                q1 = f"select username from User where Id='{res['records'][0]['TracedEntityId']}'"
                res1 = query.query(q1)
                print()
                print(f'Environment: {env}')
                utils.printFormated(res1['records'])
            except Exception as e:
                utils.printException(e)

        print()

    def test_completions(self):
        restClient.init('NOSDEV')
        tooling.completions()

    def test_aync(self):
        restClient.init('NOSDEV')
        tooling.executeAnonymous()

    def test_limitUsageHistory(self):
        restClient.init('NOSDEV')

        q = "select fields(all) from NetworkPublicUsageDailyMetrics limit 10 "

        res = tooling.query(q)

        print()
