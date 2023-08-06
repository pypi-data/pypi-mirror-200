import generateNscore as gNs


Q=['Submit the sum of the two integers {%vA%} and {%vB%}.',
   'Submit the product of the two integers {%vA%} and {%vB%}.',
   'Subtract {%vA%} from {%vB%} and submit your answer.']
A='''data=[]
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[vA+vB, vA*vB, vB-vA]'''

QGs=[[Q, A, ('chap1', 'qg1'), 'short']]

Q=['Submit the acceleration, in unit of m/s², of an object of {%vM%} kg when the force of {%vF%} N is acted upon.',
   'Sumbit the force in unit of N to give an object of {%vM%} kg acceleration of {%round(vF/vM,3)%} m/s².']
A='''data=[]
vM=random.randint(1,10)
vF=random.randint(10,30)
answer=[vF/vM, vM*round(vF/vM,3)]'''

QGs.append([Q, A, ('chap3', 'qg5'), 'short'])

Q=['The figure below shows a vector, in red, with θ = {%theta%}° and a vector magnitude of {%mag%}. Submit the x coordinate component. figure(vector)',
   'The figure below shows a vector, in red, with θ = {%theta%}° and a vector magnitude of {%mag%}. Submit the y coordinate component. figure(vector)']
A='''data=[]
theta=random.randint(5, 85)
mag=random.randint(3,10)
answer=[mag*math.cos(math.radians(theta)), mag*math.sin(math.radians(theta))]'''

QGs.append([Q, A, ('chap3', 'qg5'), 'short'])

Q=['The figure below shows a vector, in red, with θ = {%theta%}° and a vector magnitude of {%mag%}. Submit the x coordinate component. figure(vector)<br>init({%prms%});',
   'The figure below shows a vector, in red, with θ = {%theta%}° and a vector magnitude of {%mag%}. Submit the y coordinate component. figure(vector)<br>init({%prms%});']
A='''data=[]
theta=random.randint(25, 165)
mag=random.randint(3,10)
answer=[mag*math.cos(math.radians(theta)), mag*math.sin(math.radians(theta))]
prms=[theta, mag]'''

QGs.append([Q, A, ('chap3', 'qg5B'), 'short'])

Q=['What time is the clock shown below?<br><br>figure(clock)<br>init({%prms%});']
A='''data=[]
answers = [f'{random.choice(range(1,12))}:{random.choice(range(5,60,5))}' for _ in range(random.choice(range(5,10)))]
ans=random.choice(answers)
answer=[{'choices':answers, 'ans':ans}]
vH, vM=[int(s) for s in ans.split(':')]
prms=[300, vH, vM]'''

QGs.append([Q, A, ('chap6', 'qg1'), 'choice'])

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


figures={'vector': vector, 'clock': clock}



def example6A(iMultipleChoices=False):
    # This example shows what each question with a figure included looks like in HTML format.
    # This particular example demonstrates a multi-choice question.
    name='checkups' # do not change
    heading='Testing' # do not change
    STDs={'12345678': 'oooo'} # do not change

    a=gNs.work(name, heading, STDs, QGs, True, iMultipleChoices, False)
    gNs.mkHTMLs(a, figures)
    #a.saveWork()


def example6B(iMultipleChoices=False, iShuffling=False):
    # This example demonstrates the generation a set of question sheets in HTML format for a set of students whose identification numbers are read from a csv file.
    name='ex6'
    heading='Homework'
    #STDs={'22332213': '홍길동 (GilDong Hong)' , '28193278':'이몽룡 (Mong ryong Lee)', '98123522': 'Weeny Tiny'}
    STDs=gNs.common.getStudList('출석부.csv','학번','학생명') # "utf-8" encoding의 csv file.

    a=gNs.work(name, heading, STDs, QGs, False, iMultipleChoices, iShuffling)
    gNs.mkHTMLs(a, figures)
    a.saveWork()

if __name__ == '__main__':
    #example6B(True, True)
    example6A(False)
