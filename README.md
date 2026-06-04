# AI Blockchain Surveillance

## Giới thiệu

**AI Blockchain Surveillance** là hệ thống nhận diện hành vi bất thường trong camera giám sát sử dụng **trí tuệ nhân tạo AI** kết hợp **Blockchain**. Hệ thống cho phép người dùng tải video giám sát lên website, sau đó AI sẽ phân tích video để phát hiện người, vẽ khung xương người và nhận diện một số hành vi bất thường như **chạy**, **té ngã** và **nghi ngờ đánh nhau**.

Khi phát hiện hành vi bất thường, hệ thống sẽ tạo **ảnh bằng chứng**, sinh **mã hash SHA-256** của video và cho phép lưu thông tin bằng chứng lên Blockchain thông qua **MetaMask** và **smart contract Solidity** triển khai bằng **Remix IDE**.

---

## Mục tiêu đề tài

* Xây dựng hệ thống web cho phép tải video giám sát.
* Ứng dụng AI để phát hiện người trong video.
* Vẽ khung xương người, hay còn gọi là que người.
* Phân tích và nhận diện hành vi bất thường.
* Tạo ảnh bằng chứng khi phát hiện sự kiện.
* Tạo mã hash cho video để kiểm tra tính toàn vẹn.
* Lưu thông tin bằng chứng lên Blockchain.
* Kết nối website với MetaMask để xác nhận giao dịch.

---

## Chức năng chính

* Upload video từ máy tính lên website.
* Hiển thị video gốc sau khi chọn file.
* Phân tích video bằng AI.
* Phát hiện người trong video bằng YOLO.
* Vẽ khung xương người bằng MediaPipe Pose.
* Nhận diện hành vi:

  * Chạy nhanh.
  * Té ngã.
  * Nghi ngờ đánh nhau.
* Xuất video đã phân tích.
* Tạo ảnh bằng chứng khi phát hiện hành vi bất thường.
* Hiển thị mã hash SHA-256 của video.
* Kết nối MetaMask.
* Lưu bằng chứng lên Blockchain.
* Hiển thị mã giao dịch sau khi lưu Blockchain thành công.

---

## Công nghệ sử dụng

### AI và xử lý hình ảnh

* **Python**: ngôn ngữ chính để xây dựng backend và xử lý AI.
* **OpenCV**: đọc video, xử lý từng frame và xuất video kết quả.
* **YOLO**: phát hiện người trong khung hình.
* **MediaPipe Pose**: vẽ khung xương người, hỗ trợ phân tích tư thế.

### Web

* **Flask**: xây dựng web server.
* **HTML**: xây dựng cấu trúc giao diện.
* **CSS**: thiết kế giao diện hiện đại.
* **JavaScript**: xử lý sự kiện upload video, kết nối MetaMask và gọi API.

### Blockchain

* **Solidity**: viết smart contract lưu thông tin bằng chứng.
* **Remix IDE**: biên dịch và triển khai smart contract.
* **MetaMask**: kết nối ví và xác nhận giao dịch.
* **Ethers.js**: kết nối website với smart contract.

---

## Cấu trúc thư mục

```txt
AI_Blockchain_Surveillance/
│
├── app.py
├── detector.py
├── requirements.txt
├── README.md
│
├── contracts/
│   └── SecurityLog.sol
│
├── templates/
│   └── index.html
│
├── static/
│   ├── app.js
│   ├── style.css
│   ├── uploads/
│   ├── processed/
│   └── evidence/
```

Trong đó:

* `app.py`: file chính chạy Flask server.
* `detector.py`: xử lý AI, phát hiện người, vẽ khung xương và nhận diện hành vi.
* `requirements.txt`: danh sách thư viện Python cần cài đặt.
* `contracts/SecurityLog.sol`: smart contract Solidity.
* `templates/index.html`: giao diện HTML.
* `static/app.js`: xử lý JavaScript, upload video và kết nối Blockchain.
* `static/style.css`: giao diện CSS.
* `static/uploads`: lưu video người dùng tải lên.
* `static/processed`: lưu video sau khi AI phân tích.
* `static/evidence`: lưu ảnh bằng chứng.

---

## Cài đặt môi trường

### 1. Tải project về máy

Nếu dùng Git:

```bash
git clone https://github.com/ten-github-cua-ban/AI_Blockchain_Surveillance.git
cd AI_Blockchain_Surveillance
```

Hoặc tải project bằng nút **Code → Download ZIP** trên GitHub, sau đó giải nén.

---

### 2. Tạo môi trường ảo

Trên Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Nếu chưa có file `requirements.txt`, có thể cài trực tiếp:

```bash
pip install flask opencv-python mediapipe ultralytics numpy werkzeug
```

---

## Chạy chương trình

Trong thư mục project, chạy:

```bash
python app.py
```

Khi terminal hiển thị:

```txt
Running on http://127.0.0.1:5000
```

Mở trình duyệt và truy cập:

```txt
http://127.0.0.1:5000
```

---

## Cách sử dụng hệ thống

1. Mở website tại `http://127.0.0.1:5000`.
2. Bấm **Kết nối MetaMask** để kết nối ví.
3. Chọn video giám sát từ máy tính.
4. Bấm **Phân tích video**.
5. Chờ AI xử lý video.
6. Xem video sau phân tích.
7. Kiểm tra ảnh bằng chứng và mã hash video.
8. Nếu có hành vi bất thường, bấm **Lưu bằng chứng lên Blockchain**.
9. Xác nhận giao dịch trong MetaMask.
10. Sau khi giao dịch thành công, hệ thống hiển thị mã giao dịch.

---

## Smart Contract

Smart contract dùng để lưu thông tin bằng chứng lên Blockchain.

Thông tin được lưu gồm:

* ID bằng chứng.
* Loại hành vi bất thường.
* Mã hash video.
* Đường dẫn ảnh bằng chứng.
* Thời điểm phát hiện.
* Địa chỉ ví người gửi.
* Thời gian ghi nhận trên Blockchain.

File smart contract nằm tại:

```txt
contracts/SecurityLog.sol
```

---

## Triển khai smart contract bằng Remix IDE

1. Mở Remix IDE.
2. Tạo file `SecurityLog.sol`.
3. Copy nội dung smart contract trong thư mục `contracts`.
4. Chọn **Solidity Compiler**.
5. Compile contract.
6. Sang tab **Deploy & Run Transactions**.
7. Chọn môi trường **Injected Provider - MetaMask**.
8. Bấm **Deploy**.
9. Xác nhận giao dịch trong MetaMask.
10. Sau khi deploy, copy **Contract Address**.
11. Dán địa chỉ contract vào file:

```txt
static/app.js
```

Tìm dòng:

```javascript
const CONTRACT_ADDRESS = "DIA_CHI_CONTRACT";
```

Thay bằng địa chỉ contract đã deploy.

---

## Kết quả đầu ra

Sau khi phân tích video, hệ thống tạo ra:

* Video gốc đã upload.
* Video sau phân tích AI.
* Ảnh bằng chứng.
* Mã hash SHA-256 của video.
* Danh sách hành vi bất thường.
* Mã giao dịch Blockchain nếu lưu thành công.

---

## Một số hành vi được nhận diện

| Hành vi  | Mô tả                                      |
| -------- | ------------------------------------------ |
| RUNNING  | Phát hiện người di chuyển nhanh            |
| FALLING  | Phát hiện người có dấu hiệu té ngã         |
| FIGHTING | Nghi ngờ có hành vi đánh nhau hoặc va chạm |

---

## Lưu ý

* Nên dùng video ngắn từ 5 đến 15 giây để kiểm thử nhanh.
* Video càng dài thì thời gian xử lý càng lâu.
* MediaPipe Pose hoạt động tốt hơn khi người trong video rõ toàn thân.
* Nhận diện đánh nhau trong bản demo còn đơn giản, có thể nhầm khi nhiều người đứng gần nhau.
* Cần kết nối đúng mạng Blockchain giữa Remix và MetaMask.
* Không nên upload thư mục `venv`, video nặng hoặc file model lên GitHub.

---

## Những file không nên đưa lên GitHub

Nên bỏ qua các file/thư mục sau:

```txt
venv/
__pycache__/
*.pyc
yolov8n.pt
static/uploads/
static/processed/
static/evidence/
.env
```

Có thể tạo file `.gitignore` với nội dung:

```gitignore
venv/
__pycache__/
*.pyc

yolov8n.pt

static/uploads/
static/processed/
static/evidence/

.env
*.log
```

---

## Hướng phát triển

* Phân tích camera trực tiếp theo thời gian thực.
* Nâng cao độ chính xác nhận diện hành vi.
* Lưu bằng chứng lên IPFS và Blockchain.
* Thêm cảnh báo qua email, Telegram hoặc app.

---

## Tác giả

Nguyễn Văn Nguyên
Lớp CNTT 16.01
Khoa Công nghệ Thông tin
Trường Đại học Đại Nam

