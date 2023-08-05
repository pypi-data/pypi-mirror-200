import webbrowser
from .generateMakeHTMLs import mkHTMLs
from .generateMultiChoices import generateChoices


def showExample(a, qg, iChoices, figures=None):
    a.STDs={'0000': 'oooo'}
    a.Flag4Shuffling=False
    a.Flag4Answer=True
    a.Flag4MultiChoices=iChoices
    Q, A, _, qType = qg
    tmp=[]

    if iChoices:
        for j in range(len(Q)):
            qtxt, answer, *_ = a.getQA(qg, j, None)
            if qType == 'choice':
                tmp.append((qtxt, answer, j))
                continue

            if isinstance(qtxt, str) and qtxt.startswith('Error'):
                print(None, qtxt, answer, a.Name, '????---Try again!')
                a.Sheets.clear()
                return 'Error@line 26 of ShowExample. Read the command window.'

            if not isinstance(answer, (int, float)):
                print(None, qtxt, answer, qg.Name, '정수 또는 실수 답이 아님.!')
                a.Sheets.clear()
                return 'Error@line 32 of ShowExample. Read the command window.'
            else:
                xtra, ansChoice, _ = generateChoices(answer)
                tmp.append((qtxt+xtra, int(ansChoice), j))

    else:
        for j in range(len(Q)):
            qtxt, answer, *_ = a.getQA(qg, j, None)
            if isinstance(qtxt, str) and qtxt.startswith('Error'):
                print(None, qtxt, answer, a.Name, '????---Try again!  @line39 of ShowExample')
                a.Sheets.clear()
                return 'Error@line 43 of ShowExample. Read the command window.'
            tmp.append((qtxt, answer, j))

    a.Sheets['0000']={'Q&A':tmp}
    mkHTMLs(a, True, figures)
    webbrowser.open('sample.html')
