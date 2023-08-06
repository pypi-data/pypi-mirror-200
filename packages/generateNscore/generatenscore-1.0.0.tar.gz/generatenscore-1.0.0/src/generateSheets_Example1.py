import generate_score as gNs

QGs=[]
Q=['Submit the acceleration, in unit of m/s², of an object of {%vM%} kg when the force of {%vF%} N is acted upon.',
   'Sumbit the force in unit of N to give an object of {%vM%} kg acceleration of {%round(vF/vM,3)%} m/s².']
A='''data=[]
vM=random.randint(1,10)
vF=random.randint(10,30)
answer=[vF/vM, vM*round(vF/vM,3)]'''

QGs.append([Q, A, ('chap3', 'qg5'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.',
   'Submit the product of the two integers {%vA%} and {%vB%}.',
   'Subtract {%vA%} from {%vB%} and submit your answer.']

A='''data=[]
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[vA+vB, vA*vB, vB-vA]'''

QGs.append([Q, A, ('chap3', 'qg5_일반'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.',
   'Submit the product of the two integers {%vA%} and {%vB%}.',
   'Subtract {%vA%} from {%vB%} and submit your answer.']

A='''data=[]
from userfunctions11 import func1
vA, vB = func1()
answer=[vA+vB, vA*vB, vB-vA]'''

QGs.append([Q, A, ('chap3', 'qg5_udf'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.']

A='''data=[]
choices=[(random.randint(10,30), random.randint(10,30)) for _ in range(10)]
choice=random.choice(range(len(choices)))
ans=choices[choice]
vA, vB=ans
answer=[{'choices': [a+b for a, b in choices], 'ans': sum(ans)}]'''

QGs.append([Q, A, ('chap3', 'qg5_choices'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.', 'Submit the sum of the two integers {%vA%} and {%vB%}.']

A='''data=[]
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[{'choices':None, 'ans':vA+vB, 'fn': 'variation0_int'}, vA+vB]'''

QGs.append([Q, A, ('chap3', 'qg5_variation0_int'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.']

A='''data=[]
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[{'choices':None, 'ans':vA+vB, 'fn': 'variation0_int_5Add'}]'''

QGs.append([Q, A, ('chap3', 'qg5_variation0_int_5Add'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.figure(clock)']

A='''data=[]
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[{'choices':None, 'ans':vA+vB, 'fn': 'variation0_int_5Add'}]'''

QGs.append([Q, A, ('chap3', 'qg5_variation0_int_5Add_clock'), 'short'])


Q=['What is the correct function shown on right?<br>figure(graph)<br>init({%prms%});']

A='''data=[]
choices=[]
for _ in range(6):
  b=random.choice([-4, -3,-2,-1, 0, 1, 2, 3, 4])
  c=random.choice([-4, -3,-2,-1, 0, 1, 2, 3, 4])
  choices.append([[1, b, c], [-5,5]])

indx=random.choice(range(len(choices)))
ansValue=choices[indx]
eqs=[]
term1=lambda v: '+ x' if v==1 else '- x' if v==-1 else f'+ {v}x' if v>0 else f'- {-v}x' if v<0 else ''
term2=lambda v: f'+ {v}' if v>0 else f'- {-v}' if v<0 else ''
eqs = []
for aj, _ in choices: eqs.append(f'EQ% x^2 {term1(aj[1])} {term2(aj[2])} %EQ')

answer=[{'choices':eqs, 'ans':eqs[indx]}]
prms=choices[indx]'''

QGs.append([Q, A, ('chap3', 'qg5_variation0_int_5Add_graph'), 'short'])

Q=['What is the correct function of {%eq%}?figure(graphF)']

A='''data=[]
choices=[]
for _ in range(10):
  b=random.choice([-4, -3,-2,-1, 0, 1, 2, 3, 4])
  c=random.choice([-4, -3,-2,-1, 0, 1, 2, 3, 4])
  choices.append([[1, b, c], [-5,5]])

indx=random.choice(range(len(choices)))

term1=lambda v: '+ x' if v==1 else '- x' if v==-1 else f'+ {v}x' if v>0 else f'- {-v}x' if v<0 else ''
term2=lambda v: f'+ {v}' if v>0 else f'- {-v}' if v<0 else ''
eq=f'EQ% x^2 {term1(choices[indx][0][1])} {term2(choices[indx][0][2])} %EQ'

cnvss=[f'<div id="canvas{j}"></div>' for j, choice in enumerate(choices)]
cnvss = []
xtra = []
for j, choice in enumerate(choices):
  cnvss.append(f'<div id="cnvs{j}"></div>')
  xtra.append(f'graphF("cnvs{j}", {choice});')
answer=[{'choices':cnvss, 'ans':cnvss[indx], 'cols':xtra}]'''

QGs.append([Q, A, ('chap3', 'qg5_variation0_int_5Add_graph2'), 'short'])





clock='''cnvs.width=300;cnvs.height=300;ctx.clearRect(0,0, cnvs.width, cnvs.height);var width= 300;var height = width;cnvs.width = width;cnvs.height = height;var radius = cnvs.height/2;ctx.translate(radius, radius);radius = radius * 0.90;function drawFace(ctx, radius) {  ctx.beginPath();  ctx.arc(0, 0, radius, 0, 2*Math.PI);  ctx.fillStyle = "white";  ctx.fill();  ctx.strokeStyle = "black";  ctx.stroke();}function drawNumbers(ctx, radius) {  var ang;  var num;  ctx.font = radius*0.15 + "px arial";  ctx.textBaseline="middle";  ctx.fillStyle = "black";  ctx.textAlign="center";  for(num = 1; num < 13; num++){    ang = num * Math.PI / 6;    ctx.rotate(ang);    ctx.translate(0, -radius*0.85);    ctx.rotate(-ang);    ctx.fillText(num.toString(), 0, 0);    ctx.rotate(ang);    ctx.translate(0, radius*0.85);    ctx.rotate(-ang);  }}function drawHand(ctx, pos, length, width) {    ctx.beginPath();    ctx.lineWidth = width;    ctx.lineCap = "round";    ctx.moveTo(0, 0);    ctx.rotate(pos);    ctx.lineTo(0,-length);    ctx.stroke();    ctx.rotate(-pos);}drawFace(ctx, radius);drawNumbers(ctx, radius);var hour=10;var minute=10;hour=hour%12;hour=hour*Math.PI/6 + minute*Math.PI/(6*60);drawHand(ctx, hour, radius*0.5, radius*0.04);minute=(minute*Math.PI/30);drawHand(ctx, minute, radius*0.8, radius*0.02);'''

figures={'clock':clock}

graph='''var argsFromMain=null;function init(prms) {argsFromMain=prms;}
//init(); if (argsFromMain == null) {argsFromMain=[[1, 1, -2], [-5, 5]];}const height = 200;cnvs.height = height;cnvs.width=height;const N=51;const aj=argsFromMain[0], xlim=argsFromMain[1];const dx=(xlim[1]-xlim[0])/(N-1);yMin=Math.floor(aj[2]-aj[1]*aj[1]/4-1);const ylim=[yMin, yMin+10];const xPole=-aj[1]/2;var x=[], y=[], v;for (j=0; j<N; j++) {  v=xlim[0]+j*dx; w=aj[0]*v**2 + aj[1]*v + aj[2];  if (yMin<w && w<yMin+10) {x.push(v); y.push(w);}}function x2cnvs(x) {return bOrigX+pxl2x*(x-xlim[0]);}function y2cnvs(y) {return bOrigY+bL-pxl2x*(y-ylim[0]);}const bOrigX=0.5, bOrigY=0.5, bL=height, pxl2x=bL/(xlim[1]-xlim[0]);ctx.beginPath();ctx.fillStyle="#eee";ctx.fillRect(bOrigX, bOrigY, bL, bL);ctx.strokeStyle="#ccc";for (let j=xlim[0]; j<=xlim[1]; j++) { px=x2cnvs(j); ctx.moveTo(px, bOrigY); ctx.lineTo(px, bOrigY+bL);ctx.stroke();}for (let j=Math.ceil(ylim[0]); j<=Math.floor(ylim[1]); j++) { py=y2cnvs(j); ctx.moveTo(bOrigX, py); ctx.lineTo(bOrigX+bL, py);ctx.stroke();}ctx.beginPath();ctx.strokeStyle="blue"; py=y2cnvs(0); ctx.moveTo(bOrigX, py); ctx.lineTo(bOrigX+bL, py); ctx.stroke();ctx.beginPath();ctx.strokeStyle="blue"; px=x2cnvs(0); ctx.moveTo(px, bOrigY); ctx.lineTo(px, bOrigY+bL); ctx.stroke();ctx.beginPath();ctx.font="normal 14px Arial";ctx.fillStyle="blue";ctx.fillText("O", x2cnvs(0)-15,y2cnvs(0)+15);ctx.fillText("x", bOrigX+bL-10,y2cnvs(0)-3);ctx.fillText("y", x2cnvs(0)-12, bOrigY+13);for (j=ylim[0]+1; j<ylim[1]; j++) {  if (j%2 == 0) {     if (j<0) {ctx.fillText(j.toString(), x2cnvs(0)-15,y2cnvs(j)+5);}     else if (j>0) {ctx.fillText(j.toString(), x2cnvs(0)-10,y2cnvs(j)+5);}  }}ctx.fillText("-4", x2cnvs(-4)-8,y2cnvs(0)+12);ctx.fillText("-2", x2cnvs(-2)-8,y2cnvs(0)+12);ctx.fillText("2", x2cnvs(2)-4,y2cnvs(0)+12);ctx.fillText("4", x2cnvs(4)-4,y2cnvs(0)+12);ctx.beginPath();ctx.strokeStyle="black";ctx.moveTo(x2cnvs(x[0]), y2cnvs(y[0]));for (j=1; j<N; j++) {ctx.lineTo(x2cnvs(x[j]), y2cnvs(y[j]));}ctx.stroke();ctx.beginPath();for (j=0; j<N; j++) {ctx.beginPath();  ctx.arc(x2cnvs(x[j]),y2cnvs(y[j]),2,0, 2*Math.PI);  ctx.stroke();}
'''

graphF='''function graphF(cnvsName, prms) {
var cnvs = document.createElement("canvas");
div = document.getElementById(cnvsName);
div.appendChild(cnvs);
var ctx = cnvs.getContext("2d");
'''

graphF = graphF+graph+'}'

figures['graph']=graph
figures['graphF']=graphF.replace('//init();', 'init(prms);')




name='checkups1'
heading='Testing'
STDs={'12345678': 'oooo'}

iMultipleChoices=False

a=gNs.work(name, heading, STDs, QGs, True, iMultipleChoices, False)
gNs.mkHTMLs(a, figures)
