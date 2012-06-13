#firt lines of variables.less

content = """// Variables.less
// Variables to customize the look and feel of Bootstrap
// -----------------------------------------------------



// GLOBAL VALUES
// --------------------------------------------------


// Grays
// -------------------------
@black:                 #000;
@grayDarker:            #222;
@grayDark:              #333;
@gray:                  #555;
@grayLight:             #999;
@grayLighter:           #eee;
@white:                 #fff;
"""

class TYPE:
    Color=1
    Pix=2
    Percent=3
    Txt=4
    Unknow=404

class var:
    name =""
    type = TYPE.Unknow
    value =0
    

var = {}

for lines in content.split('\n'):
    pass

