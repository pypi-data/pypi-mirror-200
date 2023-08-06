import os,sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import re
import csv
import datetime
import json
import pyarrow.parquet as pq
from pandas import DataFrame

def rstring(*args):
    with open(pdownloads(*args), 'r', encoding='utf-8') as f:
        s = f.read()
        return s

def wstring(s, *args):
    with open(pdownloads(*args), 'w') as f:
        f.write(s)

def astring(s, *args):
    with open(pdownloads(*args), 'a') as f:
        f.write(f"\n{s}")

def rlines(*args):
    with open(pdownloads(*args), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return lines

def rjson(*args):
    with open(pdownloads(*args), 'r', encoding='utf-8') as f:
        s = f.read()
        js = json.loads(s)
        wjson(js, *args)
        return js 

def wjson(js, *args):
    arr = list(args)
    t = arr.pop()
    arr.append('JSON')
    mdir(pdownloads(*arr))
    arr.append(t)
    with open(pdownloads(*arr), 'w') as f:
        f.write(json.dumps(js, default=_datetime_handler,
                           sort_keys=False, indent=2))

def rcsv(*args):
    """
    Return list of dict.
    """
    with open(pdownloads(*args), encoding='utf-8-sig') as f:
        row_list = []
        lines = list(csv.reader(f, skipinitialspace=True))
        row_list = []
        headers = [x.strip() for x in lines[0]]
        for i in range(1, len(lines)):
            row_dict = {}
            row_values = lines[i]
            for j in range(0, len(row_values)):
                if not row_values[j] or row_values[j].lower() == 'null':
                    continue
                row_dict[headers[j]] = row_values[j]
            row_list.append(row_dict)
        return row_list

def wcsv(js, *args):
    with open(pdownloads(*args), 'w') as f:
        csv_writer = csv.writer(f)
        cnt = 0
        for row in js:
            if cnt == 0:
                headers = row.keys()
                csv_writer.writerow(headers)
                cnt += 1
            csv_writer.writerow(row.values())

def rparquet(*args):
    df = DataFrame(pq.read_table(pdownloads(*args)).to_pandas())
    arr = list(args)
    t = arr.pop()
    arr.append('JSON')
    mdir(pdownloads(*arr))
    arr.append(f"{t}.json")
    return df.to_json(pdownloads(*arr), orient='records')

def pjson():
    json_files = [pos_json for pos_json in os.listdir(pdownloads()) if pos_json.endswith('.json')]
    for jf in json_files:
        rjson(jf)

def pdownloads(*args):
    """ Return dir path under default Downloads with splat(*) dir components. """
    arr = list(args)
    arr.insert(0,'Downloads')
    return os.path.join(os.path.expanduser('~'), *arr)

def puser(*dirs):
    """ Return dir path under default user path with splat(*) dir components. """
    file_path = os.path.join(os.path.expanduser('~'))
    return os.path.join(file_path, *dirs)

def mdir(file_path):
    """ Generate dir with given file path. """
    try:
        os.makedirs(file_path, exist_ok=True)
    except OSError:
        print('Directory {} can not be created.'.format(file_path))

def _datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()

if __name__ == "__main__":
    print('### bon file ###')
    pjson()
