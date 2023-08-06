import random, re, os, math, pickle
from .generateMakeHTMLs import mkHTMLs
from .generateMultiChoices import generateChoices


##def getQA(QG, indxJ: int =-1, seed: int =None):
##    # generateEm.work.makeSheets()
##    # generateShowExample.showExample()
##    if seed:
##        random.seed(seed)
##
##    Q, strA, _, qType = QG
##
##    if indxJ<0:
##        indxJ=random.choice(range(len(Q)))
##
##    try:
##        exec(strA)
##    except Exception as err:
##        return f'Error::exec(A)...{err}', None, None, None
##
##    try:
##        dataA=eval('data')
##    except Exception as err:
##        return f'Error::eval(data)....{err}', None, None, None
##    
##    try:
##        answers=eval('answer')
##    except Exception as err:
##        return f'Error::eval(answer)....{err}', None, None, None
##
##    if not answers:
##        return f'Error::empty answer. Add answer.', None, None, None
##
##    if len(answers)<len(Q):
##        return f'Error::insufficent answers. Add answer.', None, None, None
##
##    strQ=Q[indxJ]
##
##    if '<!--' in strQ:
##        indx=strQ.index('<!--')
##        print(indx)
##        strQ = strQ[:indx]
##
##    if '{%' in strQ and '%}' in strQ:
##        for string in re.findall(r"\{%(.*?)\%}", strQ):
##            try:
##                strQ=strQ.replace('{%'+string+'%}', str(eval(string)))
##            except Exception as err:
##                return f'Error::질문 #{indxJ+1}에 들어있는 변수-{string}....{err}', None, None, None
##
##    if dataA:
##        if strQ.rstrip().endswith('</pre>'):
##            strQ += '<b>DATA:</b><br>'+'<br>'.join(f'{v}' for v in dataA)
##        else:
##            strQ += '<br><b>DATA:</b><br>'+'<br>'.join(f'{v}' for v in dataA)
##    else:
##        if '아래 DATA' in strQ:
##            return f'Error::Q{indx+1} 본문에서는 DATA를 언급하는데 제공된 값이 없네요.', None, None, None
##
##    return strQ, answers[indxJ], indxJ, qType



class work():
    def __init__(self, name='', heading='', STDs={}, QGs=[], 
                 flagChoice=None, flagShuffling=False):
        self.Name=name
        self.Heading=heading
        self.STDs=STDs
        self.QGs=QGs
        self.Flag4Choice = flagChoice
        self.Flag4Shuffling = flagShuffling
        self.Flag4Answer = True
        self.Sheets={}

    def initializeWork(self):
        if not self.QGs or not self.STDs: return
        self.Sheets.clear()
        indices=list(range(len(self.QGs)))
        for std in self.STDs.keys():
            self.Sheets[std]={'orders':indices.copy(),
                              'seed':random.sample(range(10001,100000), len(self.QGs))}

        if self.Flag4Shuffling:
            for v in self.Sheets.values():
                random.shuffle(v['orders'])

    def makeSheets(self):
        if not self.QGs or not self.STDs: return
        
        for std, v in self.Sheets.items():
            tmp=[]
            for seed, j in zip(v['seed'], v['orders']):
                out=self.getQA(self.QGs[j], -1, seed)
                if out[0] is None:
                    print(std, out, self.QGs[cat][name].Name, '????---Try again!')
                    self.Sheets.clear()
                    return

                if self.Flag4Choice or (isinstance(out[1], dict) and 'choices' in out[1]):
                    xtra, ansChoice, _ = generateChoices(out[1])
                    out = (out[0]+xtra, int(ansChoice), out[-1])

                tmp.append(out)

            v['Q&A'] = tmp


    def makeSheetsWChoices(self): # 이미 계산완료된 상태로 v['Q&A']가 있다는 전제.
        for std, v in self.Sheets.items():
            for j, qNa in enumerate(v['Q&A']):
##                if qNa[-1] == 'choice':
##                    continue
##                else:
##                    xtra, ansChoice, _ = generateChoices(qNa[1])
##                    v['Q&A'][j]=(qNa[0]+xtra, int(ansChoice), qNa[-1])

                xtra, ansChoice, _ = generateChoices(qNa[1])
                v['Q&A'][j]=(qNa[0]+xtra, int(ansChoice), qNa[-1])


    def getAnswers(self):
        return {std:[item[1] for item in v['Q&A']] for std,v in self.Sheets.items()}


    def saveWork(self):
        if not os.path.exists(os.path.join('.', f'{self.Name}')):
            os.mkdir(os.path.join('.', f'{self.Name}'))

        # save work to a pickle file - to be used to score student's answer files
        pickle.dump(self, open(os.path.join('.',f'{self.Name}',f'{self.Name}Work.pickle'),'wb'),
                               protocol=pickle.HIGHEST_PROTOCOL)

        # save all answers to a text file - to provide to students after scoring is done
        with open(os.path.join('.',f'{self.Name}',f'{self.Name}Answers.txt'), mode='w', encoding='utf-8') as f:
            f.write(f'{self.Heading} Answers {self.Name}\n')
            for SID, ans in self.getAnswers().items():
                f.write('SID: '+SID+'\n')
                for j, item in enumerate(ans):
                    f.write(f'\t{j+1}: {item}\n')


    @staticmethod
    def getQA(QG, indxJ: int =-1, seed: int =None):
        if seed:
            random.seed(seed)

        Q, strA, _, qType = QG

        if indxJ<0:
            indxJ=random.choice(range(len(Q)))

        try:
            exec(strA)
        except Exception as err:
            return f'Error::exec(A)...{err}', None, None, None

        try:
            dataA=eval('data')
        except Exception as err:
            return f'Error::eval(data)....{err}', None, None, None
        
        try:
            answers=eval('answer')
        except Exception as err:
            return f'Error::eval(answer)....{err}', None, None, None

        if not answers:
            return f'Error::empty answer. Add answer.', None, None, None

        if len(answers)<len(Q):
            return f'Error::insufficent answers. Add answer.', None, None, None

        strQ=Q[indxJ]

        if '<!--' in strQ:
            indx=strQ.index('<!--')
            print(indx)
            strQ = strQ[:indx]

        if '{%' in strQ and '%}' in strQ:
            for string in re.findall(r"\{%(.*?)\%}", strQ):
                try:
                    strQ=strQ.replace('{%'+string+'%}', str(eval(string)))
                except Exception as err:
                    return f'Error::질문 #{indxJ+1}에 들어있는 변수-{string}....{err}', None, None, None

        if dataA:
            if strQ.rstrip().endswith('</pre>'):
                strQ += '<b>DATA:</b><br>'+'<br>'.join(f'{v}' for v in dataA)
            else:
                strQ += '<br><b>DATA:</b><br>'+'<br>'.join(f'{v}' for v in dataA)

        return strQ, answers[indxJ], indxJ, qType

