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

QGs.append([Q, A, ('chap3', 'qg3'), 'short'])

Q=['The figure below shows a vector, in red, with θ = {%theta%}° and a vector magnitude of {%mag%}. Submit the x coordinate component. figure(vector)',
   'The figure below shows a vector, in red, with θ = {%theta%}° and a vector magnitude of {%mag%}. Submit the y coordinate component. figure(vector)']
A='''data=[]
theta=random.randint(5, 85)
mag=random.randint(1,10)
answer=[mag*math.cos(math.radians(theta)), mag*math.sin(math.radians(theta))]'''

QGs.append([Q, A, ('chap3', 'qg5'), 'short'])

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

lineArrow(ctx, 140, 250.5, 350, 250.5, "#000");
ctx.beginPath();
lineArrow(ctx, 150.5, 260, 150.5, 50, "#000");
ctx.font="normal 18px Arial";
ctx.fillStyle="black";
ctx.fillText("x", 360, 255);
ctx.font="normal 18px Arial";
ctx.fillStyle="black";
ctx.fillText("y", 148, 41);
const ang=-Math.PI*argsFromMain[0]/180;
const mag=argsFromMain[1]*20;
ctx.beginPath();
lineArrow(ctx, 150.5, 250.5, 150.5+mag*Math.cos(ang), 250.5+mag*Math.sin(ang), "#f00");
ctx.beginPath();
ctx.strokeStyle="black"; ctx.arc(150.5, 250.5, 50, 2*Math.PI+ang, 0);
ctx.stroke(); ctx.font="normal 18px Arial";
ctx.beginPath();
ctx.fillStyle="black";
ctx.fillText("θ", 203, 240);'''

figures={'vector': vector}


def example3A(iMultipleChoices=False):
    # This example shows what each question with a figure included looks like in HTML format..
    name='checkups' # do not change
    heading='Testing' # do not change
    STDs={'12345678': 'oooo'} # do not change

    a=gNs.work(name, heading, STDs, QGs, True, iMultipleChoices, False)
    gNs.mkHTMLs(a, figures)
    #a.saveWork()


def example3B(iMultipleChoices=False, iShuffling=False):
    # This example demonstrates the generation a set of question sheets in HTML format.
    name='ex3'
    heading='Homework'
    STDs={'22332213': '홍길동 (GilDong Hong)' , '28193278':'이몽룡 (Mong ryong Lee)', '98123522': 'Weeny Tiny'}

    a=gNs.work(name, heading, STDs, QGs, False, iMultipleChoices, iShuffling)
    gNs.mkHTMLs(a, figures)
    a.saveWork()

if __name__ == '__main__':
    example3A(False)
