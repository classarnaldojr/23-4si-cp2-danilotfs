import cv2
import numpy as np



def carregaMatches(des1, des2):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x:x.distance)
    return matches

def resultado(e1, e2, pe, pd):
    # definição do vitorioso dependendo da escolha do jogador
    if escolha1 == "tesoura" and escolha2 == "papel" or escolha1 == "pedra" and escolha2 == "tesoura" or escolha1 == "papel" and escolha2 == "pedra":
        cv2.putText(output, "esquerda ganhou", (340, 150), font, 1, (255, 255, 0), 2, cv2.LINE_4)
        pe += 0.01
    elif escolha1 == "tesoura" and escolha2 == "pedra" or escolha1 == "pedra" and escolha2 == "papel" or escolha1 == "papel" and escolha2 == "tesoura":
        cv2.putText(output, "direita ganhou", (340, 150), font, 1, (100, 0, 100), 2, cv2.LINE_4)
        pd += 0.01
    elif escolha1 == escolha2:
        cv2.putText(output, "empate", (400, 150), font, 1, (0, 125, 255), 2, cv2.LINE_4)

    return pe, pd


# carrega as imagens
tesoura = cv2.imread('tesoura.png',0)
pedra = cv2.imread('pedra.png', 0)
papel = cv2.imread('papel.png', 0)

# leitura do vídeo
vc = cv2.VideoCapture("pedra-papel-tesoura.mp4")

# definição de fonte
font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX

# declaração da pontuação
pontoEsq = 0
pontoDir = 0


if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

while rval:
    rval, frame = vc.read()

    if not rval:
        break

    # output vai ser o vídeo usado no final para registrar a pontuação, o trabalho será feito no img
    output = frame.copy()
    output = cv2.resize(output, (1024, 576))
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # relocação de tamanho na imagem para que nós trabalhemos com uma imagem menor dentro de cada frame
    img = cv2.resize(img, (1024, 576))
    orb = cv2.ORB_create()

    # Pega para trabalhar apenas na parte esquerda do canvas
    roiesq = img[:, :520]

    # definição do kp e des de cada formato (frame inteiro, pedra, papel e tesoura)
    kptesoura, destesoura = orb.detectAndCompute(tesoura,None)
    kppedra, despedra = orb.detectAndCompute(pedra,None)
    kppapel, despapel = orb.detectAndCompute(papel,None)
    kpframe, desframe = orb.detectAndCompute(roiesq, None)

    # divisão dos pontos de características de cada um dos formatos, assim como dos frames
    graytesoura = cv2.drawKeypoints(tesoura, kptesoura, outImage=np.array([]), flags=0)
    graypedra = cv2.drawKeypoints(pedra, kppedra, outImage=np.array([]), flags=0)
    graypapel = cv2.drawKeypoints(papel, kppapel, outImage=np.array([]), flags=0)
    grayframe = cv2.drawKeypoints(roiesq, kpframe, outImage=np.array([]), flags=0)

    # comparação e organização das características entre o formato da mão (pedra, papel ou tesoura) e o frame no lado esquerdo
    matchesTesoura = carregaMatches(desframe, destesoura)
    #print("Foram encontrados: {} matches para tesoura".format(len(matchesTesoura)))
    imgMatchesTesoura = cv2.drawMatches(roiesq, kpframe, tesoura, kptesoura, matchesTesoura[:20], None, flags=2)

    matchesPedra = carregaMatches(desframe, despedra)
    #print("Foram encontrados: {} matches para pedra".format(len(matchesPedra)))
    imgMatchesPedra = cv2.drawMatches(roiesq, kpframe, pedra, kppedra, matchesPedra[:20], None, flags=2)

    matchesPapel = carregaMatches(desframe, despapel)
    #print("Foram encontrados: {} matches para papel\n".format(len(matchesPapel)))
    imgMatchesPapel = cv2.drawMatches(roiesq, kpframe, papel, kppapel, matchesPapel[:20], None, flags=2)

    # o programa faz a comparação de caracterísitcas notadas entre o frame e o formato da mão, do qual o formato que tiver mais caracterísiticas será o formato certo (pedra, papel, tesoura)
    if (len(matchesTesoura) > len(matchesPedra)) & (len(matchesTesoura) > len(matchesPapel)):
        #print("o da esquerda é uma tesoura eu acho")
        escolha1 = "tesoura"
        cv2.putText(output, "tesoura", (150, 150), font, 1, (255, 0, 255), 2, cv2.LINE_4)
    elif (len(matchesPedra) > len(matchesTesoura)) & (len(matchesPedra) > len(matchesPapel)):
        #print("o da esquerda é uma pedra eu acho")
        escolha1 = "pedra"
        cv2.putText(output, "pedra", (150, 150), font, 1, (255, 0, 255), 2, cv2.LINE_4)
    elif (len(matchesPapel) > len(matchesTesoura)) & (len(matchesPapel) > len(matchesPedra)):
        #print("o da esquerda é um papel eu acho")
        escolha1 = "papel"
        cv2.putText(output, "papel", (150, 150), font, 1, (255, 0, 255), 2, cv2.LINE_4)

    # registro de pontos dentro do canvas
    cv2.putText(output, "PONTOS", (400, 50), font, 1, (0, 0, 255), 2, cv2.LINE_4)


    # Pega para trabalhar apenas na parte direita do canvas
    roidir = img[:, 490:]

    kpframe, desframe = orb.detectAndCompute(roidir, None)
    grayframe = cv2.drawKeypoints(roidir, kpframe, outImage=np.array([]), flags=0)

    matchesTesoura = carregaMatches(desframe, destesoura)
    #print("Foram encontrados: {} matches para tesoura".format(len(matchesTesoura)))
    imgMatchesTesoura = cv2.drawMatches(roidir, kpframe, tesoura, kptesoura, matchesTesoura[:20], None, flags=2)

    matchesPedra = carregaMatches(desframe, despedra)
    #print("Foram encontrados: {} matches para pedra".format(len(matchesPedra)))
    imgMatchesPedra = cv2.drawMatches(roidir, kpframe, pedra, kppedra, matchesPedra[:20], None, flags=2)

    matchesPapel = carregaMatches(desframe, despapel)
    #print("Foram encontrados: {} matches para papel\n".format(len(matchesPapel)))
    imgMatchesPapel = cv2.drawMatches(roidir, kpframe, papel, kppapel, matchesPapel[:20], None, flags=2)

    if (len(matchesTesoura) > len(matchesPedra)) & (len(matchesTesoura) > len(matchesPapel)):
        #print("o da direita é uma tesoura eu acho")
        escolha2 = "tesoura"
        cv2.putText(output, "tesoura", (700, 150), font, 1, (255, 0, 255), 2, cv2.LINE_4)
    elif (len(matchesPedra) > len(matchesTesoura)) & (len(matchesPedra) > len(matchesPapel)):
        #print("o da direita é uma pedra eu acho")
        escolha2 = "pedra"
        cv2.putText(output, "pedra", (700, 150), font, 1, (255, 0, 255), 2, cv2.LINE_4)
    elif (len(matchesPapel) > len(matchesTesoura)) & (len(matchesPapel) > len(matchesPedra)):
        #("o da direita é um papel eu acho")
        cv2.putText(output, "papel", (700, 150), font, 1, (255, 0, 255), 2, cv2.LINE_4)
        escolha2 = "papel"

    # chama a função que aponta o vitorioso e adiciona ao resultado no contador
    pontoEsq, pontoDir = resultado(escolha1, escolha2, pontoEsq, pontoDir)

    # arredonda a pontuação porque eu não sei fazer de outro jeito :)
    cv2.putText(output, f"{round(pontoEsq)} X {round(pontoDir)}", (415, 80), font, 1, (255, 0, 0), 2, cv2.LINE_4)

    # roda várias previews para a visualização dos dados
    #cv2.imshow("preview esq", roiesq)
    #cv2.imshow("preview dir", roidir)
    cv2.imshow("preview", output)

    #cv2.imshow("papel", graypapel)
    #cv2.imshow("tesoura", graytesoura)
    #cv2.imshow("tesoura2", graytesoura2)

    #cv2.imshow("preview papel", imgMatchesPapel)
    #cv2.imshow("preview tesoura", imgMatchesTesoura)
    #cv2.imshow("preview tesoura2", imgMatchesTesoura2)

    key = cv2.waitKey(20)
    if key == 27:
        break
cv2.destroyAllWindows()
vc.release()


