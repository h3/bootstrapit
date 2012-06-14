#firt lines of variables.less

content = """// Variables.less
// Variables to customize the look and feel of Bootstrap
// -----------------------------------------------------

// Type Test
// -------------------------
//@fluidGridColumnWidth:    6.382978723%;
@iconSpritePath:          "../img/glyphicons-halflings.png";
@sansFontFamily:        "Helvetica Neue", Helvetica, Arial, sans-serif;
@fluidGridColumnWidth:      1% * ((@gridColumnWidth * 100) / @gridRowWidth);
@linkColorHover:        darken(@linkColor, 15%);
@bodyBackground:        @white;
@baseFontFamily:        @sansFontFamily;
@black:                 #000;
@baseFontSize:          13px;
//@fluidGridColumnWidth:    6.382978723%;
@zindexDropdown:          1000;
"""

class TYPE:
    Color=1
    Pix=2
    Percent=3
    Nombre=4
    Txt=5
    File=6
    Reference=7
    Calulate=8

    Unknow=404

class obj:

    def __init__(self,name,app,type,value=0):
        self.name = name
        self.app = app
        self.type = type
        self.value = value

    def __str__(self):
        return "%s %d %s" % (self.name,self.type,self.value)
    
def ComType(txt,nb_line):
    size = len(txt)
    if txt[-1] == ';':
        return None
    if size >=5:
        if nb_line < 5:
            return "desc"
        if txt[4].islower():
            return "small"
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

def main():
    var = []
    last_big_title =""
    last_small_title = ""
    last_des = ""
    nb_line  = 0 
    for line in content.split('\n'):
        line = line.strip()
        nb_line += 1
        if len(line)< 5:
            continue
        if line.startswith('//'):
            if line[3] == line[4] and line[4] == "-":
                continue
            d = ComType(line,nb_line)
            if d == "small":
                last_small_title = line
            elif d == "big":
                last_big_title = line
            else:
                last_des = line
            continue
        print last_big_title,last_small_title,last_des

        line = line.split(':')[1].strip()
        o = None
        if '"' in line or "'" in line:
            o = obj(last_big_title,last_small_title,TxtType(line),line)

        elif any(('(' in line,'+' in line,'*' in line,'-' in line,' / ' in line)):
            o = obj(last_big_title,last_small_title,TYPE.Reference,line)
        elif '@' in line:
            o = obj(last_big_title,last_small_title,TYPE.Reference,tofloat(line))
        elif '#' in line:
            o = obj(last_big_title,last_small_title,TYPE.Color,tofloat(line))
        elif 'px' in line:
            o = obj(last_big_title,last_small_title,TYPE.Pix,tofloat(line))
        elif "%" in line:
            o = obj(last_big_title,last_small_title,TYPE.Percent,tofloat(line))


#        print o

main()





