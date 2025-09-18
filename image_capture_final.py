#------------------------------------------------------------------------------------------------------------------
#   Image capture program
#------------------------------------------------------------------------------------------------------------------

import cv2
import pickle
from datetime import datetime

# Initialize camera (compatible con macOS)
# Ajusta `cam_port` si tu cámara está en otro índice (0, 1, ...)
cam_port = 1
cam = cv2.VideoCapture(cam_port)
if not cam.isOpened():
    # Intenta con el puerto 0 si el puerto por defecto no funciona
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise RuntimeError("No se pudo abrir la cámara. Ajusta `cam_port` al índice correcto.")
font = cv2.FONT_HERSHEY_SIMPLEX

# Read images
n_images = 50
images = []
i = 0
while (i<n_images):

    result, frame = cam.read()    

    # Show result
    if result:
        # Convertir a escala de grises y suavizar antes de detectar bordes
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
        edges = cv2.Canny(blurred, 50, 150)

        # Convertir a BGR para poder dibujar texto y mostrar en color (bordes en blanco sobre fondo negro)
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        text = "Image " + str(i) + "/" + str(n_images)
        cv2.putText(edges_bgr, text, (10,450), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("<<Press + to capture image - edges shown>>", edges_bgr)

        # Leer la tecla una sola vez por iteración
        key = cv2.waitKey(1) & 0xFF
        if key == ord('+'):
            # Guardar el frame original a color (cambia a `edges` si prefieres guardar los bordes)
            images.append(frame)
            i += 1
            print("Image " + str(i) + "/" + str(n_images))
        elif key == ord('q'):
            break

    else:
        print("No image detected")
        break

cam.release()
cv2.destroyAllWindows()

# Save data
now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
outputFile = open(now + '.obj', 'wb')
pickle.dump(images, outputFile)
outputFile.close()

#------------------------------------------------------------------------------------------------------------------
#   End of file
#------------------------------------------------------------------------------------------------------------------
