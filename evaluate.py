import datetime
from Brain import Brain
import pandas as pd
from evaluator import evaluator

BLUE = "\033[34m"
RESET = "\033[0m"
YELLOW = "\033[33m"
GREEN = "\033[32m"

benchmark_settings = {

'Proxifier': {
        'log_file': 'Proxifier/Proxifier_2k.log',
        'log_format': '\[<Time>\] <Program> - <Content>',
        'regex': [r'<\d+\ssec', r'([\w-]+\.)+[\w-]+(:\d+)?', r'\d{2}:\d{2}(:\d{2})*', r'[KGTM]B'],
        'delimiter': [r'\(.*?\)'],
        'tag': 0,
        'theshold': 3
    },
    'HDFS': {
        'log_file': 'HDFS/HDFS_2k.log',
        'log_format': '<Date> <Time> <Pid> <Level> <Component>: <Content>',
        'regex': [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'],
        'delimiter': [''],
        'tag': 0,
        'theshold': 2
        },

    'Hadoop': {
        'log_file': 'Hadoop/Hadoop_2k.log',
        'log_format': '<Date> <Time> <Level> \[<Process>\] <Component>: <Content>',
        'regex': [r'(\d+\.){3}\d+'],
        'delimiter': [],
        'tag': 1,
        'theshold': 6
        },

    'Spark': {
        'log_file': 'Spark/Spark_2k.log',
        'log_format': '<Date> <Time> <Level> <Component>: <Content>',
        'regex': [r'(\d+\.){3}\d+', r'\b[KGTM]?B\b', r'([\w-]+\.){2,}[\w-]+'],
        'delimiter': [],
        'tag': 0,
        'theshold': 4
        },

    'Zookeeper': {
        'log_file': 'Zookeeper/Zookeeper_2k.log',
        'log_format': '<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>',
        'regex': [r'(/|)(\d+\.){3}\d+(:\d+)?'],
        'delimiter': [],
        'tag': 1,
        'theshold': 3
        },

    'BGL': {
        'log_file': 'BGL/BGL_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>',
        'regex': [r'core\.\d+'],
        'delimiter': [],
        'theshold': 6
        },

    'HPC': {
        'log_file': 'HPC/HPC_2k.log',
        'log_format': '<LogId> <Node> <Component> <State> <Time> <Flag> <Content>',
        'regex': [],
        'delimiter': [],
        'theshold': 5
        },

    'Thunderbird': {
        'log_file': 'Thunderbird/Thunderbird_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>',
        'regex': [r'(\d+\.){3}\d+'],
        'delimiter': [],
        'theshold': 3
        },

    'Windows': {
        'log_file': 'Windows/Windows_2k.log',
        'log_format': '<Date> <Time>, <Level>                  <Component>    <Content>',
        'regex': [r'0x.*?\s'],
        'delimiter': [],
        'theshold': 3
        },

    'Linux': {
        'log_file': 'Linux/Linux_2k.log',
        'log_format': '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>',
        'regex': [r'(\d+\.){3}\d+', r'\d{2}:\d{2}:\d{2}',r'J([a-z]{2})'],
        'delimiter': [r''],
        'theshold': 4
        },

    'Android': {
        'log_file': 'Android/Android_2k.log',
        'log_format': '<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>',
        'regex': [r'(/[\w-]+)+', r'([\w-]+\.){2,}[\w-]+', r'\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b'],
        'delimiter': [r''],
        'theshold': 5
        },

    'HealthApp': {
        'log_file': 'HealthApp/HealthApp_2k.log',
        'log_format': '<Time>\|<Component>\|<Pid>\|<Content>',
        'regex': [],
        'delimiter': [r''],
        'theshold': 4
        },

    'Apache': {
        'log_file': 'Apache/Apache_2k.log',
        'log_format': '\[<Time>\] \[<Level>\] <Content>',
        'regex': [r'(\d+\.){3}\d+'],
        'delimiter': [],
        'theshold': 4
        },

    'OpenSSH': {
        'log_file': 'OpenSSH/OpenSSH_2k.log',
        'log_format': '<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>',
        'regex': [r'(\d+\.){3}\d+', r'([\w-]+\.){2,}[\w-]+'],
        'delimiter': [],
        'theshold': 6
        },

    'OpenStack': {
        'log_file': 'OpenStack/OpenStack_2k.log',
        'log_format': '<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>',
        'regex': [r'((\d+\.){3}\d+,?)+', r'/.+?\s ', r'\d+'],
        'delimiter': [],
        'theshold': 5,
        },

    'Mac': {
        'log_file': 'Mac/Mac_2k.log',
        'log_format': '<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>',
        'regex': [r'([\w-]+\.){2,}[\w-]+'],
        'delimiter': [],
        'theshold': 5
        },



}

benchmark_result=[]

for dataset, setting in benchmark_settings.items():
    print(BLUE+dataset+RESET)
    starttime = datetime.datetime.now()
    parse = Brain.format_log(
        log_format=setting['log_format'],
        indir='logs/')
    form = parse.format(setting['log_file'])
    content = form['Content']
    start = datetime.datetime.now()
    sentences = content.tolist()
    df_groundtruth=pd.read_csv('logs/' + dataset + '/' + dataset + '_2k.log_structured.csv',
                encoding='UTF-8', header=0)
    df_output,template_set= Brain.parse(sentences, setting['regex'], dataset, setting['theshold'], setting['delimiter'], starttime, efficiency=False, df_input=df_groundtruth.copy())
    Brain.save_result(dataset, df_output, template_set)
    f_measure, accuracy= evaluator.evaluate(df_groundtruth, df_output)
    GA= evaluator.get_GA(df_groundtruth, df_output)
    ED,ED_= evaluator.get_editdistance(df_groundtruth, df_output)
    benchmark_result.append([dataset, GA, f_measure,ED])
print('\n=== Overall evaluation results ===')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
df_result = pd.DataFrame(benchmark_result, columns=['Dataset',  'Group_accuracy', 'F1_score','Edit_distance'])
df_result.set_index('Dataset', inplace=True)
print(GREEN)
print(df_result)
print(RESET)
print("Average Group_accuracy= "+YELLOW+str(sum(df_result['Group_accuracy'])/len(df_result['Group_accuracy']))+RESET+ \
"   Average Edit_distance (without data clean) = "+YELLOW+str(sum(df_result['Edit_distance'])/len(df_result['Edit_distance']))+RESET)