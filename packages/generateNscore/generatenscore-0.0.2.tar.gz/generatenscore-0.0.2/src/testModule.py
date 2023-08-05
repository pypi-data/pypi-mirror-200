import random


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
            return [eval(ans[0]+str(j)) for j in range(10)]
        else:
            return [eval(str(j)+ans[1]) for j in range(1, 10)]
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
