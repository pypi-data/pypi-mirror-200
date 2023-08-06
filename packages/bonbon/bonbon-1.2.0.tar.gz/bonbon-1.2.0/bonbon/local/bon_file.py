"""
Data read functions:
    rstring, rlines, rjson, rcsv, rparquet
Write functions:
    wstring, astring, wjson, wcsv
Path utilities:
    mdir, puser, pdownloads, pjson
"""

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
    """Read and return string from ~/Downloads/targetFile.

    Args:
        *args: target file path
        e.g., s=rstring('folder1','notes.txt')
    
    Return:
        string in target file
    """
    with open(pdownloads(*args), 'r', encoding='utf-8') as f:
        s = f.read()
        return s

def wstring(s, *args):
    """Write string s to ~/Downloads/targetFile

    Args:
        s: string to write
        *args: target file path
        e.g., wstring(s, 'folder1','notes.txt')
    
    Return:
        None
    """
    with open(pdownloads(*args), 'w') as f:
        f.write(s)

def astring(s, *args):
    """Append string s as a new line to ~/Downloads/targetFile

    Args:
        s: string to append 
        *args: target file path
        e.g., astring(s, 'folder1','notes.txt')
    
    Return:
        None
    """
    with open(pdownloads(*args), 'a') as f:
        f.write(f"\n{s}")

def rlines(*args):
    """Read string in lines/list from ~/Downloads/targetFile

    Args:
        *args: target file path
        e.g., lines = rlines('folder1','notes.txt')
    
    Return:
        string in lines/list
    """
    with open(pdownloads(*args), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return lines

def rjson(*args):
    """Read json from ~/Downloads/targetFile

    Args:
        *args: target file path
        e.g., js = rjson('folder1','notes.json')
    
    Return:
        JSON format string
    """
    with open(pdownloads(*args), 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)

def wjson(js, *args):
    """Write JSON string to ~/Downloads/targetFile

    Args:
        s: JSON string to write
        *args: target file path
        e.g., wjson(s, 'folder1','notes.json')
    
    Return:
        None
    """
    with open(pdownloads(*args), 'w') as f:
        f.write(json.dumps(js, default=_datetime_handler,
                    sort_keys=False, indent=2))

def pjson():
    """Parse json files under ~/Downloads/ and save copy under ~/Downloads/JSON/

    Args:
        *args: None
        e.g., pjson()
    
    Return:
        None
    """
    json_files = [pos_json for pos_json in os.listdir(pdownloads()) if pos_json.endswith('.json')]
    for jfn in json_files:
        js = rjson(jfn)
        mdir(pdownloads('JSON'))
        wjson(js, 'JSON', jfn)

def rcsv(*args):
    """Read csv from ~/Downloads/targetFile

    Args:
        *args: target file path
        e.g., dicts = rjson('folder1','notes.csv')
    
    Return:
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
    """Write csv (format of dict list) to ~/Downloads/targetFile

    Args:
        s: list of dicts to write
        *args: target file path
        e.g., wcsv(s, 'folder1','notes.json')
    
    Return:
        None
    """
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
    """Read parquet from ~/Downloads/targetFile

    Args:
        *args: target file path
        e.g., pqt = rparquet('folder1','notes.parquet')
    
    Return:
        Return parquet in json format
    """
    df = DataFrame(pq.read_table(pdownloads(*args)).to_pandas())
    arr = list(args)
    t = arr.pop()
    arr.append('JSON')
    mdir(pdownloads(*arr))
    arr.append(f"{t}.json")
    return df.to_json(pdownloads(*arr), orient='records')

def pdownloads(*args):
    """ Configure file path to start with ~/Downloads/

    Args:
        *args: target file path
        e.g., path = pdownloads('A','B','C.json')
    
    Return:
        File path connects ~/Downloads/ with given args.
    """
    arr = list(args)
    arr.insert(0,'Downloads')
    return os.path.join(os.path.expanduser('~'), *arr)

def puser(*dirs):
    """ Configure file path to start with ~/

    Args:
        *args: target file path
        e.g., path = puser('A','B','C.json')
    
    Return:
        File path connects ~/ with given args.
    """
    file_path = os.path.join(os.path.expanduser('~'))
    return os.path.join(file_path, *dirs)

def mdir(file_path):
    """ Generate dir with given file path.

    Args:
        file_path: given file path
        e.g., mdir('./A/New/Folder')
    
    Return:
        None
    """
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
