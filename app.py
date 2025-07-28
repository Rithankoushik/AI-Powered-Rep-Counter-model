import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import numpy as np

# Initialize mediapipe pose
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    up = False
    counter = 0
    stframe = st.empty()

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break

        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[id] = (cx, cy)

            required_points = [12, 14]
            if all(pid in points for pid in required_points):
                cv2.circle(img, points[12], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[14], 15, (255, 0, 0), cv2.FILLED)

                # Rep counting logic
                if not up and points[14][1] + 40 < points[12][1]:
                    up = True
                    counter += 1
                elif points[14][1] > points[12][1]:
                    up = False

        # Overlay counter on the video
        cv2.putText(img, f"Reps: {counter}", (100, 150),
                    cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

        # Display the frame in the Streamlit app
        stframe.image(img, channels="BGR")

    cap.release()
    return counter  # ✅ return the final rep count

def main():
    st.set_page_config(page_title="💪 AI Rep Counter", layout="wide")
    st.title("🏋️ Exercise Rep Counter using MediaPipe")
    st.sidebar.title("Upload your workout video")

    uploaded_file = st.sidebar.file_uploader("Choose a video file (.mp4, .avi)", type=["mp4", "avi"])

    if uploaded_file is not None:
        # Save uploaded video to temp file
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        st.success("Processing your video...")

        # Run rep counter
        final_count = process_video(tfile.name)

        # ✅ Display final result
        st.success(f"✅ Total Reps Counted: **{final_count}**")

    else:
        st.info("👆 Upload a video from the sidebar to begin.")

if __name__ == "__main__":
    main()
