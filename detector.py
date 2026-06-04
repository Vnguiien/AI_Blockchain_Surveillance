import cv2
import os
import time
import hashlib
import numpy as np
import mediapipe as mp
from ultralytics import YOLO


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


class AbnormalDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.previous_centers = {}
        self.previous_time = time.time()

    def calculate_hash(self, file_path):
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)

        return sha256.hexdigest()

    def detect_people(self, frame):
        results = self.model(frame, verbose=False)
        people = []

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                # YOLO COCO class 0 = person
                if cls == 0 and conf >= 0.4:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    people.append({
                        "box": (x1, y1, x2, y2),
                        "conf": conf,
                        "center": ((x1 + x2) // 2, (y1 + y2) // 2)
                    })

        return people

    def draw_pose(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(0, 255, 255),
                    thickness=2,
                    circle_radius=3
                ),
                mp_drawing.DrawingSpec(
                    color=(0, 120, 255),
                    thickness=2
                )
            )

        return frame

    def distance(self, p1, p2):
        return np.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    def merge_boxes(self, box1, box2):
        x1 = min(box1[0], box2[0])
        y1 = min(box1[1], box2[1])
        x2 = max(box1[2], box2[2])
        y2 = max(box1[3], box2[3])

        return x1, y1, x2, y2

    def analyze_behaviors(self, people):
        behaviors = []

        current_time = time.time()
        dt = max(current_time - self.previous_time, 0.001)

        for i, person in enumerate(people):
            x1, y1, x2, y2 = person["box"]
            cx, cy = person["center"]

            width = x2 - x1
            height = y2 - y1

            speed = 0

            if i in self.previous_centers:
                old_cx, old_cy = self.previous_centers[i]
                speed = self.distance((cx, cy), (old_cx, old_cy)) / dt

            self.previous_centers[i] = (cx, cy)

            # Nhận diện té ngã:
            # Người nằm ngang, chiều rộng lớn hơn chiều cao
            if height > 0 and width > height * 1.25:
                behaviors.append({
                    "type": "FALLING",
                    "label": "Phát hiện té ngã",
                    "box": person["box"],
                    "score": 0.90
                })

            # Nhận diện chạy:
            # Tốc độ dịch chuyển giữa các frame lớn
            if speed > 220:
                behaviors.append({
                    "type": "RUNNING",
                    "label": "Phát hiện chạy nhanh",
                    "box": person["box"],
                    "score": min(speed / 500, 1.0)
                })

        # Nhận diện đánh nhau:
        # Từ 2 người trở lên đứng gần nhau
        if len(people) >= 2:
            for i in range(len(people)):
                for j in range(i + 1, len(people)):
                    p1 = people[i]
                    p2 = people[j]

                    d = self.distance(p1["center"], p2["center"])

                    if d < 180:
                        behaviors.append({
                            "type": "FIGHTING",
                            "label": "Nghi ngờ đánh nhau",
                            "box": self.merge_boxes(p1["box"], p2["box"]),
                            "score": 0.85
                        })

        self.previous_time = current_time

        return behaviors

    def draw_results(self, frame, people, behaviors):
        for person in people:
            x1, y1, x2, y2 = person["box"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (60, 220, 255),
                2
            )

            cv2.putText(
                frame,
                "PERSON",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (60, 220, 255),
                2
            )

        for behavior in behaviors:
            x1, y1, x2, y2 = behavior["box"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                3
            )

            cv2.putText(
                frame,
                behavior["label"],
                (x1, max(y1 - 35, 30)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                f"Score: {behavior['score']:.2f}",
                (x1, max(y1 - 10, 50)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

        return frame

    def process_video(self, video_path, output_path, evidence_folder):
        self.previous_centers = {}
        self.previous_time = time.time()

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise Exception("Không thể mở video. Vui lòng kiểm tra định dạng video.")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps <= 0:
            fps = 25

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if width <= 0 or height <= 0:
            raise Exception("Video không hợp lệ hoặc bị lỗi.")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_index = 0
        abnormal_events = []
        saved_event_types = set()

        video_hash = self.calculate_hash(video_path)

        print("FPS:", fps)
        print("Kích thước video:", width, "x", height)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame_index += 1

            # Resize frame khi phân tích để chạy nhanh hơn
            small_frame = cv2.resize(frame, (640, int(640 * height / width)))

            # Chỉ phân tích mỗi 5 frame để tăng tốc
            if frame_index % 5 == 0:
                people_small = self.detect_people(small_frame)

                # Quy đổi tọa độ từ frame nhỏ về frame gốc
                scale_x = width / small_frame.shape[1]
                scale_y = height / small_frame.shape[0]

                people = []

                for p in people_small:
                    x1, y1, x2, y2 = p["box"]

                    x1 = int(x1 * scale_x)
                    y1 = int(y1 * scale_y)
                    x2 = int(x2 * scale_x)
                    y2 = int(y2 * scale_y)

                    people.append({
                        "box": (x1, y1, x2, y2),
                        "conf": p["conf"],
                        "center": ((x1 + x2) // 2, (y1 + y2) // 2)
                    })

                behaviors = self.analyze_behaviors(people)

                frame = self.draw_pose(frame)
                frame = self.draw_results(frame, people, behaviors)

                timestamp_video = frame_index / fps

                cv2.putText(
                    frame,
                    f"Time: {timestamp_video:.2f}s",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2
                )

                for behavior in behaviors:
                    event_key = behavior["type"]

                    # Mỗi loại hành vi lưu 1 ảnh bằng chứng
                    if event_key not in saved_event_types:
                        evidence_name = f"evidence_{event_key}_{int(time.time())}.jpg"
                        evidence_path = os.path.join(evidence_folder, evidence_name)

                        cv2.imwrite(evidence_path, frame)

                        abnormal_events.append({
                            "behavior_type": behavior["type"],
                            "label": behavior["label"],
                            "score": round(float(behavior["score"]), 2),
                            "timestamp": round(timestamp_video, 2),
                            "evidence_image": f"/static/evidence/{evidence_name}",
                            "video_hash": video_hash
                        })

                        print("Phát hiện:", behavior["type"], "tại", round(timestamp_video, 2), "giây")

                        saved_event_types.add(event_key)

            else:
                # Những frame không phân tích vẫn ghi ra video
                cv2.putText(
                    frame,
                    "AI CCTV ANALYSIS",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2
                )

            out.write(frame)

        cap.release()
        out.release()

        print("Tổng số frame:", frame_index)

        return {
            "video_hash": video_hash,
            "events": abnormal_events
        }