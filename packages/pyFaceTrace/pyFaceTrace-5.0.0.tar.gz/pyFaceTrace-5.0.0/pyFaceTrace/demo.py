import pyFaceTrace as ft
import cv2
ft.loadDB()
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while(True):    
    ret, img = cap.read()
    if not ret:continue
    #img=cv2.flip(img,1)
    tags,dists,rects,img = ft.predictImage(img)            
    cv2.imshow('press esc to exit...', img)
    if cv2.waitKey(10) == 27: break
    
cap.release()
cv2.destroyAllWindows()