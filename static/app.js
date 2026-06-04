let currentAccount = null;
let analyzedEvents = [];

const CONTRACT_ADDRESS = "0xF7Fd015853FDcF9eb30BFD9A7bB7B5e42eBe204a";

const CONTRACT_ABI = [
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "internalType": "uint256", "name": "id", "type": "uint256"},
            {"indexed": false, "internalType": "string", "name": "behaviorType", "type": "string"},
            {"indexed": false, "internalType": "string", "name": "videoHash", "type": "string"},
            {"indexed": false, "internalType": "string", "name": "evidenceImage", "type": "string"},
            {"indexed": false, "internalType": "string", "name": "timestampText", "type": "string"},
            {"indexed": true, "internalType": "address", "name": "reporter", "type": "address"},
            {"indexed": false, "internalType": "uint256", "name": "blockTime", "type": "uint256"}
        ],
        "name": "EvidenceAdded",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_behaviorType", "type": "string"},
            {"internalType": "string", "name": "_videoHash", "type": "string"},
            {"internalType": "string", "name": "_evidenceImage", "type": "string"},
            {"internalType": "string", "name": "_timestampText", "type": "string"}
        ],
        "name": "addEvidence",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalEvidence",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
];

console.log("app.js đã load thành công");

async function connectWallet() {
    if (!window.ethereum) {
        alert("Bạn cần cài MetaMask trên Chrome.");
        return;
    }

    try {
        const accounts = await window.ethereum.request({
            method: "eth_requestAccounts"
        });

        currentAccount = accounts[0];

        document.getElementById("walletAddress").innerText =
            "Ví: " + currentAccount;

        document.getElementById("systemStatus").innerText =
            "Đã kết nối MetaMask";

    } catch (error) {
        console.error("Lỗi MetaMask:", error);
        alert("Không thể kết nối MetaMask.");
    }
}

async function uploadVideo() {
    const input = document.getElementById("videoInput");

    if (!input.files || input.files.length === 0) {
        alert("Vui lòng chọn video.");
        return;
    }

    const file = input.files[0];

    // Hiển thị video gốc ngay lập tức
    const originalVideo = document.getElementById("originalVideo");
    originalVideo.src = URL.createObjectURL(file);
    originalVideo.load();

    const formData = new FormData();
    formData.append("video", file);

    document.getElementById("systemStatus").innerText =
        "AI đang phân tích video... Vui lòng chờ.";

    document.getElementById("eventList").innerHTML = `
        <div class="event-card">
            <h3>Đang xử lý...</h3>
            <p>AI đang phân tích video. Nếu video dài, quá trình này có thể mất vài phút.</p>
        </div>
    `;

    document.getElementById("videoHash").innerText = "Đang tạo hash...";
    document.getElementById("processedVideo").removeAttribute("src");
    document.getElementById("processedVideo").load();

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        console.log("Kết quả từ server:", data);

        if (!data.success) {
            alert(data.message || "Phân tích thất bại.");
            document.getElementById("systemStatus").innerText =
                "Phân tích thất bại";

            document.getElementById("eventList").innerHTML = `
                <div class="event-card">
                    <h3>Lỗi phân tích</h3>
                    <p>${data.message || "Không rõ nguyên nhân."}</p>
                </div>
            `;

            return;
        }

        analyzedEvents = data.events || [];

        const processedVideo = document.getElementById("processedVideo");
        processedVideo.src = data.processed_video + "?t=" + new Date().getTime();
        processedVideo.load();

        document.getElementById("videoHash").innerText = data.video_hash;

        renderEvents(analyzedEvents);

        document.getElementById("systemStatus").innerText =
            "Phân tích hoàn tất";

    } catch (error) {
        console.error("Lỗi khi gửi video:", error);

        document.getElementById("systemStatus").innerText =
            "Có lỗi xảy ra";

        document.getElementById("eventList").innerHTML = `
            <div class="event-card">
                <h3>Lỗi</h3>
                <p>Không thể phân tích video. Hãy xem lỗi trong PowerShell hoặc Console.</p>
            </div>
        `;

        alert("Lỗi khi phân tích video.");
    }
}

function renderEvents(events) {
    const eventList = document.getElementById("eventList");
    eventList.innerHTML = "";

    if (!events || events.length === 0) {
        eventList.innerHTML = `
            <div class="event-card">
                <div>
                    <span class="badge">SAFE</span>
                    <h3>Không phát hiện hành vi bất thường</h3>
                    <p>Video chưa phát hiện chạy, té ngã hoặc đánh nhau.</p>
                </div>
            </div>
        `;
        return;
    }

    events.forEach((event, index) => {
        const card = document.createElement("div");
        card.className = "event-card";

        card.innerHTML = `
            <img src="${event.evidence_image}" alt="Evidence">

            <div>
                <span class="badge">${event.behavior_type}</span>
                <h3>${event.label}</h3>
                <p><b>Thời điểm:</b> ${event.timestamp}s</p>
                <p><b>Độ tin cậy:</b> ${event.score}</p>
                <p><b>Video Hash:</b> ${event.video_hash}</p>

                <button class="blockchain-btn" onclick="saveToBlockchain(${index})">
                    Lưu bằng chứng lên Blockchain
                </button>

                <p id="tx_${index}" class="tx"></p>
            </div>
        `;

        eventList.appendChild(card);
    });
}

async function saveToBlockchain(index) {
    if (!window.ethereum) {
        alert("Bạn cần cài MetaMask.");
        return;
    }

    if (!currentAccount) {
        await connectWallet();
    }

    const event = analyzedEvents[index];

    if (!event) {
        alert("Không tìm thấy dữ liệu bằng chứng.");
        return;
    }

    try {
        if (typeof ethers === "undefined") {
            alert("Không tải được thư viện ethers. Kiểm tra Internet.");
            return;
        }

        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();

        const contract = new ethers.Contract(
            CONTRACT_ADDRESS,
            CONTRACT_ABI,
            signer
        );

        const tx = await contract.addEvidence(
            event.behavior_type,
            event.video_hash,
            event.evidence_image,
            String(event.timestamp) + "s"
        );

        document.getElementById(`tx_${index}`).innerText =
            "Đang ghi blockchain: " + tx.hash;

        await tx.wait();

        document.getElementById(`tx_${index}`).innerText =
            "Đã lưu Blockchain. Tx Hash: " + tx.hash;

    } catch (error) {
        console.error("Lỗi blockchain:", error);

        alert(
            "Không thể lưu blockchain. Hãy kiểm tra:\n" +
            "1. MetaMask đã kết nối chưa\n" +
            "2. Remix deploy cùng network với MetaMask chưa\n" +
            "3. Contract address có đúng không"
        );
    }
}