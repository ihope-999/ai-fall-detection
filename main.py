import cv2
import mediapipe as mp
import datetime
import functions
import settings

fall_count = 0
capture = cv2.VideoCapture(0)
program_running = True
fps_time = 0
fall_detected = False
recent_changes = []

model_path = functions.check_model_availabity()

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    min_pose_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

landmarker = PoseLandmarker.create_from_options(options)
previous_spine_height = None

print("Fall detection \n press q to quit.")

while program_running:
    isWorking, frame = capture.read()
    if not isWorking:
        break

    fps_time += 30
    imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imageRGB)
    result = landmarker.detect_for_video(mp_image, fps_time)

    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]

        left_hip = landmarks[settings.LEFT_HIP]
        right_hip = landmarks[settings.RIGHT_HIP]
        left_shoulder = landmarks[settings.LEFT_SHOULDER]
        right_shoulder = landmarks[settings.RIGHT_SHOULDER]

        mid_shoulder = (left_shoulder.y + right_shoulder.y) / 2
        mid_hip = (right_hip.y + left_hip.y) / 2
        recline = abs(mid_hip - mid_shoulder)
        current_spine_height = (mid_hip + mid_shoulder) / 2

        body_width = abs(left_shoulder.x - right_shoulder.x)
        aspect_ratio = body_width / (recline + 0.001)
        person_is_horizontal = aspect_ratio > 1.5
        hip_is_low = mid_hip > 0.75

        if previous_spine_height:
            now = datetime.datetime.now()
            change = current_spine_height - previous_spine_height

            recent_changes.append(abs(change))
            if len(recent_changes) > 5:
                recent_changes.pop(0)
            avg_change = sum(recent_changes) / len(recent_changes)

            print(f"Avg change: {avg_change:.4f} | Recline: {recline:.4f} | Aspect: {aspect_ratio:.4f} | Hip: {mid_hip:.4f}")

            if True:
                fall_count += 1
                fall_detected = True
                print(f"FALL: {fall_count}")
                print(f"Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                img_path = functions.take_fall_picture(frame, now)
                functions.create_fall_log(now, fall_count)
                functions.send_WP_message(fall_count, img_path)

            elif avg_change < settings.CONDITIONED_CHECK and not person_is_horizontal:
                fall_detected = False

        previous_spine_height = current_spine_height

    cv2.imshow("fallDetection", imageRGB)

    key = cv2.waitKey(10)
    if key == ord("q"):
        print("Closing the window")
        program_running = False

capture.release()
cv2.destroyAllWindows()
landmarker.close()