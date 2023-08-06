import generateNscore as GnS
import os

Q = ['Submit the sum of {%vA%}+{%vB%}',
     'Submit the value of {%vA%}÷{%vB%}',
     'Submit the value of sin({%vA/10%}).']
A = '''data=[]
vA=random.choice(range(2, 10))
vB=random.choice(range(2, 10))
answer = [vA+vB, vA/vB, math.sin(vA/10)]
'''
QGs=[[Q, A, ('chap10', 'qg11'), 'short']]


Q=['What is the sum of {%ansValue%}?']
A='''data=[]
import userfunctions
choices, indx, ansValue = userfunctions.func1()
answer=[{'choices':choices, 'ans':choices[indx]}]'''

QGs.append([Q, A, ('chap10', 'qg12'), 'choice'])

Q=['Select the {%vA%} one. ',
   'Select the {%vA%} one. ']

A='''data=[]
vA=random.choice(['correct', 'incorrect'])
import userfunctions
choices, indx, ansValue = userfunctions.func2(vA)
answer=[{'choices':choices, 'ans':choices[indx]}, {'choices':choices, 'ans':choices[indx]}]'''

QGs.append([Q, A, ('chap10', 'qg13'), 'choice'])


Q=['What time is the clock shown below?<br><br>figure(clock)<br>init({%prms%});']
A='''data=[]
answers = [f'{random.choice(range(1,12))}:{random.choice(range(5,60,5)):02d}' for _ in range(random.choice(range(4,7)))]
ans=random.choice(answers)
answer=[{'choices':answers, 'ans':ans}]
vH, vM=[int(s) for s in ans.split(':')]
prms=[300, vH, vM]'''

QGs.append([Q, A, ('chap6', 'qg14'), 'choice'])

Q=['What is the sum of the two fill areas of the color drawn below?<br>figure(addFractions)<br>init({%prms%});']
A='''data=[]
import userfunctions
choices, indx, ansValue = userfunctions.func1B()
answer=[{'choices':choices, 'ans':choices[indx]}]
prms=ansValue'''

QGs.append([Q, A, ('chap10', 'qg12b'), 'choice'])

addFractions='''var argsFromMain=null;
function init(prms) {argsFromMain=prms;}
//init();
if (argsFromMain == null) {argsFromMain=[1, 2, 2, 3];}
var height = 300;
cnvs.height = height;
var radius = cnvs.height/2;
var cY = cnvs.height/2;
var cX = cnvs.width/2;
var radius = cY-20;

ctx.beginPath();
ctx.font="normal 60px Arial";
ctx.fillStyle="black";
ctx.fillText("+", cX-17, cY+20);

var angle = 2*Math.PI/argsFromMain[1];
for (let j=0; j<argsFromMain[1]; j++) {
  ctx.beginPath();
  ctx.moveTo(cX-radius-20, cY);
  ctx.strokeStyle="black";
  if (j<argsFromMain[0]) {ctx.fillStyle="#ed7";}
  else {ctx.fillStyle="white";}
  ctx.arc(cX-radius-20, cY, radius, j*angle, (j+1)*angle);
  ctx.lineTo(cX-radius-20, cY);
  ctx.fill();
  ctx.stroke();
}

angle = 2*Math.PI/argsFromMain[3];
for (let j=0; j<argsFromMain[3]; j++) {
  ctx.beginPath();
  ctx.moveTo(cX+radius+20, cY);
  ctx.strokeStyle="black";
  if (j<argsFromMain[2]) {ctx.fillStyle="#7ed";}
  else {ctx.fillStyle="white";}
  ctx.arc(cX+radius+20, cY, radius, j*angle, (j+1)*angle);
  ctx.lineTo(cX+radius+20, cY);
  ctx.fill();
  ctx.stroke();
}
'''


clock='''function drawFace(ctx, radius) {
ctx.beginPath();
ctx.arc(0, 0, radius, 0, 2*Math.PI);
ctx.fillStyle = "white";
ctx.fill();
ctx.strokeStyle = "black";
ctx.stroke();
}

function drawNumbers(ctx, radius) {
var ang; var num;
ctx.font = radius*0.15 + "px arial";
ctx.textBaseline="middle";
ctx.fillStyle = 'black';
ctx.textAlign="center";
  for (let num = 1; num < 13; num++) {
  ang = num * Math.PI / 6; ctx.rotate(ang);
  ctx.translate(0, -radius*0.85);
  ctx.rotate(-ang);
  ctx.fillText(num.toString(), 0, 0);
  ctx.rotate(ang);
  ctx.translate(0, radius*0.85);
  ctx.rotate(-ang);
  }
}

function drawHand(ctx, pos, length, width) {
ctx.beginPath();
ctx.lineWidth = width;
ctx.lineCap = "round";
ctx.moveTo(0, 0);
ctx.rotate(pos);
ctx.lineTo(0,-length);
ctx.stroke();
ctx.rotate(-pos);
}

function clock(hour, minute) {
ctx.translate(radius, radius);
radius = radius * 0.90;
drawFace(ctx, radius);
drawNumbers(ctx, radius);
hour=hour%12;
hour=hour*Math.PI/6 + minute*Math.PI/(6*60);
drawHand(ctx, hour, radius*0.5, radius*0.04);
minute=(minute*Math.PI/30);
drawHand(ctx, minute, radius*0.8, radius*0.02);
}

var argsFromMain=null;
function init(prms) {argsFromMain=prms;}
//init();
if (argsFromMain == null) {argsFromMain=[300, 10, 10];}
var width = 300;
var height = width;
cnvs.width = width;
cnvs.height = height;
var radius = cnvs.height/2;
clock(argsFromMain[1], argsFromMain[2]);'''


vector='''function lineArrow(context, fromx, fromy, tox, toy, color) {
var headlen = 7;
var dx = tox - fromx;
var dy = toy - fromy;
var angle = Math.atan2(dy, dx);
context.strokeStyle = color;
context.moveTo(fromx, fromy);
context.lineTo(tox, toy);
context.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
context.moveTo(tox, toy);
context.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
context.stroke();
}

var argsFromMain=null;
function init(prms) {argsFromMain=prms;}
//init();
if (argsFromMain == null) {argsFromMain=[30, 10];}

const cXo=350.5; const cYo=250.5;
lineArrow(ctx, cXo-10, cYo, cXo+200, cYo, "#000");
ctx.beginPath();
lineArrow(ctx, cXo, cYo+10, cXo, cYo-200, "#000");
ctx.font="normal 18px Arial";
ctx.fillStyle="black";
ctx.fillText("x", cXo+210, cYo+5);
ctx.font="normal 18px Arial";
ctx.fillStyle="black";
ctx.fillText("y", cXo-2, cYo-210);
const ang=-Math.PI*argsFromMain[0]/180;
const mag=argsFromMain[1]*20;
ctx.beginPath();
lineArrow(ctx, cXo, cYo, cXo+mag*Math.cos(ang), cYo+mag*Math.sin(ang), "#f00");
ctx.beginPath();
ctx.strokeStyle="black"; ctx.arc(cXo, cYo, 50, 2*Math.PI+ang, 0);
ctx.stroke(); ctx.font="normal 18px Arial";
ctx.beginPath();
ctx.fillStyle="black";
ctx.fillText("θ", cXo+35, cYo-5);'''

figures={'vector': vector, 'clock': clock, 'addFractions': addFractions}


def example9A(iMultipleChoices=False):
    # This example shows what each question with a figure included looks like in HTML format.
    name='checkups' # do not change
    heading='Testing' # do not change
    STDs={'12345678': 'oooo'} # do not change

    a=GnS.work(name, heading, STDs, QGs, True, iMultipleChoices, False)
    GnS.mkHTMLs(a, figures)
    #a.saveWork()


def example9B(iMultipleChoices=False, iShuffling=False):
    # This example demonstrates the generation a set of question sheets in HTML format.
    name='K0326d'
    heading='Homework'
    STDs={'22332213': '홍길동 (GilDong Hong)' , '28193278':'이몽룡 (Mong ryong Lee)', '98123522': 'Weeny Tiny'}

    a=GnS.work(name, heading, STDs, QGs, False, iMultipleChoices, iShuffling)
    GnS.mkHTMLs(a, figures)
    a.saveWork()


if __name__ == '__main__':
    example9A(True)
