#firt lines of variables.less

content = """// Variables.less
// Variables to customize the look and feel of Bootstrap
// -----------------------------------------------------

// Type Test
// -------------------------
@black:                 #000;
@bodyBackground:        @white;
@linkColorHover:        darken(@linkColor, 15%);
@sansFontFamily:        "Helvetica Neue", Helvetica, Arial, sans-serif;
@baseFontSize:          13px;
@baseFontFamily:        @sansFontFamily;
@zindexDropdown:          1000;
@iconSpritePath:          "../img/glyphicons-halflings.png";
//@fluidGridColumnWidth:    6.382978723%;
@fluidGridColumnWidth:      1% * ((@gridColumnWidth * 100) / @gridRowWidth);
"""

class TYPE:
    Color=1
    Pix=2
    Percent=3
    Nombre=4
    Txt=5
    Img=6
    Reference=7
    Calulate=8

    Unknow=404

class var:
    name =""
    type = TYPE.Unknow
    value =0
    

var = {}

for lines in content.split('\n'):
    pass

