import json

class TYPE:

    Color="#"
    Pix="px"
    Percent="%"
    Nombre="nb"
    Txt="txt"
    File="file"
    Reference="ref"
    Calulate="calc"

    Unknow="404"

class obj:

    def __init__(self,name,app,subapp,type,value=0):
        self.name = name
        self.app = app
        self.subapp = subapp
        self.type = type
        self.value = value

    def __str__(self):
        return "<%s> <%s>.<%s> <%s> <%s>" % (self.name,self.app,self.subapp,self.type,self.value)

    def todict(self):
        return {
                #'name' : self.name,
                'app' : self.app,
                'subapp' : self.subapp,
                'type' : self.type,
                'value' : self.value}
    
def ComType(txt,nb_line):
    size = len(txt)
    if txt[-1] == ';':
        return None
    if size >=5:
        if nb_line < 10:
            return "desc"
        if txt[4].islower() and not txt[3].islower():
            return "small"
        elif not txt[3].islower() and not txt[4].islower() and not any(('-' in txt[4],'/' in txt[4], "_" in txt[4])):
            nb_line = 0
            return "big"
    return None

def TxtType(txt):
    if '../' in txt:
        return TYPE.File
    return TYPE.Txt

import re
def tofloat(txt):
    i = ''.join(re.findall(r'[\d.]+',txt))
    if i:
        return float(i)
    return None

def FileVarToJson(filename):
    vars = {}
    last_big_title =""
    last_small_title = ""
    last_des = ""
    nb_line  = 10
    content =  file(filename,'r').read().split('\n')[3:]
    for line in content:
        line = line.strip()
        nb_line += 1
        if len(line)< 5:
            continue
        if line.startswith('//'):
            if line[3] == line[4] and line[4] == "-":
                continue
            d = ComType(line,nb_line)
            if d == "small":
                last_small_title = line[2:].strip()
            elif d == "big":
                last_big_title = line[2:].strip()
            else:
                last_des = line[2:].strip()
            continue
        #print [last_big_title,last_small_title,last_des]

        var,line = line.split(':')
        line = line.strip().replace(';','')
        var = var.replace('@','').strip()
        o = None
        if '"' in line or "'" in line:
            o = obj(var,last_big_title,last_small_title,TxtType(line),line)

        elif any(('(' in line,'+' in line,'*' in line,'-' in line,' / ' in line)):
            o = obj(var,last_big_title,last_small_title,TYPE.Calulate,line)
        elif '@' in line:
            o = obj(var,last_big_title,last_small_title,TYPE.Reference,line)
        elif '#' in line:
            o = obj(var,last_big_title,last_small_title,TYPE.Color,line.replace('#',''))
        elif 'px' in line:
            o = obj(var,last_big_title,last_small_title,TYPE.Pix,tofloat(line))
        elif "%" in line:
            o = obj(var,last_big_title,last_small_title,TYPE.Percent,tofloat(line))
        else:
            try:
                f = float(line)
                o = obj(var,last_big_title,last_small_title,TYPE.Nombre,f)
            except:
                o = obj(var,last_big_title,last_small_title,TYPE.Txt,line)
        vars.update({var :o.todict()})

    return json.dumps(vars)
    
#print FileVarToJson('../less/variables.less')



