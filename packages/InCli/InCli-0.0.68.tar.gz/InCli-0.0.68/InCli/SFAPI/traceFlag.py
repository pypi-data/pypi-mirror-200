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

def create_trace_flag_incli_f(userF):
    userId = Sobjects.IdF('User',userF)
    DebugLevelId = tooling.IdF('DebugLevel',"DeveloperName:InCli")
    return create_trace_flag_incli(userId,DebugLevelId)

def create_trace_flag_incli(userId,DebugLevelId):
    data = {
        "TracedEntityId":userId,
        "LogType":"USER_DEBUG",
        "DebugLevelId":DebugLevelId,
        "StartDate":utils.datetime_now_string(),
        "ExpirationDate":utils.datetime_now_string(addMinutes=10)
    }
    call = tooling.post('TraceFlag',data=data)
    return get_trace_flags(call['id'])

    #'7tf3O000001LbmoQAC'

def update_trace_flag_incli(id,minutes=5,start=-2):
    data = {
        "StartDate":utils.datetime_now_string(addMinutes=start),
        "ExpirationDate":utils.datetime_now_string(addMinutes=minutes)
    }
    call = tooling.patch(sobject='TraceFlag',id=id , data=data)
    return get_trace_flags(id)

def delete_trace_Flag(id):
    tooling.delete(sobject='TraceFlag',id=id)

def get_trace_flags(id):
    call = tooling.get(sobject='TraceFlag',id=id)
    return call

def get_InCli_traceflags_for_user(userF):
    try:
        call = get_traceflags_for_user(userF,developerName='InCli')
    except Exception as e:
        if 'invalid ID field' in e.args[0]['error']:
            utils.raiseException("INVALID_USER",f"User {userF} does not exist.")
        raise e
    return call
    
def get_traceflags_for_user(userF,developerName=None):
    userId = Sobjects.IdF('User',userF)

    q = f"select Id,StartDate,ExpirationDate,DebugLevelId,DebugLevel.DeveloperName,ApexCode,ApexProfiling,Callout,Database,LogType,System,TracedEntityId,Validation,Visualforce,Workflow from TraceFlag where TracedEntityId='{userId}'"

    call = tooling.query(q)

    if developerName!=None:
        call2 = [r for r in call['records'] if r['DebugLevel']['DeveloperName'] == developerName]
        if len(call2) > 1:
            print(f"There is more than one traceflag for user {userF} for InCli.")

        if len(call2) > 0:
            return call2[0]
        return None
    return call

def set_incli_traceFlag_for_user(userF):
    InCli_trace_flags = get_InCli_traceflags_for_user(userF)

    if InCli_trace_flags == None:
        InCli_trace_flags = create_trace_flag_incli_f(userF)

    InCli_trace_flags = update_trace_flag_incli(InCli_trace_flags['Id'],5)

    return InCli_trace_flags

def set_incli_traceFlag_for_user_old(userF):
    userId = Sobjects.IdF('User',userF)
    DebugLevelId = tooling.IdF('DebugLevel',"DeveloperName:InCli")   
    if DebugLevelId == None:
        call = create_debug_level_incli()
        DebugLevelId = call['id']  

    q = f"select Id from TraceFlag where DebugLevelId='{DebugLevelId}' and TracedEntityId = '{userId}'"
    call = tooling.query(q)

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