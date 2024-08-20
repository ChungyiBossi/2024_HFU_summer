# from keras.models import load_model  # TensorFlow is required for Keras to work
import tensorflow as tf
import cv2  # Install opencv-python
import numpy as np
import time

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
# model = load_model("keras_model.h5", compile=False)
model = tf.saved_model.load("model.savedmodel")

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    start_time = time.time_ns()

    # Grab the webcamera's image.
    ret, raw_image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(raw_image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model(image)
    # prediction = model.predict(image)
    index = np.argmax(prediction) # 最高分的label的編號
    class_name = class_names[index] # label編號的對應名稱
    confidence_score = prediction[0][index] # label編號對應的分數

    # Print prediction and confidence score
    top_one = class_name[2:].strip() # 預測的種類名稱
    top_one_score = np.round(confidence_score * 100) # 預測的分數

    # Show the image in a window, and put some text
    if top_one_score >= 80:
        text_to_put = f'{top_one}: {top_one_score}%'
    else:
        text_to_put = "Recognizing...."

    cv2.putText(
        img=raw_image,
        text=str(text_to_put), 
        org=(100, 100), 
        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale=1,
        color=(0, 255, 255), 
        thickness=1, 
        lineType=cv2.LINE_AA
    )
    cv2.imshow("Webcam Image", raw_image)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

    period_time_in_ms = (time.time_ns() - start_time)/(10**6)
    print("Check time: ", period_time_in_ms)


camera.release()
cv2.destroyAllWindows()
