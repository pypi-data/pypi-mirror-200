import generateNscore as gNs


QGs=[]
Q=['Select the {%vA%} one. ',
   'Select the {%vA%} one. ']

A='''data=[]
vA=random.choice(['correct', 'incorrect'])
import userfunctions2
choices, indx, ansValue = userfunctions2.func2(vA)
answer=[{'choices':choices, 'ans':choices[indx]}, {'choices':choices, 'ans':choices[indx]}]'''

QGs.append([Q, A, ('chap10', 'qg13'), 'choice'])


figures={}




def example10A(iMultipleChoices=False):
    # This example shows what each question with a figure included looks like in HTML format.
    name='checkups' # do not change
    heading='Testing' # do not change
    STDs={'12345678': 'oooo'} # do not change

    a=gNs.work(name, heading, STDs, QGs, True, iMultipleChoices, False)
    gNs.mkHTMLs(a, figures)
    #a.saveWork()


def example10B(iMultipleChoices=False, iShuffling=False):
    # This example demonstrates the generation a set of question sheets in HTML format.
    name='ex10'
    heading='Homework'
    STDs={'22332213': '홍길동 (GilDong Hong)' , '28193278':'이몽룡 (Mong ryong Lee)', '98123522': 'Weeny Tiny'}

    a=gNs.work(name, heading, STDs, QGs, False, iMultipleChoices, iShuffling)
    gNs.mkHTMLs(a, figures)
    a.saveWork()


if __name__ == '__main__':
    example10B(True, True)
