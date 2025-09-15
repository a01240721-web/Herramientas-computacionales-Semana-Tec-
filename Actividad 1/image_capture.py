#------------------------------------------------------------------------------------------------------------------
#   Image capture program
#------------------------------------------------------------------------------------------------------------------

import cv2
import pickle
from datetime import datetime

# Initialize camera
cam_port = 0
cam = cv2.VideoCapture()
cam.open(cam_port, cv2.CAP_DSHOW)
font = cv2.FONT_HERSHEY_SIMPLEX

# Read images
n_images = 50
images = []
i = 0
while (i<n_images):

    result, frame = cam.read()    

    # Show result
    if result:  
                
        frame_with_text = frame.copy()
        text = "Image " + str(i) + "/" + str(n_images)
        cv2.putText(frame_with_text, text, (10,450), font, 2, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("<<Press + to capture image>>", frame_with_text)
    
        if cv2.waitKey(1) & 0xFF == ord('+'):
            images.append(frame)
            i+=1
            print("Image " + str(i) + "/" + str(n_images))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        print("No image detected")

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
