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

class var:
    name =""
    app = ""
    type = TYPE.Unknow
    value =0
    

def ComType(txt):
    size = len(txt)
    if txt[-1] == ';'
        return None
    if size >=5:
        if txt[].islower():
            return "desc"
        return "app"
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

var = []
last_big_title =""
last_small_title = ""
last_des = ""
for line in content.split('\n'):
    if len(txt)< 5:
        continue

    if line.startswith('//'):
        type = ComType(line)

    if '"' in txt or "'" in txt:
        TxtType(line)

    if any('(' in line,'+' in line,'*' in line,'-' in line,' / ' in line):
        #calculate to ignore
        continue

    if '@' in line:
        continue

    if '#' in line:
        continue

    if 'px' in line:
        continue

    if "%" in line:
        continue







