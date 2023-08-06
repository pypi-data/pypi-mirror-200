import generateNscore as gNs


Q=['Submit the sum of the two integers {%vC%} and {%vB%}.',
   'Submit the product of the two integers {%vA%} and {%vB%}.',
   'Subtract {%vA%} from {%vB%} and submit your answer.']
A='''data=[]
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[vA+vB, vA*vB, vB-vA]'''

QGs=[[Q, A, ('chap1', 'err1'), 'short']]


Q=['Submit the sum of the two integers {%vA%} and {%vB%}.',
   'Submit the product of the two integers {%vA%} and {%vB%}.',
   'Subtract {%vA%} from {%vB%} and submit your answer.']
A='''
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[vA+vB, vA*vB, vB-vA]'''

QGs.append([Q, A, ('chap1', 'err2'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.',
   'Submit the product of the two integers {%vA%} and {%vB%}.',
   'Subtract {%vA%} from {%vB%} and submit your answer.']
A='''data=[]
vA=random.randin(10,30)
vB=random.randint(10,30)
answer=[vA+vB, vA*vB, vB-vA]'''

QGs.append([Q, A, ('chap1', 'err3'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.',
   'Submit the product of the two integers {%vA%} and {%vB%}.',
   'Subtract {%vA%} from {%vB%} and submit your answer.']
A='''data=[]
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[]'''

QGs.append([Q, A, ('chap1', 'err4'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.',
   'Submit the product of the two integers {%vA%} and {%vB%}.',
   'Subtract {%vA%} from {%vB%} and submit your answer.']
A='''data=[]
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[vA+vB, vA*vB]'''

QGs.append([Q, A, ('chap1', 'err5'), 'short'])

Q=['Submit the sum of the two integers {%vA%} and {%vB%}.',
   'Submit the product of the two integers {%vA%} and {%vB%}.',
   'Subtract {%vA%} from {%vB%} and submit your answer.']
A='''data=[]
vA=random.randint(10,30)
vB=random.randint(10,30)
answer=[vA+vB, vA*B, vA-vB]'''

QGs.append([Q, A, ('chap1', 'err6'), 'short'])



figures={}



def example7A(iMultipleChoices=False):
    # This example shows messages indicating errors in quesiton and answer.
    # The errors due to the current source code is nothing to do with them and is printed in the "black" console (terminal).
    name='checkups7' # do not change
    heading='Testing' # do not change
    STDs={'12345678': 'oooo'} # do not change

    a=gNs.work(name, heading, STDs, QGs, True, iMultipleChoices, False)
    gNs.mkHTMLs(a, figures)
    #a.saveWork()


if __name__ == '__main__':
    example7A(False)
