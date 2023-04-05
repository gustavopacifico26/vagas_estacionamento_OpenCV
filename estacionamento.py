import numpy as np
import cv2

#mapeamento das vagas
vaga1 = [1, 89, 108, 213]
vaga2 = [115, 87, 152, 211]
vaga3 = [289, 89, 138, 212]
vaga4 = [439, 87, 135, 212]
vaga5 = [591, 90, 132, 206]
vaga6 = [738, 93, 139, 204]
vaga7 = [881, 93, 138, 201]
vaga8 = [1027, 94, 147, 202]

vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6, vaga7, vaga8]

#upload do video
video = cv2.VideoCapture("video.mp4")

#loop para rodar o video
while True:

    check,img = video.read()

    #converter a imagem original para cinza
    imgCinza = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #aplicar um threshold adaptativo(vai desconsiderar ruídos das imagens como sombras) para binarizar a imagem
    #o threshold cria uma imagem binária a partir de uma imagem cinza
    imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    #é possível observar que uma vaga vazia tem uma grande quantidade de pixels preto

    #melhorando a imagem(retirando ruídos)
    imgBlur = cv2.medianBlur(imgTh, 5)
    kernel = np.ones((3, 3), np.int8)
    imgDil = cv2.dilate(imgBlur, kernel)

    vagas_livres = 0

    for x,y,w,h in vagas:
        #calcular a quantidade de pixels brancos dentro das vagas
        recorte = imgDil[y:y+h, x:x+w]
        qtd_brancos = cv2.countNonZero(recorte)
        cv2.putText(img, str(qtd_brancos), (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        if qtd_brancos > 3000:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
        else:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
            vagas_livres += 1

    cv2.rectangle(img, (90,0), (415,60), (255, 0, 0), -1)
    cv2.putText(img, f'Vagas Livres: {vagas_livres}/{len(vagas)}', (95,45), (cv2.FONT_HERSHEY_SIMPLEX), 1.5, (0, 0, 0), 5)

    cv2.imshow("video", img)
    #cv2.imshow("video TH", imgTh)
    #cv2.imshow("video Dilatado", imgDil)
    cv2.waitKey(10)