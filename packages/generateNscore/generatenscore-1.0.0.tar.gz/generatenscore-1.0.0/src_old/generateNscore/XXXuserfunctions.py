import random

    
def func1(prm=None): # right/wrong 
    # 반환값: 보기문항들 (최소 4 개 이상), 정답문항번호, 정답
    nChoices=random.choice([3,4,5])
    choices=random.sample([f'{prm}{v}' for v in range(10)], nChoices)
    return choices, nChoices, random.choice(choices)


def func2():
    return None

def RightWrong(entries4Right=[], entries4Wrong=[], f='옳은', nChoices=3):
    if len(entries4Wrong)<nChoices:
        return f'Error  vWrong items<{nChoices}', None
    if len(entries4Right)<nChoices:
        return f'Error  vRight items<{nChoices}', None

    if f in ('옳은', 'correct'):
        correctAns=random.choice(entries4Right)
        entries=entries4Wrong.copy()
        indx=entries4Right.index(correctAns)
        if len(entries)>indx: entries.pop(indx) # 같은 순서의 짝은 서로 exclusive
    else:
        correctAns=random.choice(entries4Wrong)
        entries=entries4Right.copy()
        indx=entries4Wrong.index(correctAns)
        if len(entries)>indx: entries.pop()

    entries.append(correctAns)

    return MakeChoices(entries, nChoices, correctAns)



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




