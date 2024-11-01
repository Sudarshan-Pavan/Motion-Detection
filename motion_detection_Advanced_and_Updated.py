import threading
import winsound
import cv2
import imutils

print("Threshold value: the minimum amount of pixel change needed to detect motion between frames.")
threshold_input = int(input("Enter the threshold limit for motion detection: "))
print("Alarm count threshold indicates sustained motion detection, triggering the alarm after multiple frames detect significant changes. ")
alarm_count_threshold = int(input("Enter the alarm count threshold: "))

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm_counter = 0
thread_running = False  # Flag to track if an alarm thread is active
detection_active = False  # Flag to toggle motion detection on/off

def beep_alarm():
    global alarm_counter, thread_running
    for _ in range(5):
        print("ALARM")
    winsound.Beep(3000, 600)
    alarm_counter = 0
    thread_running = False  # Reset flag after alarm finishes

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=500)
    
    # Check if detection is active
    if detection_active:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > threshold_input:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)

        # Trigger alarm if counter threshold is reached and no thread is active
        if alarm_counter > alarm_count_threshold and not thread_running:
            thread_running = True  # Set flag before starting thread
            threading.Thread(target=beep_alarm).start()
    else:
        cv2.imshow("Cam", frame)  # Show regular frame if detection is inactive

    key_pressed = cv2.waitKey(30)
    
    # Toggle detection with "a" key
    if key_pressed == ord("d"):
        detection_active = not detection_active
        alarm_counter = 0  # Reset alarm counter when toggling detection
        print("Motion detection active: ", detection_active)

    # Exit with "m" key
    if key_pressed == ord("m"):
        break

cap.release()
cv2.destroyAllWindows()