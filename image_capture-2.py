#------------------------------------------------------------------------------------------------------------------
#   Image capture program
#------------------------------------------------------------------------------------------------------------------

import cv2
import pickle
from datetime import datetime

# Initialize camera
cam_port = 1
cam = cv2.VideoCapture()
# On Windows you might use cv2.CAP_DSHOW; on macOS/OpenCV defaults are fine.
try:
    cam.open(cam_port, cv2.CAP_DSHOW)
except Exception:
    cam.open(cam_port)
font = cv2.FONT_HERSHEY_SIMPLEX

# Read images
n_images = 50
images = []
i = 0
while (i<n_images):

    result, frame = cam.read()    

    # Show result
    if result:
        # Convert to grayscale and compute edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Optional: blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5,5), 1.4)
        # Canny edge detector - thresholds can be tuned
        edges = cv2.Canny(blurred, 50, 150)

        # Convert edges to BGR so we can draw text in color if desired
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        text = "Image " + str(i) + "/" + str(n_images)
        cv2.putText(edges_bgr, text, (10,450), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("<<Press + to capture image - edges shown>>", edges_bgr)

        # WaitKey once per loop and store the key
        key = cv2.waitKey(1) & 0xFF
        if key == ord('+'):
            # Save the original color frame (or edges if you prefer)
            images.append(frame)
            i+=1
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
