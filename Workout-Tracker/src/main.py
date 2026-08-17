import cv2
import mediapipe as mp
from pathlib import Path
import numpy as np



BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "assets" / "pose_landmarker_full.task"
VIDEO_PATH = BASE_DIR / "assets" / "pushup.mp4"

print("Model path:", MODEL_PATH)
print("Model exists:", MODEL_PATH.exists())

print("Video path:", VIDEO_PATH)
print("Video exists:", VIDEO_PATH.exists())


BaseOptions = mp.tasks.BaseOptions

PoseLandmarker = mp.tasks.vision.PoseLandmarker

PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions

VisionRunningMode = mp.tasks.vision.RunningMode


options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=VisionRunningMode.VIDEO
)
landmarker = PoseLandmarker.create_from_options(options)

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


def get_visible_arm(landmarks):
    left_vis = (landmarks[11].visibility + landmarks[13].visibility + landmarks[15].visibility) / 3
    right_vis = (landmarks[12].visibility + landmarks[14].visibility + landmarks[16].visibility) / 3

    if left_vis >= right_vis:
        return 11, 13, 15  # left shoulder, elbow, wrist
    return 12, 14, 16      # right shoulder, elbow, wrist


POSE_CONNECTIONS = mp.tasks.vision.PoseLandmarksConnections.POSE_LANDMARKS

def draw_landmarks(frame, landmarks):

    h, w, _ = frame.shape
    points = [
        (int(lm.x * w), int(lm.y * h))
        for lm in landmarks
    ]

    # Left:
    # 11 = left shoulder
    # 13 = left elbow
    # 15 = left wrist
    # 17 = left pinky
    # 19 = left index
    # 21 = left thumb

    # Right:
    # 12 = right shoulder
    # 14 = right elbow
    # 16 = right wrist
    # 18 = right pinky
    # 20 = right index
    # 22 = right thumb

    cv2.line(
        frame,
        points[11],
        points[12],
        (0, 255, 255),
        3
    )

    # LEFT ARM
    cv2.line(
        frame,
        points[11],
        points[13],
        (255, 255, 0),
        3
    )

    cv2.line(
        frame,
        points[13],
        points[15],
        (255, 255, 0),
        3
    )

    # RIGHT ARM
    cv2.line(
        frame,
        points[12],
        points[14],
        (0, 255, 0),
        3
    )

    cv2.line(
        frame,
        points[14],
        points[16],
        (0, 255, 0),
        3
    )

    # LEFT HAND
    cv2.line(frame, points[15], points[17], (255, 0, 0), 2)
    cv2.line(frame, points[15], points[19], (255, 0, 0), 2)
    cv2.line(frame, points[15], points[21], (255, 0, 0), 2)

    # Connect the hand points
    cv2.line(frame, points[17], points[19], (255, 0, 0), 2)
    cv2.line(frame, points[19], points[21], (255, 0, 0), 2)

    # RIGHT HAND
    cv2.line(frame, points[16], points[18], (0, 255, 0), 2)
    cv2.line(frame, points[16], points[20], (0, 255, 0), 2)
    cv2.line(frame, points[16], points[22], (0, 255, 0), 2)

    # Connect the hand points
    cv2.line(frame, points[18], points[20], (0, 255, 0), 2)
    cv2.line(frame, points[20], points[22], (0, 255, 0), 2)

    important_points = [
        11, 12,       # shoulders
        13, 14,       # elbows
        15, 16,       # wrists
        17, 18,       # pinkies
        19, 20,       # indexes
        21, 22        # thumbs
    ]

    for index in important_points:

        cv2.circle(
            frame,
            points[index],
            6,
            (0, 0, 255),
            -1
        )

# WORKOUT POSE DETECTION
def workout_pose_detection(landmarker, filename):

    cap = cv2.VideoCapture(filename)

    counter = 0
    stage = None  # "up" or "down"

    # tune these to your video after watching the angle values printed on-frame
    UP_ANGLE = 160
    DOWN_ANGLE = 90

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        result = landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.pose_landmarks:

            landmarks = result.pose_landmarks[0]
            h, w, _ = frame.shape

            draw_landmarks(frame, landmarks)

            s_idx, e_idx, w_idx = get_visible_arm(landmarks)
            shoulder = (landmarks[s_idx].x * w, landmarks[s_idx].y * h)
            elbow = (landmarks[e_idx].x * w, landmarks[e_idx].y * h)
            wrist = (landmarks[w_idx].x * w, landmarks[w_idx].y * h)

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle > UP_ANGLE:
                if stage == "down":
                    counter += 1
                stage = "up"
            elif angle < DOWN_ANGLE:
                stage = "down"

            cv2.putText(frame, f"Angle: {int(angle)}", (int(elbow[0]) + 10, int(elbow[1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        # counter display box
        cv2.rectangle(frame, (0, 0), (250, 80), (245, 117, 16), -1)
        cv2.putText(frame, "PUSHUPS", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(frame, str(counter), (15, 65), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(frame, stage if stage else "-", (120, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Workout Tracker", frame)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("Total pushups counted:", counter)

if __name__ == "__main__":

    workout_pose_detection(
        landmarker,
        str(VIDEO_PATH)
    )