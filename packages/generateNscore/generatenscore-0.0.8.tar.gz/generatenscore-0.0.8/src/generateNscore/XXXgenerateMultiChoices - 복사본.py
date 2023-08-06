import random

from .common import round2MSF

# 위 import의 common 앞의 .(dot)은 반드시 필요하다.
# 본 코드를 수정하면, .(dot)을 삭제하고 실행한다.
# 그러나, 오류가 없음을 확인하면 반드시 .(dot)을 되돌린 후 저장한다.

# 보기문항은 반드시 정답란에서 정한다.
# 보기문항은 string object으로 생성되며 이름은 choices으로 한다.
# 즉, 이름이 choices인 변수가 존재하면,  선택형 질문이 된다.


def generateChoices(ans, nChoices: int=5): # generateEm.work.makeSheetsWChoices()에서 사용
    # ans의 값 주위의 보기문항 생성
    if isinstance(ans, dict):
        if 'choices' in ans and isinstance(ans['choices'], (tuple, list)):
            choices, choice4ans = MakeChoices(ans['choices'], nChoices, ans['ans'], ans['xtra'])
        elif 'Right' in ans and 'Wrong' in ans and 'TorF' in ans:
            choices, choice4ans = RightWrong(ans['Right'], ans['Wrong'], ans['TofF'])
    else:
        if ans:
            ans=round2MSF(ans)
            if isinstance(ans, int):
                if random.randint(0, 3):
                    choices=variation0_int(str(ans), nChoices=nChoices)
                else:
                    if not ans%2:
                        choices=variation0_int_2(str(ans), nChoices=nChoices)
                    else:
                        choices=variation0_int(str(ans), nChoices=nChoices)
            else:
                if random.randint(0,1):
                    choices=variation0(str(ans), nChoices=nChoices)
                else:
                    choices=variation2(str(ans), nChoices=nChoices)
        else:
            ans=0
            choices=variation0_int(str(ans), nChoices=nChoices)
        
        choices, choice4ans=MakeChoices(choices, nChoices, ans)
    
    return choices, choice4ans, ans



def MakeChoices(answers, nChoices, correctAns, xtra=None):
    try:
        answers.remove(correctAns) # 정답 제거
    except Exception as err:
        print(answers, correctAns, err)

    try:
        answers=random.sample(answers, nChoices-1)
    except Exception as err:
        nChoices = len(answers)+1
        
    answers.append(correctAns)
    random.shuffle(answers)
    
##    choices = '<br>'
##    for i, choice in enumerate(answers):
##        charInCircle=chr(9312+i)
##        choices += f'<br><input type="radio" style="height:20px; width:20px; vertical-align: middle; border-radius: 50%; bckground: white;" id="{charInCircle}" name="QqNUM" onclick="handleClick(this);" value="{i}"><label for="{charInCircle}"> {choice}</label>'
##
##    charInCircle=chr(9312+i)
##    choices += f'<br><input type="radio" style="height:20px; width:20px; vertical-align: middle; border-radius: 50%; bckground: white;" id="{charInCircle}" name="QqNUM" onclick="handleClick(this);" value="{i+1}"><label for="{charInCircle}"> None of the above</label>'
##    charInCircle=chr(9313+i)
##    choices += f'<br><input type="radio" style="height:20px; width:20px; vertical-align: middle; border-radius: 50%; bckground: white;" id="{charInCircle}" name="QqNUM" onclick="handleClick(this);" value="{i+2}"><label for="{charInCircle}"> All of the above</label>'

##    choices = ChoicesWithRadiobuttons(answers) if method2Use4Choices else ChoicesWithNumbers(answers)
    choices = ChoicesWithRadiobuttons(answers, xtra)
    
    if correctAns in answers:
        Choice4correctAns=answers.index(correctAns)+1
    else:
        Choice4correctAns=nChoices+1
    return choices, Choice4correctAns


def ChoicesWithNumbers(answers):
    choices = '<br>'
    for j, choice in enumerate(answers):
        choices += '<br>'+chr(9312+j)+f' {choice}'

    choices += '<br>'+chr(9312+j)+' None of the above'
    choices += '<br>'+chr(9313+j)+' All of the above'
    return choices


def ChoicesWithRadiobuttons(answers, xtra=None):
    choices = '<br>'
    if xtra:
        for j, choice in enumerate(answers):
            charInCircle=chr(9312+j)
            choices += f'<br><input type="radio" style="height:20px; width:20px; vertical-align: middle; border-radius: 50%; bckground: white;" id="{charInCircle}" name="QqNUM" onclick="handleClick(this);" value="{j}"><label for="{charInCircle}"> {xtra(choice)}</label>'
    else:
        for j, choice in enumerate(answers):
            charInCircle=chr(9312+j)
            choices += f'<br><input type="radio" style="height:20px; width:20px; vertical-align: middle; border-radius: 50%; bckground: white;" id="{charInCircle}" name="QqNUM" onclick="handleClick(this);" value="{j}"><label for="{charInCircle}"> {choice}</label>'

    charInCircle=chr(9312+j)
    choices += f'<br><input type="radio" style="height:20px; width:20px; vertical-align: middle; border-radius: 50%; bckground: white;" id="{charInCircle}" name="QqNUM" onclick="handleClick(this);" value="{j+1}"><label for="{charInCircle}"> None of the above</label>'
    charInCircle=chr(9313+j)
    choices += f'<br><input type="radio" style="height:20px; width:20px; vertical-align: middle; border-radius: 50%; bckground: white;" id="{charInCircle}" name="QqNUM" onclick="handleClick(this);" value="{j+2}"><label for="{charInCircle}"> All of the above</label>'
    return choices


    
    



def variation0_int_2(answer: str, nChoices):
    # 음수여부
    ans=answer
    negative=False
    if answer.startswith('-'):
        negative=True
        ans=answer[1:] # 음수기호가 제거된 답

    for i4NZ, c in enumerate(ans[::-1]):
        if int(c):
            break
    if i4NZ:
        ans=ans[:-i4NZ]

    zeros='0'*i4NZ

    # 약수 2의 갯수
    value = int(ans)
    nYaksoo=0
    while not value%2:
        value //= 2
        nYaksoo += 1

    tmp = [f'{value*2**j}{zeros}' for j in range(10) if len(f'{value*2**j}')<=3]
     
    # 음수 복원
    if negative: tmp=['-'+item for item in tmp if item]

    return [eval(f) for f in tmp]



def variation0_int(answer: str, nChoices):
    # 음수여부
    ans=answer
    negative=False
    if answer.startswith('-'):
        negative=True
        ans=answer[1:] # 음수기호가 제거된 답
    
    if len(ans)==1:
        tmp = [str(j) for j in range(10)]
    elif len(ans) == 2:
        if random.randint(0,1):
            tmp = [ans[0]+str(j) for j in range(10)]
        else:
            tmp = [str(j)+ans[1] for j in range(1, 10)]
    else:
        whichone = random.randint(0, 2)
        if  whichone == 0:
            # 유효숫자들 중 첫 번째숫자를 1부터 9까지 변화시킨 목록 생성
            tmp=[f'{i}'+ans[1:] for i in range(1, 10)] # 2022.07.16 추가...
        elif whichone == 1:
            # 유효숫자들 중 2 번째를 0부터 9까지 변화시킨 목록 생성
            tmp=[ans[:1]+f'{i}'+ans[2:] for i in range(10)]
        else:
            # 유효숫자들 중 3 번째를 0부터 9까지 변화시킨 목록 생성
            tmp=[ans[:2]+f'{i}'+ans[3:] for i in range(10)]
 
    # 음수 복원
    if negative: tmp=['-'+item for item in tmp if item]

    return [eval(f) for f in tmp]


def variation0(answer: str, nChoices):
    '''보기문항 정하는 방법 1:
정답의 가장 중요한 첫번째 유효 숫자를 앞 뒤로 1 씩 변경
예: 정답이 92.4이며 nChoices=6인 경우의 보기문항은
1) 62.4  2) 72.4  3) 82.4  4) 92.4 5) None of the above 6) All of the above 이며
정답은 4이다.'''

    # 음수여부
    ans=answer
    negative=False
    if answer.startswith('-'):
        negative=True
        ans=ans[1:] # 음수기호가 제거된 답

    # 소수점여부
    iDot=None
    if '.' in ans:
        iDot=ans.index('.')
        ans=''.join(ans.split('.')) #소수점이 제거된 답

    # i: 0이 아닌 숫자 index
    for i4NZ, c in enumerate(ans):
        #print(ans, c, type(c))
        if int(c): break

    ansChoice=random.randrange(0, nChoices-2)
    
    if len(ans)==1:
        tmp=[ans[:i4NZ]+f'{i}'+ans[i4NZ+1:] for i in range(10)]
    else:
        if random.randint(0,1):
            # 유효숫자들 중 첫 번째숫자를 0부터 9까지 변화시킨 목록 생성
            tmp=[ans[:i4NZ]+f'{i}'+ans[i4NZ+1:] for i in range(10)] # 2022.07.16 추가...
        else:
            # 유효숫자들 중 2 번째를 0부터 9까지 변화시킨 목록 생성
            tmp=[ans[:i4NZ+1]+f'{i}'+ans[i4NZ+2:] for i in range(10)]

    # 소수점 복원
    if iDot: tmp=[item[:iDot]+'.'+item[iDot:] for item in tmp]
    # 음수 복원
    if negative: tmp=['-'+item for item in tmp if item]

    return [eval(f) for f in tmp]



def variation2(answer: str, nChoices): #, allowNoChoice=False):
    '''보기문항 정하는 방법 3:
정답의 단위를 10 씩 늘이는 방법으로 변경
예: 정답이 92.4이며 nChoices=6인 경우의 보기문항은
1) 9.24    2) 92.4  3) 924  4) 9240   5) None of the above   6) All of the above 이다.
이 경우 정답문항을 미리 정한다. 보기문항 수는 1부터 nChoices-2까지 이므로,
정답에 사용된 숫자들 중 가장 큰 숫자를 nChoices-2으로 나눈 나머지로 한다.
예: 92.4의 가장 큰 숫자는 9이며, 9를 (6-2)=4로 나눈 나머지는 1이므로
정답은 2번으로 정한다.
'''
    # 음수여부
    ans=answer
    negative=False
    if answer.startswith('-'):
        negative=True
        ans=ans[1:] # 음수기호가 제거된 답

    # 소수점여부
    iDot=len(ans)
    if '.' in ans:
        iDot=ans.index('.')
        ans=''.join(ans.split('.')) #소수점이 제거된 답

    ans='0'*3+ans+'0'*3 # 2022.07.16 수정..

    ansChoice=max(int(c) for c in answer if c.isnumeric()) % (nChoices-2)

    a=[(ans[:i]+'.'+ans[i:]).strip('0') for i in range(1, len(ans))]
    a=['0'+item if item.startswith('.') else item for item in a]
    ans=[item[:-1] if item.endswith('.') else item for item in a]
    if negative: ans=['-'+item for item in ans if item] # 음수 복원

    return [eval(f) for f in ans]


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





if __name__ == '__main__':
    for v in [1999]:
        print(generateChoices(v))
