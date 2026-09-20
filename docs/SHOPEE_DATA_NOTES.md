# G23 — Nguồn dữ liệu về đơn hàng Shopee

## Phạm vi bộ dữ liệu

Nhóm G23 đổi đề tài sang **đơn hàng Shopee**: trạng thái, theo dõi, hủy đơn, thanh toán trả trước và xử lý đơn phía người bán. Đây là nội dung quy định/hướng dẫn dành cho người mua và người bán trong phạm vi K4-L3B.

Điểm xuất phát là [danh mục Đơn hàng do nhóm chọn](https://help.shopee.vn/portal/4/category/60-%25C4%2590%25C6%25A1n-H%25C3%25A0ng-V%25E1%25BA%25ADn-Chuy%25E1%25BB%2583n/703-%25C4%2590%25C6%25A1n-h%25C3%25A0ng?page=1). Trang danh mục phụ thuộc JavaScript và không trả danh sách bài trong công cụ đọc trang. Các bài liên quan được tìm và đọc qua công cụ tìm kiếm, giữ liên kết chính thức đến từng bài. Hai bài phía người bán được bổ sung từ cùng Trung tâm trợ giúp để bộ lọc `audience` có cả `buyer` và `seller`.

Corpus tại `data/shopee-orders/` gồm **7 bản tóm lược tự biên soạn**, mỗi file dựa trên một bài chính thức. Đây là tập nhỏ phục vụ so sánh thuật toán, không phải bản sao đầy đủ của chính sách Shopee. Các tiêu đề trong corpus được biên tập để giữ từng ý; vì vậy kết quả chia theo heading phản ánh cấu trúc bản tóm lược, không chứng minh chất lượng trên toàn bộ trang nguồn gốc.

## Cách thu thập và giới hạn quyền sử dụng

- Ngày đọc/tổng hợp: **20/09/2026**. `retrieved_at` là ngày truy cập kết quả đọc trang/tìm kiếm, không phải ngày Shopee cập nhật chính sách. Công cụ có thể sử dụng chỉ mục hoặc bản trang được lưu trước đó.
- Các nguồn được dùng không hiện ngày hiệu lực/cập nhật trong phần đọc được; do đó `document_version="not-stated"`. Không tự gán số phiên bản hay khẳng định đây là toàn bộ quy định mới nhất.
- Kiểm tra HTTP công khai đối với [robots.txt](https://help.shopee.vn/robots.txt) trả mã 200 và chỉ thị `User-Agent:*`, `Allow: /` trong phiên thực hiện. Cho phép trong robots không đồng nghĩa có giấy phép sao chép.
- [Điều khoản dịch vụ, mục 3.1](https://help.shopee.vn/portal/4/article/77243) có giới hạn thu thập và sao chép nội dung. Vì vậy không chạy crawler để tải/sao chép toàn trang, không dùng scraper mẫu của lab cho các URL này và không lưu HTML, ảnh hoặc toàn văn nguồn.
- Nội dung nộp là các diễn giải ngắn bằng lời riêng của những thông tin cần cho bài thực nghiệm, có URL và phạm vi mục nguồn. `license_or_permission="team-authored-summary-of-public-facts"` mô tả cách tạo bản tóm lược; **không phải giấy phép hay chấp thuận của Shopee**. Không gắn nhãn CC hoặc khẳng định quyền tái bản nguồn gốc.
- Không đăng nhập, không truy cập đơn mua thật, không lưu mã đơn hay thông tin cá nhân của khách hàng, không vượt CAPTCHA và không gọi API riêng của Shopee.

## Kiểm kê nguồn

| File / doc_id | Audience | Bài nguồn chính thức | Nội dung chọn |
|---|---|---|---|
| `buyer-order-status` | buyer | [79472](https://help.shopee.vn/portal/4/article/79472) | Nơi xem trạng thái và tra cứu vận chuyển |
| `buyer-cancel-order` | buyer | [79182](https://help.shopee.vn/portal/4/article/79182) | Điều kiện hủy, ngoại lệ SPX và giới hạn yêu cầu |
| `buyer-cancelled-order` | buyer | [79519](https://help.shopee.vn/portal/4/article/79519) | Đơn đã hủy và nguyên nhân hủy; URL đầy đủ đã đọc lưu trong manifest |
| `buyer-prepayment` | buyer | [79473](https://help.shopee.vn/portal/4/article/79473) | Hạn thẻ tín dụng/ghi nợ và cách tra hạn; URL đầy đủ trong manifest |
| `buyer-track-chat` | buyer | [79600](https://help.shopee.vn/portal/4/article/79600) | Tra cứu bằng mã đơn trong công cụ trò chuyện |
| `seller-cancel-request` | seller | [98754](https://help.shopee.vn/portal/1/article/98754) | Mục B.5, thao tác trên Kênh Quản Lý Shop |
| `seller-failed-delivery` | seller | [102523](https://help.shopee.vn/portal/1/article/102523) | Mục 1–3, nhận hàng hoàn và yêu cầu hỗ trợ |

`sources.csv` khớp một dòng cho mỗi tài liệu. Frontmatter được tách khỏi phần thân trước khi embedding; các trường nguồn, phiên bản, đối tượng và loại nội dung được giữ trong metadata của từng chunk.

## Bộ câu hỏi và cách đọc kết quả

`benchmark_queries.json` cố định đúng 5 câu hỏi và đáp án tham chiếu trước khi chạy benchmark. Tất cả chiến lược dùng cùng corpus, câu hỏi, embedding và top-k. Q5 cố ý không nêu vai trò trong câu hỏi; `metadata_filter={"audience":"seller"}` cung cấp ngữ cảnh vai trò, tránh lẫn hướng dẫn người mua. Q2 cũng có phép đối chiếu với bộ lọc buyer.

Một chunk được đánh dấu đủ bằng chứng khi đúng tài liệu **và chứa các cụm điều kiện/đáp án cần thiết trong cùng chunk**; không chỉ kiểm tra ID tài liệu. Hit@3 này là tiêu chí tự động có tính bảo thủ: câu trả lời có thể ghép bằng chứng từ nhiều chunk, nên vẫn cần đọc câu trả lời agent. Không dùng số liệu retrieval để tự suy ra điểm giảng viên.

Các cấu hình đối chiếu được chạy trên cùng máy. Tên Nguyễn Văn A và Nguyễn Văn B là tên tạm để phân công; kết quả không được trình bày như bằng chứng hai người này đã tự lập trình, chạy bài hay thuyết trình.
