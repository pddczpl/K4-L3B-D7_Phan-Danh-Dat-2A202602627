# Báo cáo nhóm G23 — Lab 7: Embedding & Vector Store

**Chủ đề:** Đơn hàng Shopee. **Ngày thực nghiệm và lập báo cáo:** 20/09/2026.

| Thành viên | Phân công dự kiến |
|---|---|---|
| Phan Danh Đạt | HeadingChunker |
| Mai Hoàng Anh | FixedSizeChunker |
| Hoàng Văn Sơn | RecursiveChunker |

Báo cáo đã có corpus, bộ 5 câu hỏi và kết quả thật của ba cấu hình chạy trên cùng máy. Heading là chiến lược cá nhân của Đạt; các lần chạy fixed-size và recursive là thực nghiệm đối chiếu, chưa phải bằng chứng hai thành viên còn lại tự hoàn thành. Phần thảo luận trực tiếp, demo và ngày thuyết trình chưa thực hiện/chưa được cung cấp.

## 1. Bộ tài liệu và nguồn

Phạm vi gồm xem trạng thái, theo dõi, hủy đơn, thời hạn thanh toán trả trước và xử lý phía người bán. Cùng từ “hủy đơn” nhưng vai trò buyer/seller cần thao tác khác nhau, phù hợp để thử bộ lọc metadata. Các điều kiện SPX, trạng thái đơn và tên mục giao diện tạo tình huống đánh giá việc giữ đủ ngữ cảnh.

Corpus có **7 bản tóm lược tự biên soạn, tổng 4.135 ký tự phần thân**. Số ký tự dưới đây được tính sau khi bỏ frontmatter và chuẩn hóa xuống dòng bằng bộ nạp của runner; không phải độ dài toàn trang Shopee.

| # | Tài liệu trong corpus | Source URL | Ký tự phần thân | Metadata audience / category |
|---|---|---|---:|---|
| 1 | [Xem trạng thái đơn mua Shopee](../data/shopee-orders/buyer-order-status.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79472) | 578 | `buyer` / `order-status` |
| 2 | [Điều kiện người mua yêu cầu hủy đơn](../data/shopee-orders/buyer-cancel-order.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79182) | 732 | `buyer` / `cancellation` |
| 3 | [Đơn đã hủy và các nguyên nhân thường gặp](../data/shopee-orders/buyer-cancelled-order.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y) | 593 | `buyer` / `cancelled-order` |
| 4 | [Hạn thanh toán đơn trả trước](../data/shopee-orders/buyer-prepayment.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u) | 550 | `buyer` / `payment-deadline` |
| 5 | [Tra cứu đơn trong phần trò chuyện Shopee](../data/shopee-orders/buyer-track-chat.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79600) | 455 | `buyer` / `order-tracking` |
| 6 | [Người bán phản hồi yêu cầu hủy](../data/shopee-orders/seller-cancel-request.md) | [Bài chính thức](https://help.shopee.vn/portal/1/article/98754) | 615 | `seller` / `cancellation` |
| 7 | [Theo dõi kiện giao thất bại và hàng hoàn](../data/shopee-orders/seller-failed-delivery.md) | [Bài chính thức](https://help.shopee.vn/portal/1/article/102523) | 612 | `seller` / `failed-delivery` |

Tất cả tài liệu có `retrieved_at="2026-09-20"`, `document_version="not-stated"`, `language="vi"`, `platform="shopee"` và `content_type="authored-summary"`. Danh mục từng nguồn và thông tin truy vết nằm trong [sources.csv](../data/shopee-orders/sources.csv).

Corpus diễn giải các thông tin công khai bằng lời riêng, không lưu HTML, ảnh hay toàn văn trang nguồn. `license_or_permission="team-authored-summary-of-public-facts"` mô tả cách biên soạn, **không phải giấy phép hoặc sự cho phép của Shopee**. Ngày lấy là ngày đọc/tổng hợp; nguồn không nêu ngày hiệu lực trong phần đọc được nên không suy ra phiên bản mới nhất. Cách đọc trang, giới hạn chỉ mục và quyền sử dụng được ghi tại [SHOPEE_DATA_NOTES.md](../docs/SHOPEE_DATA_NOTES.md), kèm [điều khoản dịch vụ Shopee](https://help.shopee.vn/portal/4/article/77243).

### Schema metadata

| Trường | Kiểu / ví dụ | Vai trò |
|---|---|---|
| `doc_id`, `title` | Chuỗi; `buyer-cancel-order` | Nhận diện tài liệu gốc, kiểm tra và xóa toàn bộ chunk của tài liệu |
| `source_url`, `source_section` | Chuỗi; URL và mục nguồn | Dẫn nguồn, chỉ ra phần đã được tóm lược |
| `retrieved_at`, `document_version` | Chuỗi; `2026-09-20`, `not-stated` | Phân biệt ngày thu thập với ngày hiệu lực |
| `audience` | Chuỗi; `buyer` hoặc `seller` | Lọc theo vai trò trước khi xếp hạng |
| `category` | Chuỗi; `cancellation`, `payment-deadline` | Nhận diện chủ đề, có thể mở rộng bộ lọc |
| `language`, `platform` | Chuỗi; `vi`, `shopee` | Phân biệt ngôn ngữ và nền tảng khi mở rộng corpus |
| `content_type`, `license_or_permission` | Chuỗi; `authored-summary`, mô tả biên soạn | Nêu rõ loại tài liệu và nguồn gốc nội dung |
| `source_file`, `strategy`, `chunk_index` | Chuỗi, chuỗi, số nguyên từ 0 | Runner bổ sung để truy lại file và vị trí chunk |

Frontmatter không được đưa vào embedding. Toàn bộ metadata nguồn được gắn lại cho mỗi chunk; tiêu đề thuộc phần thân vẫn được giữ. Corpus không chứa đơn hàng thật, mã đơn của khách hàng, thông tin cá nhân hay khóa API.

## 2. Thiết kế và so sánh chiến lược

### Baseline bằng ba chunker của lab

Chạy `ChunkingStrategyComparator().compare(doc.content, chunk_size=350)` trên ba tài liệu đầu theo thứ tự tên file. Fixed-size của comparator dùng overlap 35; sentence gom tối đa 3 câu; recursive dùng giới hạn 350. Kết quả dưới đây đo trực tiếp trên cùng corpus ngày 20/09/2026; mỗi ô là **số chunk / độ dài trung bình (ký tự)**.

| Tài liệu | Fixed-size 350/35 | Sentence 3 câu | Recursive 350 |
|---|---:|---:|---:|
| `buyer-cancel-order` | 3 / 267,33 | 3 / 242,67 | 3 / 244,00 |
| `buyer-cancelled-order` | 2 / 314,00 | 3 / 196,67 | 2 / 296,50 |
| `buyer-order-status` | 2 / 306,50 | 2 / 288,00 | 3 / 192,67 |

Có thể tái tạo baseline bằng đoạn mã sau từ thư mục gốc:

```python
from pathlib import Path
from src import ChunkingStrategyComparator
from scripts.run_shopee_benchmark import load_documents
for doc in load_documents(Path("data/shopee-orders"))[:3]:
    stats = ChunkingStrategyComparator().compare(doc.content, chunk_size=350)
    print(doc.id, {k: (v["count"], v["avg_length"]) for k, v in stats.items()})
```

Số chunk ít hơn chưa chứng minh truy xuất tốt hơn. Cắt theo ký tự có thể chia điều kiện khỏi ngoại lệ; gom theo câu không đảm bảo mỗi đoạn mang tên mục. Corpus có tiêu đề do người biên soạn tạo nên heading có lợi thế cấu trúc, cần xét giới hạn này khi đọc kết quả.

### Cấu hình đưa vào benchmark

| Cấu hình | Lý do và giới hạn | Tổng chunk |
|---|---|---|---:|
| `HeadingChunker(chunk_size=500)` | Giữ tiêu đề và từng mục, giúp phân biệt SPX/khác SPX; khi đoạn dài vẫn phải chia tiếp | 15 |
| `FixedSizeChunker(chunk_size=350, overlap=50)` | Dễ triển khai, overlap giảm mất thông tin sát ranh giới; có thể trộn các mục | 15 |
| `RecursiveChunker(chunk_size=500)` | Ưu tiên ranh giới đoạn/câu trước khi cắt nhỏ; có thể gom nhiều ý chung một chunk | 13 |

Ba dòng trên là phân công cho nhóm; toàn bộ số liệu hiện có là các cấu hình đối chiếu chạy trên máy của Đạt. Mã tùy chỉnh nằm ở [src/heading_chunking.py](../src/heading_chunking.py).

Đối chiếu ba cấu hình benchmark trên cùng ba tài liệu baseline, lấy từ JSON thực nghiệm; mỗi ô vẫn là **số chunk / độ dài trung bình**:

| Tài liệu | Heading 500 | Fixed-size 350/50 | Recursive 500 |
|---|---:|---:|---:|
| `buyer-cancel-order` | 3 / 262,00 | 3 / 277,33 | 2 / 366,00 |
| `buyer-cancelled-order` | 2 / 308,00 | 2 / 321,50 | 2 / 296,50 |
| `buyer-order-status` | 2 / 301,00 | 2 / 314,00 | 2 / 289,00 |

Heading có lặp tiêu đề để giữ ngữ cảnh, fixed-size có overlap nên tổng độ dài chunk có thể lớn hơn thân tài liệu. Baseline 350/35 và benchmark 350/50 là hai cấu hình khác nhau; không dùng chung số liệu.

## 3. Bộ 5 câu hỏi và phương pháp đánh giá

Bộ câu hỏi được cố định trong [benchmark_queries.json](../data/shopee-orders/benchmark_queries.json). Đáp án chuẩn lấy từ corpus có nguồn, không lấy từ câu trả lời mô hình. Cột bằng chứng dùng chunk index của **heading**, bắt đầu từ 0; chi tiết các cấu hình khác có trong bản xuất benchmark.

| ID | Câu hỏi chung | Gold answer | Tài liệu / chunk chứa bằng chứng |
|---|---|---|---|
| Q1 | Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua? | Mở **Tôi > Đơn mua** để xem tiến trình đơn hàng. | `buyer-order-status` / 0 |
| Q2 | Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không? | Phải đợi người bán chấp nhận; nếu từ chối, đơn vẫn tiếp tục giao. Lọc `audience=buyer`. | `buyer-cancel-order` / 0 |
| Q3 | Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không? | Không khôi phục đơn đã hủy; phải đặt đơn mới, có thể trao đổi giá với shop nhưng không mặc định giữ ưu đãi cũ. | `buyer-cancelled-order` / 0 |
| Q4 | Đơn trả trước bằng thẻ tín dụng hoặc ghi nợ cần thanh toán trong bao lâu, nếu quá hạn thì sao? | Trong **12 giờ** từ lúc đặt hàng thành công; quá hạn không thanh toán thì hệ thống tự động hủy. | `buyer-prepayment` / 0 |
| Q5 | Tôi xử lý yêu cầu hủy đơn hàng như thế nào? | Với vai trò người bán trên **Kênh Quản Lý Shop**: **Đơn hủy > Chờ phản hồi > Xem thêm**; đồng ý chuyển **Đã hủy**, từ chối về **Đã đóng gói** trong **Chờ lấy hàng**. Lọc `audience=seller`. | `seller-cancel-request` / 0 |

Thực nghiệm dùng `gemini-embedding-001`, 3.072 chiều, `RETRIEVAL_DOCUMENT` cho chunk và `RETRIEVAL_QUERY` cho câu hỏi. Vector được chuẩn hóa L2; dot product tương ứng cosine. Tất cả chiến lược cùng corpus, câu hỏi và `top_k=3`; bộ lọc là AND chính xác, áp dụng trước xếp hạng.

`KnowledgeBaseAgent` nhận đúng top-3 đã truy xuất rồi gọi **Gemini `gemini-3.1-flash-lite` thật**, temperature 0. Với Q2/Q5, vai trò và metadata được thêm vào câu hỏi gửi LLM; embedding truy vấn vẫn dùng câu hỏi gốc. Chỉ sinh câu trả lời cho cấu hình chính của mỗi câu; nhánh không lọc chỉ đo retrieval, không suy diễn chất lượng câu trả lời chưa được sinh.

Kết quả ghi lúc **10:25:48 ngày 20/09/2026 (UTC+7)**. Bản cuối có 15 câu trả lời: 11 lượt generate mới và 4 câu đọc lại từ cache cùng model/prompt; 48 embedding được tái sử dụng từ cache API thật. Đây không phải kết quả mock. Cache có khóa theo model/task/nội dung, giúp chạy lại không gọi API thừa.

**Hit@3** bằng 1 khi ít nhất một chunk top-3 có đúng `doc_id` và đủ tất cả cụm bằng chứng của một mục evidence trong **cùng chunk**, không phân biệt hoa/thường và khoảng trắng. Đây là tiêu chí tìm được bằng chứng, không tự chứng minh LLM trả lời đúng. Câu trả lời được đọc đối chiếu với gold và nguồn; bản đánh giá có hỗ trợ trợ lý AI lưu tại [shopee_answer_review.json](shopee_answer_review.json).

### Kết quả đo và đọc đối chiếu

| Cấu hình | Hit@3 | Bằng chứng ở top-1 | Câu trả lời đúng hoàn toàn | Điểm tham khảo /10 |
|---|---:|---:|---:|---:|
| Heading 500 | 5/5 | 5/5 | 5/5 | 10 |
| Fixed-size 350/50 | 5/5 | 4/5 | 4/5 | 8 |
| Recursive 500 | 5/5 | 5/5 | 4/5 | 9 |

Điểm tham khảo diễn giải [rubric của lab](../docs/SCORING.md): 2 khi top-1 đủ bằng chứng và câu trả lời đúng; 1 khi bằng chứng ở hạng thấp hơn hoặc câu trả lời thiếu/sai một chi tiết; 0 nếu không có bằng chứng top-3. Đây không phải điểm giảng viên hay tổng điểm phần nhóm.

| Câu | Heading | Fixed-size | Recursive | Nhận xét từ dữ liệu thực |
|---|---:|---:|---:|---|
| Q1 | 2 | 2 | 2 | Cả ba trả lời đúng nơi xem trạng thái |
| Q2 | 2 | 1 | 2 | Fixed-size đủ bằng chứng ở rank 2; agent vẫn trả lời đúng và trích [2] |
| Q3 | 2 | 2 | 2 | Cả ba phân biệt đặt mới với khôi phục đơn cũ |
| Q4 | 2 | 2 | 2 | Cả ba nêu đúng 12 giờ và hậu quả quá hạn |
| Q5 | 2 | 1 | 1 | Fixed-size/recursive đổi tên giao diện thành “Kênh Người Bán” ở phần trả lời |

Heading tốt nhất theo lần chạy và cách đối chiếu này vì bằng chứng luôn ở top-1 và 5 câu trả lời đều khớp nguồn. Tuy nhiên, chỉ có 5 câu hỏi trên corpus 7 bản tóm lược được cấu trúc sẵn; chưa thể kết luận heading luôn tốt nhất hoặc khác biệt do chunking là nguyên nhân duy nhất của lỗi LLM.

### Tác dụng của metadata

| Câu / cấu hình | Chunk đúng audience khi không lọc | Khi lọc | Hit@3 trước → sau |
|---|---:|---:|---|
| Q5 / heading | 1/3 seller | 3/3 seller | 1 → 1 |
| Q5 / fixed-size | 1/3 seller | 3/3 seller | 1 → 1 |
| Q5 / recursive | 1/3 seller | 3/3 seller | 1 → 1 |
| Q2 / cả ba | 3/3 buyer | 3/3 buyer | 1 → 1 |

Q5 không lọc trộn hai chunk hướng dẫn người mua vào top-3; lọc seller loại phần sai vai trò. **Hit@3 không tăng**, vì bằng chứng đúng đã ở top-1 trước khi lọc. Tỷ lệ đúng audience 3/3 không đồng nghĩa cả ba chunk đều đủ đáp án: vẫn có chunk về giao thất bại nằm trong top-3. Với Q2, cả danh sách kết quả và thứ tự đều không đổi vì top-3 vốn đã là buyer.

## 4. Phân tích lỗi và hướng cải thiện

**Lỗi 1 — Fixed-size/Q2 xếp ngoại lệ cao hơn điều kiện cần hỏi.** Chunk `buyer-cancel-order`, index 1, score **0,850080** đứng đầu nhưng không đủ bằng chứng; chunk index 0 chứa điều kiện hãng khác SPX chỉ đứng thứ hai, score **0,829590**. Cửa sổ ký tự đưa nội dung ngoại lệ SPX vào chunk khác và truy vấn cũng có từ SPX. Đây là hiện tượng xếp hạng quan sát được, chưa phải bằng chứng từ khóa là nguyên nhân duy nhất. Agent hiện vẫn trả lời đúng nhờ đọc [2], nhưng giảm top-k xuống 1 sẽ bỏ mất chunk đủ điều kiện theo tiêu chí đã đặt.

Đề xuất kiểm thử tiếp: giữ tiêu đề hãng/trạng thái trên mỗi chunk, thêm metadata `carrier`/`order_status` khi có thể gán nhất quán, hoặc thử rerank. Chưa chạy các phương án này nên chưa báo cáo mức cải thiện.

**Lỗi 2 — Recursive/Q5 truy xuất đúng nhưng agent tự đổi tên giao diện.** Chunk đứng đầu `seller-cancel-request`, index 0, score **0,766838** ghi **Kênh Quản Lý Shop** và đủ cả nhánh đồng ý/từ chối. Câu trả lời lại dùng **Kênh Người Bán** nhiều lần; corpus không cho phép đồng nhất hai tên. Fixed-size cũng mắc lỗi ở câu mở đầu, dù các bước sau dùng lại tên đúng. Vì vậy cả hai câu được đánh giá partial, không chấm “đúng” chỉ dựa vào Hit@3.

Đề xuất thêm chỉ dẫn giữ nguyên tên giao diện/nhãn nút, kiểm tra thực thể trước khi trả lời và đánh giá lặp nhiều lần sinh. Lọc audience giải quyết sai vai trò nhưng không tự ngăn mô hình thêm hoặc đổi chi tiết. Các cải tiến này chưa được thực nghiệm trong kết quả hiện tại.

## 5. Kịch bản demo và việc nhóm còn phải xác nhận

Kịch bản chuẩn bị gồm 5 bước;

1. Mở một file corpus và nguồn Shopee tương ứng; chỉ ra phần tóm lược, ngày lấy, phiên bản chưa nêu và audience.
2. Cho xem một tài liệu được chia bởi heading, fixed-size và recursive; đối chiếu số chunk cùng ranh giới điều kiện SPX.
3. Mở Q2 trong bản benchmark: so top-1 của heading với top-1/top-2 của fixed-size và nguồn [2] trong câu trả lời.
4. Mở Q5 trước/sau lọc seller: chỉ ra tỷ lệ đúng vai trò 1/3 → 3/3, Hit@3 không đổi, rồi kiểm tra lỗi tên giao diện của recursive.
5. Tóm tắt số liệu 5 câu, giới hạn corpus nhỏ và các cải tiến đề xuất; mời hai thành viên đối chiếu kết quả tự chạy trước khi kết luận chung.

Bài học rút ra từ thực nghiệm hiện có: giữ điều kiện cùng tiêu đề giúp đọc bằng chứng; metadata cần được đo đúng mục đích; tìm đúng chunk và trả lời đúng là hai việc phải kiểm tra riêng. Đây là phân tích từ các lần chạy hiện tại, chưa phải nội dung được ghi nhận từ buổi trao đổi với bạn học.

Trước khi nộp bản nhóm cuối cùng cần thay tên tạm/MSSV của hai thành viên, để mỗi người tự chạy cấu hình được giao, đối chiếu sai khác và bổ sung ngày demo cùng kết quả thảo luận thực. Không tự ghi nhận hoàn thành thay cho các hoạt động này.

## 6. Minh chứng và cách chạy lại

- [Runner benchmark](../scripts/run_shopee_benchmark.py) và [HeadingChunker](../src/heading_chunking.py).
- [JSON kết quả thật](shopee_benchmark_gemini_gemini.json): cấu hình, corpus hash, top-3 đầy đủ, score, nguồn, câu trả lời và đối chiếu không lọc.
- [Chi tiết dễ đọc](SHOPEE_BENCHMARK_DETAILS.md): đầy đủ 15 lượt hỏi/đáp của ba cấu hình với nội dung chunk.
- [Bản xuất văn bản cá nhân](ket_qua_benchmark.txt): 5 lượt hỏi/đáp theo chiến lược Heading của Đạt.
- [Đánh giá câu trả lời](shopee_answer_review.json), [ghi chú nguồn](../docs/SHOPEE_DATA_NOTES.md), [manifest nguồn](../data/shopee-orders/sources.csv) và [5 câu hỏi chuẩn](../data/shopee-orders/benchmark_queries.json).
- [Báo cáo cá nhân](REPORT_CANHAN.md) và [log kiểm thử Shopee](pytest_shopee.txt).

Từ thư mục gốc, với môi trường đã cài `google-genai` và khóa cấu hình riêng trong `.env`:

```powershell
.\venv\Scripts\python.exe -m scripts.run_shopee_benchmark --provider gemini --llm gemini --llm-model gemini-3.5-flash-lite
```

Chạy `--provider mock --llm extractive` chỉ kiểm tra luồng offline;
