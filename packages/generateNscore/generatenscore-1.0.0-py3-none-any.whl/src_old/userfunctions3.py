import random

# 반환값: 보기문항들 (최소 4 개 이상), 정답문항번호, 정답

nChoices=4

def func3(prm): # 아직 미비...
    rightPairs=[]
    for _ in range(10):
        vA=random.choice(range(50,99))
        vB=random.choice(range(10,50))
        rights.append(f'{vA}+{vB}={vA+vB}')

    wrongPairs=[]
    for s in rights:
        eq, ans= s.split('=')
        a, b = eq.split('+')
        wrongs.append(f"{eq}={eval(ans)+1}" if random.choice([0,1]) else f"{eq}={eval(ans)-1}")

    entries, indx, ans = Paired()
    return entries, indx, ans


def Paired(rightPairs=[], wrongPairs=[], f='옳은'): #제공된 짝(pair)이 옳은 지 틀린 지...
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

##    prob=''
##    for i, choice in enumerate(choices):
##        if random.choice([0,1]):
##            x=choice.split(delimetr)
##            x.reverse()
##            prob += '<br>'+chr(9312+i)+' '+delimetr.join(x)
##        else:
##            prob += '<br>'+chr(9312+i)+' '+choice
##        
##    prob += '<br>'+chr(9312+int(nChoices))+' None of the above'
##    prob += '<br>'+chr(9313+int(nChoices))+' All of the above'
##    return '<br>'+prob, ans+1

    entries=[]
    for i, choice in enumerate(choices):
        if random.choice([0,1]):
            x=choice.split(delimetr)
            x.reverse()
            entries.append(delimetr.join(x))
        else:
            entries.append(choice)
    return MakeChoices(entries, 4, entries[ans])

