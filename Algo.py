import PySimpleGUI as sg
import subprocess
import re
from os import path
import os

def write_file(fname, data, out_name):
    name = path.dirname(fname) + "\\"
    #n = str(name) + ('\\')
    #print(n)
    with open(name + out_name, 'w+') as f:
        [f.write(x+'\n') for x in data]

def proc_filter (str_proc):
    str_proc=str_proc.replace('\n','')
    res1=str_proc.split('","')
    if len(res1)==7:
        str_proc=res1[4]
        return str_proc
    else:
        return "\n"

def clear_file(file, file_system, logs='No use'):
    #subprocess.call()

    out = []

    if file_system == 'Windows' and logs == 'No use':
        with open(file, encoding='windows-1251') as f:
            uniq_lines = f.read().splitlines()
            out = sorted(set(uniq_lines))

    if file_system == 'Windows' and logs == 'No use':
        with open(file, encoding='utf-8') as f:
            uniq_lines = f.read().splitlines()
            out = sorted(set(uniq_lines))

    if file_system == 'Windows' and logs == 'ProcMonitor':
        with open(file, encoding='windows-1251') as f:
            name = path.dirname(file) + "\\" + "tmp.txt"
            with open(name, 'w+') as tmp:
                for line in f:
                    line=proc_filter(line)
                    tmp.write(line+'\n')
        
        with open(name, encoding='windows-1251') as f:
            uniq_lines = f.read().splitlines()
            out = sorted(set(uniq_lines))
            #name1 = path.dirname(file) + "\\" + "tmp1.txt"
            #with open(name1, 'w+') as tmp1:
                #write_file(tmp1, sorted(set(uniq_lines)), )

        #with open(name1, encoding='windows-1251') as f:
            #for line in f:
                #out.append(line)

        os.remove(name)
    #os.remove(name1)

    if file_system == 'Unix' and logs == 'ProcMonitor':
        with open(file, encoding='utf-8') as f:
            name = path.dirname(file) + "\\" + "tmp.txt"
            with open(name, 'w+') as tmp:
                for line in f:
                    line=proc_filter(line)
                    tmp.write(line+'\n')
        
        with open(name, encoding='windows-1251') as f:
            uniq_lines = f.read().splitlines()
            out = sorted(set(uniq_lines))
            #name1 = path.dirname(file) + "\\" + "tmp1.txt"
            #with open(name1, 'w+') as tmp1:
                #write_file(tmp1, sorted(set(uniq_lines)), )

        #with open(name1, encoding='windows-1251') as f:
            #for line in f:
                #out.append(line)

        os.remove(name)
    #os.remove(name1)

    if file_system == 'Unix' and logs == 'Strace':
        with open(file, encoding='utf-8') as f:
            name = path.dirname(file) + "\\" + "tmp.txt"
            with open(name, 'w+') as tmp:
                for line in f:
                    if 'openat' in line and '-1' not in line:
                        line = line[line.find('"') + 1:]  ##не работает len(line)-line.find('"')+1
                        line = line[:line.find('"')]
                        if 'openat' not in line:
                            tmp.write(line+'\n')

        """with open(name, encoding='windows-1251') as tmp:
            name1 = path.dirname(file) + "\\" + "tmp1.txt"
            with open(name1, 'w+') as tmp1:
                for line in tmp:
                    line = line[line.find('"') + 1:]  ##не работает len(line)-line.find('"')+1
                    line = line[:line.find('"')]
                    if 'openat' not in line:
                        tmp1.write(line+'\n')"""

        with open(name, encoding='windows-1251') as f:
            uniq_lines = f.read().splitlines()
            out = sorted(set(uniq_lines))

        os.remove(name)
                
                #for line in f:
                    #lines_exit = re.findall(r'openat\(\"(.*)\",.*\) = -1', line)
                    #if lines_exit==[]:
                        #lines_exit = re.findall(r'openat\(\"(.*)\",.*\)', line)
                        #for exit_line in lines_exit:
                            #tmp.write(exit_line+'\n')
    """if file_system == 'Windows':
        with open(file, encoding='windows-1251') as f:
            for line in f:
                out = re.findall(r'((((?<!\w)[A-Z,a-z]:)|(\.{1,2}\\))([^\b%\/\|:\n\"]*))', line)
            
    if file_system == 'Unix':
        with open(file, encoding='utf-8') as f:
            for line in f:
                out = re.findall(r'((?<!\w)(\.{1,2})?(?<!\/)(\/((\\\b)|[^ \b%\|:\n\"\\\/])+)+\/?)', line)

    if algo == 'Unix':
        print(file)
        file_input = open(file, "r")
        tmp = file_input.readlines()
        out = re.findall(r'((?<!\w)(\.{1,2})?(?<!\/)(\/((\\\b)|[^ \b%\|:\n\"\\\/])+)+\/?)', line)
        file_input.close()"""

    
    #print(type(out))
    #print(type(out[0]))
    return out

def comparsion(list1, list2, file1, out_name):
    tmp = frozenset(list2)
    out = [item for item in list1 if item not in tmp] #out = list1 - list2
    write_file(file1, out, out_name)

def file_comparsion(file1, file2, file_system, logs, clean_file1, clean_file2, izb, polnota):

    file1_lines = []
    file2_lines = []

    if clean_file1 == True:
        if file_system[0] == 'Windows':
            with open(file1, encoding='windows-1251') as f:
                file1_lines = f.read().splitlines()
                #for line in f:
                    #file1_lines.append(line)
        elif file_system[0] == 'Unix':
            with open(file1, encoding='utf-8') as f:
                file1_lines = f.read().splitlines()
                #for line in f:
                    #file1_lines.append(line)
    elif clean_file1 == False:
        file1_lines = clear_file(file1, file_system[0])

    if clean_file2 == True:
        if file_system[1] == 'Windows':
            with open(file2, encoding='windows-1251') as f:
                file2_lines = f.read().splitlines()
                #for line in f:
                    #file2_lines.append(line)
        elif file_system[1] == 'Unix':
            with open(file2, encoding='utf-8') as f:
                file2_lines = f.read().splitlines()
                #for line in f:
                    #ile2_lines.append(line)
    elif clean_file2 == False:
        file2_lines = clear_file(file2, file_system[1], logs)

    #write_file(file1, file1_lines, 'kek.txt')
    #write_file(file1, file2_lines, 'kek1.txt')

    if izb == True:
        comparsion(file1_lines, file2_lines, file1, 'Izbitocnosti.txt')

    if polnota == True:
        comparsion(file2_lines, file1_lines, file1, 'Polnota.txt')

    """tmp = frozenset(file2_lines)
    out = [item for item in file1_lines if item not in tmp] #out = file1 - file2
    write_file(file1, out)"""



layout = [
    [sg.Text('Исходные тексты'), sg.InputText(), sg.FileBrowse(), sg.Radio('CP-1251', "RADIO1"), sg.Radio('UTF-8', "RADIO1"), sg.Checkbox('Файл уже очищен'),],
    [sg.Text('Используемые файлы'), sg.InputText(), sg.FileBrowse(), sg.Radio('CP-1251', "RADIO2"), sg.Radio('UTF-8', "RADIO2"), sg.Checkbox('Файл уже очищен'),],
    [sg.Checkbox('Избыточность'), sg.Checkbox('Полнота'),],
    [sg.Radio('Strace', "RADIO3"), sg.Radio('ProcMonitor', "RADIO3")],
    [sg.Submit(), sg.Cancel()]
]


window = sg.Window('File comparison', layout)

while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Submit':
        file1 = file2 = isitago = None
        if values[0] and values[4]:
            file1 = re.findall('.+:\/.+\.+.', values[0])
            file2 = re.findall('.+:\/.+\.+.', values[4])
            isitago = 1
            if not file1 and file1 is not None:
                print('Error: File 1 path not valid.')
                isitago = 0
            elif not file2 and file2 is not None:
                print('Error: File 2 path not valid.')
                isitago = 0
            #elif values[1] is not True and values[2] is not True and values[4] is not True:
                print('Error: Choose at least one type of Encryption Algorithm')
            elif isitago == 1:
                print('Info: Filepaths correctly defined.')
                file_encoding = [] #algos to compare
                used_logs = [] # used logs name
                logs = ''
                if values[1] == True: file_encoding.append('Windows')
                if values[2] == True: file_encoding.append('Unix')
                if values[5] == True: file_encoding.append('Windows')
                if values[6] == True: file_encoding.append('Unix')
                if values[10] == True: logs = 'Strace'
                if values[11] == True: logs = 'ProcMonitor'
                filepaths = [] #files
                filepaths.append(values[0])
                filepaths.append(values[4])
                if file_encoding == []:
                    print('Enter system file')
                else: 
                    file_comparsion(filepaths[0], filepaths[1], file_encoding, logs, values[3], values[7], values[8], values[9])
                    """if hash(filepaths[0],algo) == hash(filepaths[1],algo):
                        print('Files match for ', algo)
                    else:
                        print('Files do NOT match for ', algo)"""
        else:
            print('Please choose 2 files.')
window.close()