from . import restClient,query,file,utils,Sobjects,traceFlag,elementParser

import colorama
import sys,time,os
import ansi2html,re
import threading,traceback
from queue import Queue

def printLogRecords(loguser=None,limit=50,whereClause=None):
    logUserId = get_loguser_id(loguser) if loguser != None else None
    if loguser != None:
        print(f'Logs for user {loguser}:')
    logs = get_apexLog_records(logUserId,limit=limit,whereClause=whereClause)
    logs = utils.deleteNulls(logs,systemFields=False)
    logs1 = []
    for log in logs:
        log['LastModifiedDate'] = log['LastModifiedDate'].split('.')[0]
        log['StartTime'] = log['StartTime'].split('.')[0]
        log['LogUserId'] =  f"{log['LogUserId']} ({get_username_and_cache(log['LogUserId'])})"

        logs1.append(log)

    utils.printFormated(logs1,rename="LogLength%Len:DurationMilliseconds%ms:Application%App")
    return logs

def get_apexLog_records(logUserId=None,limit=50,whereClause=None):
    where = f" where {whereClause} " if whereClause != None else ''
    where = f" where logUserId='{logUserId}' " if logUserId is not None else where

    call = query.query(f"Select Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier FROM ApexLog  {where} order by LastModifiedDate desc limit {limit}")
    return call

def get_apexLog_record_and_body(logId):
    logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog where Id ='{logId}' limit 1")

    if logRecords == None or len(logRecords)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found in the Server.',other=f"No record in ApexLogwith Id {logId}")    
    logRecord = logRecords[0]

    action = f"/services/data/v56.0/sobjects/ApexLog/{logId}/Body/"
    logbody = restClient.callAPI(action)
    return logRecord,logbody

userCache = {}
def get_username_and_cache(Id):
    username_query = f"select Username from User where Id='{Id}'"
    if username_query not in userCache: userCache[username_query] = query.queryField(username_query) 
    return userCache[username_query]

def apexLog_record_to_string(logRecord):
    log = logRecord
    username = get_username_and_cache(log['LogUserId'])

    logLine = f"""{utils.CFAINT}LOGDATA:    Id: {log['Id']}   LogUserId: {log['LogUserId']} {utils.CGREEN}({username}){utils.CEND}{utils.CFAINT}    Request: {log['Request']}  Operation: {utils.CGREEN}{log['Operation']}{utils.CEND}{utils.CFAINT}    lenght: {log['LogLength']}    duration:  {utils.CGREEN}{log['DurationMilliseconds']} {utils.CEND} 
 {utils.CFAINT}LOGDATA:      startTime: {log['StartTime']}    app: {log['Application']}      status: {log['Status']}     location: {log['Location']}     requestIdentifier: {log['RequestIdentifier']}{utils.CEND}
    """     
    return logLine

def do_parse_storage(pc,search_dir=None):  
    if pc['store_logId'] != None:
       # pc['logId'] = pc['store_logId']
        pc['filepath'] = f"{restClient.logFolder()}{pc['store_logId']}.log"

        do_parse_logId(pc)
        return

    if search_dir==None:
        search_dir = restClient.logFolder()

    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    log_files = [f for f in files if '.log' in f]
    fileNames = [os.path.basename(f) for f in log_files]

    print(f"Files to be parsed in the store {len(log_files)}")
    file_dates = []

    print(f"Ordering files by date...")

    for log_file in log_files:
        body = get_apexLog_body_from_file(log_file)
        for line in body.splitlines():
            if '|' in line:
                _time = line.split(' ')[0]
                file_dates.append({
                    'time':_time,
                    'file':log_file
                })
                break

    newlist = sorted(file_dates, key=lambda d: d['time'])

    sorted_log_file = [d['file'] for d in newlist]

    print(f"Ordered.")

    try:
        parse_apexlogs_by_Ids_or_filepaths(pc,logIds=None,filepaths=sorted_log_file,printProgress=True,printNum=False,threads=0)

    except KeyboardInterrupt:
        print('Interrupted')
    
    print_parsing_results(pc)

   # print(frequency)

def do_parse_tail(pc):
    def auto_renew_traceFlag(tf):
        try:
            while True:
                traceFlag.update_trace_flag_incli(tf['Id'],minutes=5)
                time.sleep(10)
        except Exception as e:
            print(f"InCli no longer in auto, due to exception")
            utils.printException(e)

    def deleteRecords(delete_queue):
        def divide_chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]
            
        while True:
            logIds = delete_queue.get()

            try :
                logIdsList= list(divide_chunks(logIds,200))
                for l in logIdsList:
                    res = Sobjects.deleteMultiple('ApexLog',l)
                restClient.glog().debug(f"deleted records {logIds}")
                delete_queue.task_done()
            except utils.InCliError as e:
                if e.args[0]['errorCode'] != 'NO_LOG':
                    utils.printException(e)
            except Exception as e:
                print(logIds)
                print(e)

    timefield = "LastModifiedDate"

    logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog order by {timefield} desc limit 1")
    time0 = logRecords[0][timefield] if len(logRecords) > 0 else None
    timez = time0.split('.')[0] + "Z" if time0 != None else '2000-12-12T17:19:35Z'

    delete_queue= None
    restClient.glog().debug(f"deleteLogs-->{pc['deleteLogs']}")

    if (pc['deleteLogs'] or pc['auto']) and pc['loguser'] == None:  
        pc['loguser'] = f"username:{pc['connection']['Username']}"
    logUserId = get_loguser_id(pc['loguser']) if pc['loguser'] != None else None

    if pc['deleteLogs']==True:       
        restClient.glog().debug("Starting delete queue")
        delete_queue = Queue(maxsize=0)
        for x in range(0,1):
            threading.Thread(target=deleteRecords,args=(delete_queue,), daemon=True).start()
        restClient.glog().info(f"Auto delete Apexlog records for user {pc['loguser']} {logUserId} set to Auto")

    if pc['auto']:
       # logUserId = get_loguser_id(f"username:{pc['loguser']}") if logUserId == None else logUserId
        tf = traceFlag.set_incli_traceFlag_for_user(f"Id:{logUserId}")
        restClient.glog().info(f"TraceFlag for user {pc['loguser']} {logUserId} set to Auto with debug level name InCli.")

        utils.printFormated(tf,fieldsString="ApexCode,ApexProfiling,Callout,Database,LogType,System,Validation,Visualforce,Workflow",separator=',')

        threading.Thread(target=auto_renew_traceFlag,args=(tf,), daemon=True).start()

    try:
        waitingPrinted = False
        procesed = []
        greater = True
        while (True):
            if greater:    where = f" {timefield} > {timez} "
            else:          where = f" {timefield} >= {timez} "

            where = f" {pc['whereClause']} and {where}" if pc['whereClause'] is not None else where
            where = f" logUserId='{logUserId}'and {where} " if logUserId is not None else where

            fields = "Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier,SystemModstamp"
            logRecords = query.queryRecords(f"Select {fields} FROM ApexLog where {where} order by {timefield} asc")
            if len(logRecords) > 0:
                waitingPrinted = False

                logRecords_not_processed = [r for r in logRecords if r['Id'] not in procesed]
                ids_not_processed = [r['Id'] for r in logRecords_not_processed]
                if pc['noScreen']==False:
                    logIds = [r['Id'] for r in logRecords_not_processed]
                else:
                    records1 = []
                    for r in logRecords_not_processed:
                        if r['Operation'] not in ['<empty>','VFRemoting']: records1.append(r)
                        elif r['Operation'] == 'VFRemoting' and r['LogLength']>1000: records1.append(r)
                    logIds = [r['Id'] for r in records1 ]

                if len(ids_not_processed) == 0:
                    greater = True
                    continue
                greater = False
                procesed.extend(ids_not_processed)

                if len(logIds)>0:
                    parse_apexlogs_by_Ids_or_filepaths(logIds=logIds,pc=pc,raiseKeyBoardInterrupt=True,raise_no_log=False)

                time0 = logRecords[-1][timefield]
                timez = time0.split('.')[0] + "Z"

                if delete_queue!=None:
                    delete_queue.put(ids_not_processed)
                    restClient.glog().debug(f"{logIds} into queue...")

            elif  waitingPrinted == False:
                print()
                print(f"waiting for debug logs for user {pc['loguser']}")  if pc['loguser'] != None  else print(f"waiting for debug logs ")
                waitingPrinted = True

            time.sleep(2)
    except KeyboardInterrupt as e:
        print()
        print_parsing_results(pc)
        print("Terminating -tail..., cleaning up")
        if pc['auto']:
            print(f"Stopping -auto. Deleting InCli traceflag for user { pc['loguser']}")

        #traceFlag.update_trace_flag_incli(tf,minutes=1,start=-15)
    
        traceFlag.delete_trace_Flag(tf['Id'])
        if delete_queue != None: 
            while delete_queue.empty()==False:    time.sleep(1)
        print('Terminated')
        return

def do_parse_logs_lastN(pc):
    whereClause = pc['whereClause']
    loguser = pc['loguser']
    lastN = pc['lastN']

    if loguser ==None:
        loguser = restClient.getConfigVar('loguser')

    if loguser == None:
        print(f"{utils.CYELLOW}Getting logs for all users.{utils.CEND}")
    else:
        print(f"{utils.CYELLOW}Getting logs for {loguser}.{utils.CEND}")

    where = f" where {whereClause} " if whereClause is not None else ''
    where = f" where logUserId='{get_loguser_id(loguser)}' " if loguser is not None else where

    if lastN == None: lastN = 1
    q = f"Select Id FROM ApexLog {where} order by LastModifiedDate desc limit {lastN}"
    logIds = query.queryFieldList(q)
    if logIds == None or len(logIds)==0:   utils.raiseException(errorCode='NO_LOG',error=f'No logs can be found. ',other=q)

    parse_apexlogs_by_Ids_or_filepaths(logIds= logIds,pc=pc)
    print_parsing_results(pc)

def do_parse_from_file(parseContext):
    set_apexlog_body_in_pc(parseContext)

  #  parseContext['body'] = file.read(parseContext['filepath'])
    parseContext['operation'] = 'parsefile'
 #   name = os.path.basename(parseContext['filepath']).split('.')[0]
 #   parseContext['logId']=name
    name = os.path.basename(parseContext['filepath'])
    parseContext['logId'] = name.split('.')[0]
    context =  parse_apexlog_body(parseContext)
    print_parsed_lines_to_output(parseContext)
    return context

def do_parse_logId(parseContext):
    set_apexlog_body_in_pc(parseContext)
    context =  parse_apexlog_body(parseContext)
    print_parsed_lines_to_output(parseContext)

    return context

def parse_apexlogs_by_Ids_or_filepaths(pc,logIds=None,filepaths=None,raiseKeyBoardInterrupt=False,printProgress=False,threads=10,printNum=True,raise_no_log=True):
    def read_log_from_org(q):
      while True:
        try:
            Id = q.get()
            get_apexLog_body_from_file_otherwise_db(Id)
            restClient.glog().debug(f"Read body for Id {Id}")
            q.task_done()
        except Exception as e:
            if raise_no_log==False and e.args[0]['errorCode'] == 'NO_LOG':
                pass
            else:
                raise e

    if 'total_parsed'       not in pc:   pc['total_parsed'] = 0
    if 'parsed_Id_status'   not in pc:   pc['parsed_Id_status'] = []
    if 'errors' not in pc:   pc['errors'] = []
    if 'queue'  not in pc:   pc['queue'] = None

    if filepaths != None:
        threads = 0

    if threads >0: 
        threads = 1
        if pc['queue'] == None:
            pc['queue'] = Queue(maxsize=0)
            for x in range(0,threads):
                threading.Thread(target=read_log_from_org,args=(pc['queue'],), daemon=True).start()
        for logid in logIds:
            pc['queue'].put(logid)
            
    num = 0
    items = filepaths if filepaths != None else logIds
    for num,item in enumerate(items):
        if printProgress:
            sys.stdout.write("\r%d%%" % int(100*num/len(items)))
        try:
            if logIds!= None:
                parsed={ 'logId':item, 'status':'ok' }
                pc['logId'] = item
                pc['filepath'] = None
            else:
                parsed={ 'file':os.path.basename(item), 'status':'ok' }
                pc['filepath'] = item  
                pc['logId'] = None
             
            pc['parsed_Id_status'].append(parsed)
            set_apexlog_body_in_pc(pc)
            parse_apexlog_body(pc)
            print_parsed_lines_to_output(pc)
            if printNum:    print( pc['total_parsed']+num+1)
            if pc['context']['exception'] == True:    parsed['status'] = pc['context']['exception_msg'][0:200]

        except KeyboardInterrupt:
            if raiseKeyBoardInterrupt:        raise
            break
        except utils.InCliError as e:
             parsed['status'] = f"Parse error: {e.args[0]['errorCode']}  "
             utils.printException(e)
             pc['errors'].append(e)
        except Exception as e:
            parsed['status'] = f"Unknown: {e}"
            pc['errors'].append(e)
            print(traceback.format_exc())

    pc['total_parsed'] = pc['total_parsed'] + num + 1
    
def print_parsing_results(pc):
    print()

    if 'parsed_Id_status' not in pc:
        print("No files parsed.")
        return 
    parsed = pc['parsed_Id_status']
    errors = pc['errors']

    print(f"{pc['total_parsed']} logs parsed")
    parsed = [par for par in parsed if par['status']!='ok']

    if len(parsed) == 0:  print("No errors.")
    if len(parsed)>0:
        utils.printFormated(parsed)
        errors = list({error.args[0]['errorCode']:error for error in errors}.values())
        for error in errors:    utils.printException(error)  

def get_loguser_id(loguser):
    id = Sobjects.IdF('User',loguser)
    return id if id!= None else utils.raiseException('QUERY',f"User with field {loguser} does not exist in the User Object.") 

def get_apexLog_body_from_file(filename):
    if file.exists(filename):
        return file.read(filename)

    return None

def set_apexlog_body_in_pc(pc):
    """if pc['filepath'] defined, reads from the file specified. Otherwiese logId needs to be set. 
    """
    if 'filepath' in pc and pc['filepath'] != None:
        pc['logRecord'] = None
        pc['body'] = get_apexLog_body_from_file(pc['filepath'])
    else:
        pc['logRecord'],pc['body'],pc['filepath'] = get_apexLog_body_from_file_otherwise_db(pc['logId'])
    if pc['body'] == None :   utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{pc["logId"]}> cannot be found. ')
    if len(pc['body'])==0:    utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{pc["logId"]}> is empty. ')
    
def get_apexLog_body_from_file_otherwise_db(logId):
    """Gets the log body for the provided logId from file (if exists) otherwise from the Org"""
    filename = f"{restClient.logFolder()}{logId}.log"

    if file.exists(filename) == True:
        body = get_apexLog_body_from_file(filename)

        if body == None or len(body)==0:
            print("The file seems corrupted. Getting log from server.")
            file.delete(filename)
            return get_apexLog_body_from_file_otherwise_db(logId)
        return None,body,filename
    else:
        logRecord,body = get_apexLog_record_and_body(logId) 
        body = apexLog_record_to_string(logRecord) + body  
        save_to_store(logId,body)
        return logRecord,body,filename

def save_to_store(logId,body):
    filename = f"{restClient.logFolder()}{logId}.log"
    file.write(filename,body) 

def delta(obj,field):
    return obj[field][1] - obj[field][0] if len(obj[field]) > 1 else 0

def createContext(lines):
    context = {
        'totalQueries' : 0,
        'timeZero':0,
        'ident':0,
        'DEF:SOQL queries' : 0,
        'DEF:CPU time' : 0,
        'CMT:SOQL queries' : 0,
        'CMT:CPU time' : 0,
        "exception":False
    }
    context['totalQueries'] = 0
    context['timeZero'] = 0
    context['ident'] = 0
    context['DEF:SOQL queries'] = 0
    context['DEF:CPU time']=0
    context['CMT:SOQL queries'] = 0
    context['CMT:CPU time']=0
    context['exception'] = False
    context['file_exception'] = False
    context['previousElapsedTime'] = 0
    context['previousCPUTime'] = 0
    context['previousIsLimit'] = False
    context['prevTimes'] = {
        0:[0,0]
    }
    context['prevLevel'] = 0
    context['firstLineIn'] = True
    context['firstLineOut'] = True

    context['parsedLines'] = []
    context['openItemsList'] = []

    context['lines'] = lines

    return context

frequency = {}
def parse_apexlog_body(pc):
    if pc['body'] == None :  utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{pc["logId"]}> cannot be found. ')
    if len(pc['body'])==0:    utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{pc["logId"]}> is empty. ')

    try:
        context = createContext(pc['body'].splitlines())
        pc['context'] = context

        for num,line in enumerate(context['lines']):
            if context['firstLineIn'] == True:
                if 'APEX_CODE' in line:
                    context['firstLineIn'] = False
                    levels = line.strip().split(' ')[1].replace(',','=').replace(';','  ')
                    levels = f"{utils.CFAINT}{levels}{utils.CEND}"
                    obj = {  'type':'LOGDATA', 'output':levels  }
                    context['parsedLines'].append(obj)

                    continue      
                else:
                    obj = {    'type':'LOGDATA',   'output':line  }
                    context['parsedLines'].append(obj)
                    continue

            chunks = line.split('|')
            if len(chunks)<2:
                continue
            if len(chunks[0])<10:
                continue
            if len(chunks[1])>30:
                continue

            context['chunks'] = chunks
            context['chunks_lenght'] = len(chunks)
            context['line'] = line
            context['line_index'] = num

            if len(chunks)>1 and chunks[1] in ['SYSTEM_MODE_ENTER','SYSTEM_MODE_EXIT','HEAP_ALLOCATE','STATEMENT_EXECUTE','VARIABLE_SCOPE_BEGIN','HEAP_ALLOCATE','SYSTEM_METHOD_ENTRY','SYSTEM_METHOD_EXIT','SOQL_EXECUTE_EXPLAIN','ENTERING_MANAGED_PKG','SYSTEM_CONSTRUCTOR_ENTRY','SYSTEM_CONSTRUCTOR_EXIT']:    continue

            if len(chunks)>1 and chunks[1] in ['VALIDATION_RULE','VALIDATION_FORMULA','VALIDATION_PASS','WF_RULE_FILTER','WF_RULE_EVAL_VALUE','STATIC_VARIABLE_LIST','CUMULATIVE_LIMIT_USAGE_END','CUMULATIVE_LIMIT_USAGE','FLOW_CREATE_INTERVIEW_BEGIN','FLOW_CREATE_INTERVIEW_END','TOTAL_EMAIL_RECIPIENTS_QUEUED','CUMULATIVE_PROFILING_BEGIN','CUMULATIVE_PROFILING','CUMULATIVE_PROFILING_END','EXECUTION_STARTED','EXECUTION_FINISHED'] : continue

            if elementParser.parseVariableAssigment(context):      continue
            if elementParser.parseMethod(context):            continue
            if elementParser.parseSOQL(context)==True:        continue
            if elementParser.parseLimits(context):     continue
            if elementParser.parseUserDebug(context):  continue
            if elementParser.parseUserInfo(context):   continue
            if elementParser.parseExceptionThrown(context):   continue
            if elementParser.parseDML(context):               continue
            if elementParser.parseConstructor(context):       continue
            if elementParser.parseCodeUnit(context):          continue
            if elementParser.parseConstructor(context):       continue
            if elementParser.parseNamedCredentials(context): continue
            if elementParser.parseCallOutResponse(context): continue
            if elementParser.parseWfRule(context) : continue
            if elementParser.parseFlow(context) : continue
            
        if len(context['openItemsList']) > 0:
            a=1
        elementParser.appendEnd(context)

        return context

    except KeyboardInterrupt as e:
        print(f"Parsing for logI {pc['logId']} interrupted.")
        raise e
    except Exception as e:
        print(f"Exception while parsing for logI {pc['logId']} ")
        raise e


def print_parsed_lines_to_output(pc):
    def escape_ansi(line):
        ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        return ansi_escape.sub('', line)

    if 1==1:
        pc['context']['parsedLines'] = processRepetition(pc['context']['parsedLines'])

    logId = pc['logId']
    toFile= pc['writeToFile'] if 'writeToFile' in pc else False

    if toFile == True:
        filename = f"{restClient.logFolder()}{logId}_ansi.txt"

        original_stdout = sys.stdout
        with open(filename, 'w') as f:
            sys.stdout = f 
            print_parsed_lines(pc)
            sys.stdout = original_stdout 

        data = file.read(filename)
        converter = ansi2html.Ansi2HTMLConverter()
     #   converter.
        html = converter.convert(data)
        html = html.replace('background-color: #000000;','background-color: #020b3b;')
        html = html.replace('aa5500','ecec16')
        html = html.replace('F5F1DE','8e8383')
        html = html.replace('AAAAAA','FFFFFF')
        html = html.replace('000316','3c3e48')
        html = html.replace('aa0000','e41717')

        filename = f"{restClient.logFolder()}{logId}.html"
        file.write(filename,html)
        print(f"Html file: {filename}")
        clean = escape_ansi(data)
        filename = f"{restClient.logFolder()}{logId}.txt"
        file.write(filename,clean)  
        print(f"Txt file: {filename}")
 
    else:
        colorama.just_fix_windows_console()
        print_parsed_lines(pc)

def print_parsed_lines(pc):
    logId = pc['logId'] if 'logId' in pc else None
    context = pc['context']
    print_only_errors = pc['print_only_errors'] if 'print_only_errors' in pc else False
    if context['exception'] == False and print_only_errors == True: return 
    print('___________________________________________________________________________________________________________________________________________________________________')
    if logId != None:  print(logId)
    print()
    if logId != None:  print(f"{utils.CFAINT}Parsing log Id {logId}    file: {restClient.logFolder()}{logId}.log{utils.CEND}")
    elif pc['filepath'] != None:
            print(f"file: {pc['filepath']}")

    firstLines = True

    pc['new_print'] = True
    for num,parsedLine in enumerate(context['parsedLines']):
        if parsedLine['type'] == 'LOGDATA':
            print(parsedLine['output'])
            continue
        else:
            if firstLines == True:
                firstLines = False
                print()
                print()
        printLimits = pc['printLimits'] if 'printLimits' in pc else False

        if printLimits == False:
            if '*** getCpuTime() ***' in parsedLine['output']:   continue
            if '*** getQueries() ***' in parsedLine['output']:   continue
            if 'LoggingOpenInterface.' in parsedLine['output']:   continue
            if parsedLine['type'] == 'LIMIT':                    continue

        print_parsed_line(pc,parsedLine,num)    
    print()

def isRep(all_loops,parsed_line_index,parsed_line,parsed_lines):
      if parsed_line['type'] not in ['METHOD','WF_CRITERIA','CONSTRUCTOR','DEBUG']:  return False,None

      for loop in all_loops:
        links = len(loop)
        loop_start_position = loop[0]
        link_lenght = loop[1] - loop[0]
        loop_lenght = links * link_lenght

        if loop_start_position <= parsed_line_index <= loop_start_position + loop_lenght - 1:
            if loop_start_position <= parsed_line_index <= loop_start_position + link_lenght-1:

                parsed_line['loop'] = links
                parsed_line['is_loop'] = True
                parsed_line['loop_links'] = links
                parsed_line['loop_link_lenght'] = link_lenght
                parsed_line['loop_position'] = parsed_line_index - loop_start_position + 1

                if len(parsed_line['timeStamp']) > 1 and (loop_start_position <= parsed_line_index < loop_start_position + link_lenght):
                    total_method_time = 0
                    total_wait_time = 0
                    for link_index in range(0,links):
                        brother_index = parsed_line_index + link_index * link_lenght
                        brother = parsed_lines[brother_index]
                        brother_method_time = brother['timeStamp'][1] - brother['timeStamp'][0]
                        total_method_time = total_method_time + brother_method_time

                        if link_index !=0:
                            brother_previous_line = parsed_lines[brother_index - 1]

                            if brother_previous_line['ident'] < brother['ident']:
                                wait_time =  brother['timeStamp'][0] - brother_previous_line['timeStamp'][0]
                            else:
                                ts = brother_previous_line['timeStamp'][1] if len(brother_previous_line['timeStamp'])>1 else  brother_previous_line['timeStamp'][0]
                                wait_time =  brother['timeStamp'][0] - ts

                            total_wait_time = total_wait_time + wait_time
                        #    print(f"{brother_previous_line['ident']} {brother_previous_line['output']}  {brother_previous_line['timeStamp'][0]}  {brother_previous_line['timeStamp'][1]} {brother['ident']}  {brother['output']}   {brother['timeStamp'][0]} {brother['timeStamp'][1]}   {wait_time}  {total_wait_time}")
                    parsed_line['totalLoopTime'] = total_method_time
                    parsed_line['totalLoopWait'] = total_wait_time
    
                #for the last line in the chain, set time_exit to the very last in the loop
                if len(parsed_line['timeStamp']) > 1 : 
                    parsed_line['timeStamp'][1] = parsed_lines[ parsed_line_index + (links-1) * link_lenght ]['timeStamp'][1]
                return True,True

            else: return True,False

      return False,False

def processRepetition1(parsed_lines):

    for parsed_line in parsed_lines:
        if 'output' not in parsed_line:  
            print()

    all_loops = utils.get_all_loops(parsed_lines,"output")

    new_parsed_lines = []
    for parsedLineNum,parsedLine in enumerate(parsed_lines):
        if 'apexline' in parsedLine and parsedLine['apexline'] == "161":
            a=1
        is_loop, is_first_chain = isRep(all_loops,parsedLineNum,parsedLine,parsed_lines)
        if is_loop == True and is_first_chain == False:   continue
        new_parsed_lines.append(parsedLine)

    return new_parsed_lines   

def processRepetition(parsed_lines):

    for parsed_line in parsed_lines:
        if 'output' not in parsed_line:  
            print()

    all_loops = utils.get_all_loops(parsed_lines,"output")

    new_parsed_lines = []
    for parsedLineNum,parsedLine in enumerate(parsed_lines):
        if 'timeStamp' in parsedLine and parsedLine['timeStamp'][0] == 10188648957:
            a=1
            
        is_loop, is_first_chain = isRep(all_loops,parsedLineNum,parsedLine,parsed_lines)
        if is_loop == True and is_first_chain == False:   continue
        new_parsed_lines.append(parsedLine)

    return new_parsed_lines   

def emptyString(context,size,char=' ',ident=None):
 #   str = ''
    if ident is None:   
        ident = context['ident']
    length = ident * size
    str = " "*length
 #   for x in range(length):   str = str + char  
    return str       

def get_parent_if_last_for_level(parsed_lines,parsed_line_index):
    current = parsed_lines[parsed_line_index]
    for index in range(parsed_line_index+1,len(parsed_lines)):
        if parsed_lines[index]['ident'] == current['ident']:
            return None
        if parsed_lines[index]['ident'] < current['ident']:
            i = 1
            while True:
                parent = parsed_lines[parsed_line_index-i]
                if parent['ident'] < current['ident']:
                    return parent
                i = i + 1


def print_parsed_line(pc,d,parsed_line_index):
    context = pc['context']
    Cinit = utils.CEND

    if pc['new_print']:
        pc['new_print'] = False
        print( f"Log time: {pc['context']['parsedLines'][3]['lines'][0].split(' ')[0]} to {pc['context']['parsedLines'][-1]['lines'][0].split(' ')[0]}")

    if d['type'] == 'LIMITS':
        context['previousIsLimit'] = True
        return

    #levels
    level = d['ident']
    pcLevel = pc['level'] if 'level' in pc else None
    if pcLevel != None:
        if level > int(pc['level']):
            return

    #colors
    element_type = d['type']
    if element_type == 'DEBUG':
        element_type = f"{d['type']}-{d['subType']}"
        Cinit = utils.CRED if d['subType'] == 'ERROR' else utils.CGREEN
    elif element_type == 'VAR_ASSIGN' and d['subType'] == 'EXCEPTION':  Cinit = utils.CRED
    elif element_type == 'VAR_ASSIGN' and d['subType'] != 'EXCEPTION':  return
    elif d['type'] == 'EXCEPTION':  Cinit = utils.CRED
    elif d['type'] == 'SOQL':   Cinit = utils.CCYAN
    elif d['type'] == 'DML':    Cinit =  utils.CYELLOW
    elif d['type'] == 'CODE_UNIT':  Cinit =  utils.CYELLOW

    identation = f"{emptyString(context,1,' ',level)}"

    if 'output' not in d:
        print()
    output_string = d['output']
    
    apex_line_number = d['apexline'] if 'apexline' in d else ''

    cpu_time_entry = int(d['CPUTime'][0])
    cpu_time_exit = int(d['CPUTime'][1]) if len(d['CPUTime']) >1 else ''

    time_stamp_entry = d['timeStamp'][0]
    time_stamp_exit = d['timeStamp'][1] if len(d['timeStamp'])>1 else time_stamp_entry

    soql_total_queries_entry = d['totalQueries'][0]
    soql_total_queries_exit = d['totalQueries'][1] if len(d['SOQLQueries']) >1 else soql_total_queries_entry
    soql_total_queries_delta = soql_total_queries_exit-soql_total_queries_entry

    cpu_time_elapsed = cpu_time_entry - int(context['previousCPUTime'])

    if level == context['prevLevel']:  wait_time = time_stamp_entry - context['prevTimes'][level][1]
    if level >  context['prevLevel']:  wait_time = time_stamp_entry - context['prevTimes'][context['prevLevel']][0]
    if level <  context['prevLevel']:  wait_time = time_stamp_entry - context['prevTimes'][level][1]

    if wait_time <0 and 'is_loop' in d:   
        wait_time = time_stamp_entry - context['prevTimes'][level][0]

    if 'totalLoopWait' in d:
        wait_time = d['totalLoopWait'] + wait_time

    context['prevTimes'][level] = [time_stamp_entry,time_stamp_exit]

    wait_time = f"{wait_time/1000000:.0f}"

    if time_stamp_entry == 475822989:
        a=1
    wait_time_exit = "0"
    parent = get_parent_if_last_for_level( context['parsedLines'],parsed_line_index)
    if parent != None:
        if len(parent['timeStamp']) > 1:
            wait_time_exit = parent['timeStamp'][1] - time_stamp_exit
            wait_time_exit = f"{wait_time_exit/1000000:.0f}"

    context['prevLevel'] = level

    soql_queries_entry = int(d['SOQLQueries'][0])
    soql_queries_exit = d['SOQLQueries'][1] if len(d['SOQLQueries'])>1 else ''
    soql_queries_cmt_entry = d['cmtSOQLQueries'][0]
    soql_queries_cmt_exit = d['cmtSOQLQueries'][1] if len(d['cmtSOQLQueries'])>1 else soql_queries_cmt_entry

    context['previousCPUTime'] = cpu_time_entry
    context['previousElapsedTime']  = d['elapsedTime']

    element_type_color =utils. CYELLOW  if d['type'] in ['SOQL','DML','VAR_ASSIGN'] and level == 0 else ''

    if cpu_time_elapsed == 0 and element_type != 'END':
        cpu_time_elapsed = ''
        cpu_time_entry = ''

    Qmct_estimate = soql_total_queries_entry - soql_queries_entry

    element_time = f"{delta(d,'timeStamp')/1000000:.0f}"
    
    if 'totalLoopTime' in d:  element_time = f"{ d['totalLoopTime']/1000000:.0f}"

    if element_type == 'END':
        soql_queries_exit = d['SOQLQueries'][0]
        cpu_time_entry = d['CPUTime'][0]
        soql_queries_cmt_exit = d['cmtSOQLQueries'][0]

    time_ms = f"{d['elapsedTime']/1000000:.0f}"
    time_ms = f'{int(time_ms):,}'

    if 'is_loop' in d:
        ls = f"    x{d['loop_links']}-{d['loop_position']}"# if d['loop_position'] == 1 else f"             "
        output_string = f"{output_string}   {utils.CYELLOW}{ls}{utils.CEND}"
      #  ls = f"  for:  x{d['loop_links']}  " if d['loop_position'] == 1 else f"             "
      #  output_string = output_string + utils.CYELLOW + f"{ls}{d['loop_position']}" + utils.CEND
    if element_time == "0":  element_time =''
    if soql_total_queries_delta ==0: soql_total_queries_delta = ''
    if soql_total_queries_exit ==0: soql_total_queries_exit = ''
    if Qmct_estimate == 0: Qmct_estimate = ''
    if soql_queries_exit ==0:  soql_queries_exit=''
    if soql_queries_cmt_exit==0: soql_queries_cmt_exit=''
    if soql_total_queries_entry == 0: soql_total_queries_entry = ''
    if wait_time == "0":  wait_time =''
    if wait_time_exit == "0":  wait_time_exit ='' 
    else: wait_time_exit=f"{wait_time_exit}"
    if soql_queries_cmt_entry == 0 : soql_queries_cmt_entry = ''
    if soql_queries_entry == 0 : soql_queries_entry = ''

    time_stamp_entry = utils.CLIGHT_GRAY +utils.CFAINT+ f"{time_stamp_entry:12}" + utils.CEND
    time_stamp_exit = utils.CLIGHT_GRAY +utils.CFAINT+ f"{time_stamp_exit:12}" + utils.CEND

    s = utils.CLIGHT_GRAY +utils.CFAINT+  "|" + utils.CEND

    times_lenght = 12

    if context['firstLineOut'] == True:
       # valname = f"{'wait':>5}     time query  Call Stack"
        valname = f"time         query  Call Stack"

        print(f"{utils.CFAINT}{'time entry':^12}{s}{utils.CFAINT}{'time exit':^12}{s}{'ts':^8}{s}{'CPU':^6}{s}{'cpuD':^6}{s}{'Qt':^3}{s}{'Q':^3}{s}{'Qmp':^3}{s}{'Qe':^3}{s}{'type':^21}{s}{'line':^4}{s}{valname:50}")
        context['firstLineOut'] = False

    if level % 2 == 0:
        et_color = utils.CGREEN + utils.CFAINT
    else:
        et_color = utils.CWHITE + utils.CFAINT

    a=f"{wait_time}·{element_time}·{wait_time_exit}"
    lena = len(a)
    aa = times_lenght-lena
    if aa<0: aa=0
  #  element_time = utils.CGREEN + utils.CFAINT+f"{wait_time}·{utils.CWHITE}{element_time}{utils.CGREEN}{utils.CFAINT}·{wait_time_exit:<{aa}}"
    element_time = utils.CGREEN + f"{wait_time}·{utils.CWHITE}{element_time}{utils.CLIGHT_GREEN}·{wait_time_exit}{'':<{aa}}"

   # output_string = utils.CYELLOW+utils.CFAINT+ f"{wait_time:>5}{wait_time_exit:<4}{identation}"+et_color+f"{element_time:>5}"+utils.CDARK_GRAY+f"{soql_total_queries_delta:>4}" +utils.CEND + Cinit +f"    {output_string}"
   # output_string = utils.CYELLOW+utils.CFAINT+ f"{identation}"+f"{element_time:<{times_lenght}}"+utils.CYELLOW+utils.CFAINT+f"{soql_total_queries_delta:>4}" +utils.CEND + Cinit +f"    {output_string}"
    output_string = utils.CYELLOW+utils.CFAINT+ f"{'':<{level}}"+f"{element_time:<{times_lenght}}"+utils.CYELLOW+utils.CFAINT+f"{soql_total_queries_delta:>4}" +utils.CEND + Cinit +f"    {utils.CYELLOW}{utils.CFAINT}{level} {utils.CEND}{Cinit}{output_string}"

    print(f"{time_stamp_entry:12}{s}{time_stamp_exit:12}{s}{time_ms:>8}{s}{cpu_time_entry:>6}{s}{cpu_time_elapsed:6}{s}{soql_total_queries_entry:>3}{s}{utils.CGREEN}{soql_queries_entry:>3}{utils.CEND}{s}{soql_queries_cmt_entry:>3}{s}{utils.CYELLOW}{(Qmct_estimate):>3}{utils.CEND}{s}{element_type_color}{element_type:21}{utils.CEND}{s}{apex_line_number:>4}{s}{output_string:50}"+utils.CEND)



