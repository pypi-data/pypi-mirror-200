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

figures={}


def example2(iMultipleChoices=False, iShuffling=False):
    # This example demonstrates the generation a set of question sheets in HTML format.
    name='ex2'
    heading='Homework'
    STDs={'22332213': '홍길동 (GilDong Hong)' , '28193278':'이몽룡 (Mong ryong Lee)', '98123522': 'Weeny Tiny'}

    a=gNs.work(name, heading, STDs, QGs, False, iMultipleChoices, iShuffling)
    gNs.mkHTMLs(a, figures)
    a.saveWork()


if __name__ == '__main__':
    example2(True, True)
