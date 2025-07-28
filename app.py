import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import numpy as np
import os

# Initialize MediaPipe
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    up = False
    counter = 0
    stframe = st.empty()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (1280, 720))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, _ = frame.shape
                points[id] = (int(lm.x * w), int(lm.y * h))

            if all(k in points for k in [12, 14]):
                cv2.circle(frame, points[12], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(frame, points[14], 15, (255, 0, 0), cv2.FILLED)

                if not up and points[14][1] + 40 < points[12][1]:
                    up = True
                    counter += 1
                elif points[14][1] > points[12][1]:
                    up = False

        cv2.putText(frame, f"Reps: {counter}", (100, 150),
                    cv2.FONT_HERSHEY_PLAIN, 12, (0, 255, 0), 12)
        stframe.image(frame, channels="BGR")

    cap.release()
    return counter

def main():
    st.set_page_config(page_title="🏋️ AI Rep Counter", layout="wide")
    st.title("💪 Exercise Repetition Counter with MediaPipe")
    st.sidebar.title("Upload your workout video")

    uploaded_file = st.sidebar.file_uploader("Upload .mp4 or .avi", type=["mp4", "avi"])

    if uploaded_file is not None:
        # Save video to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_file.read())
            temp_video_path = temp_video.name

        st.info("Processing video...")
        total_reps = process_video(temp_video_path)
        st.success(f"✅ Total reps counted: **{total_reps}**")

        # Clean up after
        os.remove(temp_video_path)

    else:
        st.info("👈 Upload a workout video from the sidebar to begin.")

if __name__ == "__main__":
    main()
