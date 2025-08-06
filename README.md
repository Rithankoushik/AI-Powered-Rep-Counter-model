## 🏋️ AI Exercise Repetition Counter

This project is an **AI-powered rep counter** that analyzes workout videos using [MediaPipe](https://mediapipe.dev/), [OpenCV](https://opencv.org/), and [Streamlit](https://streamlit.io/). It tracks body landmarks to **detect and count repetitions** — great for home workouts, gym monitoring, or fun fitness apps!

---

### 📹 Features

* 🧠 AI-based pose detection with MediaPipe
* 🎯 Repetition counting using joint movement logic
* 📈 Real-time rep tracking on uploaded videos
* 🖼️ Interactive UI with Streamlit
* ✅ Works with `.mp4` and `.avi` videos

---

### 🛠️ Tech Stack

| Tool      | Purpose                             |
| --------- | ----------------------------------- |
| Python    | Programming language                |
| MediaPipe | Pose detection & landmark tracking  |
| OpenCV    | Video frame processing              |
| Streamlit | Web interface for uploads & results |

---

### 🚀 How to Run Locally

#### 1. Clone the repository

```bash
git clone https://github.com/your-username/rep-counter-ai.git
cd rep-counter-ai
```

#### 2. Set up your environment

Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

##### `requirements.txt`

```txt
streamlit
opencv-python
mediapipe
numpy
```

#### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

### 📁 File Structure

```
rep-counter-ai/
├── app.py              # Streamlit UI for video upload and live counter
├── offline_counter.py  # Pure OpenCV + MediaPipe CLI script
├── requirements.txt    # Python dependencies
└── README.md           # You're here!
```

---

### 📸 Demo

[https://user-images.githubusercontent.com/demo-video.mp4](https://user-images.githubusercontent.com/demo-video.mp4) *(Add a link or GIF if you have one!)*

---

### 🤓 How It Works

* The app uses MediaPipe Pose to get body landmarks.
* It tracks the Y-coordinate of joints like the **elbow** and **shoulder**.
* When your elbow moves above your shoulder (and back down), it's counted as a rep.
* This logic is run frame-by-frame using OpenCV.

---

### 🧪 Example Movement Logic

```python
if not up and elbow_y + 40 < shoulder_y:
    up = True
    counter += 1
elif elbow_y > shoulder_y:
    up = False
```

---

### 🧠 Future Ideas

* Add support for more exercises (squats, push-ups, etc.)
* Use angles instead of raw pixel positions for better accuracy
* Real-time webcam tracking
* Sync with workout APIs or fitness dashboards

---

### 🙌 Credits

* [MediaPipe](https://mediapipe.dev/)
* [OpenCV](https://opencv.org/)
* [Streamlit](https://streamlit.io/)

---

### 📜 License

MIT License — feel free to use, modify, and share.
