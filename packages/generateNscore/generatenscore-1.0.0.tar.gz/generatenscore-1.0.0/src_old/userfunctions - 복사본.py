import random

# 반환값: 보기문항들 (최소 4 개 이상), 정답문항번호, 정답

nChoices=4

def func1(choices=None, ans=None):
    from fractions import Fraction
    choicesBefore = []
    for j in range(10):
        fr1=Fraction(random.choice([1,2]), random.choice([4,5,6,7,8]))
        fr2=Fraction(random.choice([1,2]), random.choice([4,5,6,7,8]))
        choicesBefore.append((fr1, fr2, (fr1+fr2)))

    choices=[]
    for _, _, fr in choicesBefore:
        choices.append(r'EQ% \frac {'+f'{fr.numerator}'+'} {'+f'{fr.denominator}'+'} %EQ')

    indx=random.choice(range(len(choices)))
    f1, f2, _=choicesBefore[indx]
    return choices, indx, fr'EQ% \frac {f1.numerator} {f1.denominator} + \frac {f2.numerator} {f2.denominator}%EQ'

def func1B(choices=None, ans=None):
    from fractions import Fraction
    choicesBefore = []
    for j in range(10):
        fr1=Fraction(random.choice([1,2]), random.choice([3, 4, 5, 8]))
        fr2=Fraction(random.choice([1,2]), random.choice([3, 4, 5, 8]))
        choicesBefore.append((fr1, fr2, (fr1+fr2)))

    choices=[]
    for _, _, fr in choicesBefore:
        choices.append(r'EQ% \frac {'+f'{fr.numerator}'+'} {'+f'{fr.denominator}'+'} %EQ')

    indx=random.choice(range(len(choices)))
    f1, f2, _=choicesBefore[indx]
    return choices, indx, [f1.numerator, f1.denominator, f2.numerator, f2.denominator]


def func2(prm):
    rights=[]
    for _ in range(10):
        vA=random.choice(range(50,99))
        vB=random.choice(range(10,50))
        rights.append(f'{vA}+{vB}={vA+vB}')

    wrongs=[]
    for s in rights:
        eq, ans= s.split('=')
        a, b = eq.split('+')
        wrongs.append(f"{eq}={eval(ans)+1}" if random.choice([0,1]) else f"{eq}={eval(ans)-1}")
        
    entries, indx, ans = RightWrong(rights, wrongs, prm)
    return entries, indx, ans


def RightWrong(entries4Right=[], entries4Wrong=[], f='옳은'):
    if f in ('옳은', 'correct'):
        correctAns=random.choice(entries4Right)
        entries=entries4Wrong.copy()
        indx=entries4Right.index(correctAns)
        if len(entries)>indx: entries.pop(indx)
    else:
        correctAns=random.choice(entries4Wrong)
        entries=entries4Right.copy()
        indx=entries4Wrong.index(correctAns)
        if len(entries)>indx: entries.pop()

    entries.append(correctAns)

    return entries, entries.index(correctAns), correctAns


def Paired(entries4T=[], entries4F=[], f='옳은'): #제공된 짝(pair)이 옳은 지 틀린 지...
    delimetr=' <==> '
    nChoices=min(len(entries4F), len(entries4T), 4)
    if nChoices<3: return 'Error', None
    ans=random.choice(range(nChoices)) # 정답번호
    possibleChoices=range(min(len(entries4F), len(entries4T)))
    chosenI=random.sample(possibleChoices, nChoices)

    if f in ('옳은', 'correct'):
        ref=chosenI.copy()
        x=ref.pop(ans)
        if random.choice([0,1]):
            tmp=[f for f in range(len(entries4F)) if f != x]
            chosenNew=random.sample(tmp, nChoices-1)
            while any([f==g for f,g in zip(chosenNew, ref)]):
                chosenNew=random.sample(tmp, nChoices-1)
            ref.insert(ans,x)
            chosenNew.insert(ans,x)
            choices=[f'{entries4F[f]}{delimetr}{entries4T[t]}' for f,t in zip(chosenNew, ref)]
        else:
            tmp=[f for f in range(len(entries4T)) if f != x]
            chosenNew=random.sample(tmp, nChoices-1)
            while any([f==g for f,g in zip(chosenNew, ref)]):
                chosenNew=random.sample(tmp, nChoices-1)
            ref.insert(ans,x)
            chosenNew.insert(ans,x)
            choices=[f'{entries4F[f]}{delimetr}{entries4T[t]}' for f,t in zip(ref, chosenNew)]
    else:
        choices=[f'{entries4F[i]}{delimetr}{entries4T[i]}' for i in chosenI]
        if random.choice([0,1]):
            iTmp=random.choice([f for f in range(len(entries4F)) if f not in chosenI])
            choices[ans]=f'{entries4F[iTmp]}{delimetr}{entries4T[chosenI[ans]]}'
        else:
            iTmp=random.choice([f for f in range(len(entries4T)) if f not in chosenI])
            choices[ans]=f'{entries4F[chosenI[ans]]}{delimetr}{entries4T[iTmp]}'

    entries=[]
    for i, choice in enumerate(choices):
        if random.choice([0,1]):
            x=choice.split(delimetr)
            x.reverse()
            entries.append(delimetr.join(x))
        else:
            entries.append(choice)
    return MakeChoices(entries, 4, entries[ans])


if __name__ == '__main__':
    for item in func1()[0]:
        print(item)
