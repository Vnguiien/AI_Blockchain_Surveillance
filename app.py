import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from detector import AbnormalDetector
from datetime import datetime


app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
PROCESSED_FOLDER = "static/processed"
EVIDENCE_FOLDER = "static/evidence"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(EVIDENCE_FOLDER, exist_ok=True)

print("Đang tải AI model, vui lòng chờ...")
detector = AbnormalDetector()
print("Tải AI model xong.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_video():
    print("\n==============================")
    print("Đã nhận request /analyze")

    if "video" not in request.files:
        print("Lỗi: không tìm thấy video")
        return jsonify({
            "success": False,
            "message": "Không tìm thấy video."
        }), 400

    file = request.files["video"]

    if file.filename == "":
        print("Lỗi: tên file rỗng")
        return jsonify({
            "success": False,
            "message": "Tên file rỗng."
        }), 400

    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    input_filename = f"{timestamp}_{filename}"
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)

    output_filename = f"processed_{timestamp}.mp4"
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)

    print("Đang lưu video vào:", input_path)
    file.save(input_path)

    try:
        print("Bắt đầu AI phân tích video...")

        result = detector.process_video(
            video_path=input_path,
            output_path=output_path,
            evidence_folder=EVIDENCE_FOLDER
        )

        print("AI phân tích xong")
        print("Video hash:", result["video_hash"])
        print("Số sự kiện phát hiện:", len(result["events"]))
        print("==============================\n")

        return jsonify({
            "success": True,
            "message": "Phân tích video thành công.",
            "original_video": f"/static/uploads/{input_filename}",
            "processed_video": f"/static/processed/{output_filename}",
            "video_hash": result["video_hash"],
            "events": result["events"]
        })

    except Exception as e:
        print("Lỗi khi phân tích video:", str(e))
        print("==============================\n")

        return jsonify({
            "success": False,
            "message": "Lỗi khi phân tích video: " + str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=False)