# import cv2 

# while True :

#    path = input("Enter path of the img OR q for quit\n ")
#    if path == "q" :
#     break
#    print(path)

#    img = cv2.imread(path)
#    input1 = int(input("WHAT YOU WANT TO DO WITH THIS IMG PRESS 1 FOR GRAYSCALE,  2 FOR SAVE,  3 FOR SHOW IMG\n"))
#    if input1 == 1 :
#        grayimg =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#        input2 =  int(input("img convrt to gray scale successfull\n what to do now press 1 for show img or 2 for save"))
#        if input2 == 1 :
#                 cv2.imshow("grayscale img",grayimg)
#                 cv2.waitKey(0)
#                 cv2.destroyAllWindows()
#        elif input2 == 2 :
#                 path2 = input("enter the name of the img YOU want to save")
#                 cv2.imwrite(path2, grayimg) 
#                 print(f"img {path2} save successfully")
#    break


import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Drawing utility
mp_draw = mp.solutions.drawing_utils

# Open Webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    # Flip image
    frame = cv2.flip(frame, 1)

    # Convert BGR -> RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    results = hands.process(rgb)

    # Draw landmarks
    # Draw landmarks
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:

        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        h, w, c = frame.shape

        for id, lm in enumerate(hand_landmarks.landmark):

            if id == 8:

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                cv2.circle(frame, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

                cv2.putText(
                    frame,
                    f"X:{cx}  Y:{cy}",
                    (cx + 15, cy - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )
        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows() 


import cv2
import mediapipe as mp

# ==========================
# MediaPipe Initialization
# ==========================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ==========================
# Open Webcam
# ==========================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Failed to open camera.")
    exit()

print("✅ Camera Started")

# ==========================
# Main Loop
# ==========================
while True:

    success, frame = cap.read()

    if not success:
        print("❌ Failed to read frame.")
        break

    # Mirror image
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand Detection
    results = hands.process(rgb)

    count = 0

    # Draw Hand Landmarks
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            h, w, c = frame.shape
            fingers = []
            # ==========================
                 # Thumb Detection
                     # ==========================
            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                fingers.append(1)
            else:
                 fingers.append(0)

            # Read Every Landmark
            for id, lm in enumerate(hand_landmarks.landmark):
                
                # Index Finger Tip
                if id == 8:

                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    # Green Circle
                    cv2.circle(
                        frame,
                        (cx, cy),
                        12,
                        (0, 255, 0),
                        cv2.FILLED
                    )

                    # Coordinates
                    cv2.putText(
                        frame,
                        f"X:{cx}  Y:{cy}",
                        (cx + 15, cy - 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )
  
           
                 # Other Fingers

            for tip in [8, 12, 16, 20]:

                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                     fingers.append(1)
                else:
                    fingers.append(0)  

            count = fingers.count(1) 
            
    cv2.putText(
    frame,
    f"Finger Count : {count}",
    (20, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 0, 0),
    2
)
    
    # Show Window
    cv2.imshow("Hand Tracking", frame)

    # Exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ==========================
# Release Resources
# ==========================
cap.release()
cv2.destroyAllWindows()