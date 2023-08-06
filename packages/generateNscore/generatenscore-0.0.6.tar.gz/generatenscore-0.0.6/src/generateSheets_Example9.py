import generateNscore as gNs


Q=['What is the sum of {%ansValue%}?']
A='''data=[]
import userfunctions
choices, indx, ansValue = userfunctions.func1()
answer=[{'choices':choices, 'ans':choices[indx]}]'''

QGs=[[Q, A, ('chap10', 'qg11'), 'short']]

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

figures={'addFractions': addFractions}




def example9A(iMultipleChoices=False):
    # This example shows what each question with a figure included looks like in HTML format.
    name='checkups9' # do not change
    heading='Testing' # do not change
    STDs={'12345678': 'oooo'} # do not change

    a=gNs.work(name, heading, STDs, QGs, True, iMultipleChoices, False)
    gNs.mkHTMLs(a, figures)
    #a.saveWork()


def example9B(iMultipleChoices=False, iShuffling=False):
    # This example demonstrates the generation a set of question sheets in HTML format.
    name='ex9'
    heading='Homework'
    STDs={'22332213': '홍길동 (GilDong Hong)' , '28193278':'이몽룡 (Mong ryong Lee)', '98123522': 'Weeny Tiny'}

    a=gNs.work(name, heading, STDs, QGs, False, iMultipleChoices, iShuffling)
    gNs.mkHTMLs(a, figures)
    a.saveWork()


if __name__ == '__main__':
    example9B(True, True)
