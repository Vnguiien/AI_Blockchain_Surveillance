# AI Blockchain Surveillance

Hệ thống nhận diện hành vi bất thường trong camera giám sát sử dụng AI kết hợp Blockchain.

## Chức năng chính

- Tải video lên web
- AI phát hiện người và vẽ khung xương người
- Nhận diện hành vi chạy, té ngã, đánh nhau
- Tạo ảnh bằng chứng
- Lưu thông tin bằng chứng lên Blockchain qua MetaMask

## Công nghệ sử dụng

- Python
- Flask
- OpenCV
- YOLO
- MediaPipe Pose
- Solidity
- Remix IDE
- MetaMask

## Cách chạy

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
