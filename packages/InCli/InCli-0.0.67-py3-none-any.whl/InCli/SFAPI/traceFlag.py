from . import Sobjects,tooling,utils
#def get_traceFlag_for_user(userF):
#    userId = Sobjects.IdF('User',userF)
#    q = f"select id, TracedEntityId,logtype, startdate, expirationdate, debuglevelid, debuglevel.apexcode, debuglevel.visualforce from TraceFlag where TracedEntityId = '{userId}'"
#    call = query(q)
#    utils.printFormated(call['records'],fieldsString="Id StartDate ExpirationDate DebugLevel.ApexCode",rename="DebugLevel.ApexCode%ApexCode",separator=' ')

def create_debug_level_incli():
    data = {
        "DeveloperName": "InCli",
        "Language": "pt_BR",
        "MasterLabel": "InCli",
        "Workflow": "FINE",
        "Validation": "INFO",
        "Callout": "INFO",
        "ApexCode": "FINEST",
        "ApexProfiling": "INFO",
        "Visualforce": "FINER",
        "System": "FINE",
        "Database": "FINEST",
        "Wave": "NONE",
        "Nba": "NONE"
    }
    call = tooling.post('DebugLevel',data=data)
    return call


def create_trace_flag_incli(userId,DebugLevelId):
    data = {
        "TracedEntityId":userId,
        "LogType":"USER_DEBUG",
        "DebugLevelId":DebugLevelId,
        "StartDate":utils.datetime_now_string(),
        "ExpirationDate":utils.datetime_now_string(addMinutes=10)
    }
    call = tooling.post('TraceFlag',data=data)
    return call

    #'7tf3O000001LbmoQAC'

def update_trace_flag_incli(id,minutes=5,start=-2):
    data = {
        "StartDate":utils.datetime_now_string(addMinutes=start),
        "ExpirationDate":utils.datetime_now_string(addMinutes=minutes)
    }
    call = tooling.patch(sobject='TraceFlag',id=id , data=data)
    tooling.checkError()
    return call

def get_traceflags_for_user(userF):
    userId = Sobjects.IdF('User',userF)

    q = f"select Id,StartDate,ExpirationDate,DebugLevelId from TraceFlag where TracedEntityId='{userId}'"
    call = tooling.query(q)
    print()

def set_incli_traceFlag_for_user(userF):
    userId = Sobjects.IdF('User',userF)
    DebugLevelId = tooling.idF('DebugLevel',"DeveloperName:InCli")   
    if DebugLevelId == None:
        call = create_debug_level_incli()
        DebugLevelId = call['id']  

    q = f"select Id from TraceFlag where DebugLevelId='{DebugLevelId}' and TracedEntityId = '{userId}'"
    call = tooling.query(q)
 #   traceFlagId = tooling.idF('TraceFlag',f"DebugLevelId:{DebugLevelId}")
  #  tf = tooling.get('TraceFlag',traceFlagId)
    if len(call['records']) == 0:
        call = create_trace_flag_incli(userId,DebugLevelId)
        traceFlagId = call['id']
    else:
       traceFlagId = call['records'][0]['Id']

    update_trace_flag_incli(traceFlagId,5)

    return traceFlagId
    
#	https://appsmobileqms.nos.pt
#   https://appsmobileqms.nos.pt/
#   https://appsmobileqms.nos.pt