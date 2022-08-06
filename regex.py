import re
import csv
def name_surmame_on_colum(contacts_list_raw):
    dict_ = {}
    dubl_list = []
    contacts_list = []
    patern = re.compile("^([\w ]+)?,([\w ]+)?,([\w ]+)?,")
    patern2 = re.compile(r", [+78]+.+,")
    patern3 = re.compile(', ([78])(...)(...)(..)(..)(.+)?,')

    for num, row in enumerate(contacts_list_raw):
        for count in range(1,4):
            result = patern.match(', '.join(row))
            if len(result.group(count).split()) > 1:
                for n in range(len(result.group(count).split())):
                    contacts_list_raw[num][n + count - 1] = result.group(count).split()[n]

    for num, row in enumerate(contacts_list_raw):
        result = patern2.findall(', '.join(row))
        if result:
            contacts_list_raw[num][5] = result[0].replace('+', '').replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace(',', '')
    
    for row in contacts_list_raw:
        result = patern3.sub(r',+7(\2)\3-\4-\5 \6,',', '.join(row))
        contacts_list.append(result.split(','))
    
    for num, row in enumerate(contacts_list):
        if row[0] in dict_:
            for n, text in enumerate(contacts_list[dict_[row[0]]]):
                if len(contacts_list[num][n]) > len(text):
                    contacts_list[num][n] = contacts_list[num][n]
                else:
                    contacts_list[num][n] = text
            dubl_list.append(dict_[row[0]])
        dict_[row[0]] = num
    for del_ in reversed(dubl_list):
        contacts_list.pop(del_)
    return(contacts_list)
if __name__ == '__main__':
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list_raw = list(rows)
        contacts_list_true = name_surmame_on_colum(contacts_list_raw)
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list_true)
