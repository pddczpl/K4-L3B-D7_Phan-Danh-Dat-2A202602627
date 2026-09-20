# Minh chứng benchmark đơn hàng Shopee

Sinh viên: Phan Danh Đạt | MSSV: 2A202602627 | Nhóm 3 người
Thời điểm ghi kết quả: 2026-09-20T03:25:48.259003+00:00
JSON nguồn: shopee_benchmark_gemini_gemini.json
Embedding: gemini / gemini-embedding-001 / 3072 chiều
LLM: gemini / gemini-3.1-flash-lite
Cấu hình: {"fixed_size": {"chunk_size": 350, "overlap": 50}, "heading": {"chunk_size": 500}, "recursive": {"chunk_size": 500}}
Sử dụng API/cache trong lần chạy: {"answer_cache_hits": 4, "embedding_cache_hits": 48, "embedding_requests": 0, "generation_requests": 11}

Heading là chiến lược cá nhân của Phan Danh Đạt. Fixed-size và recursive là các cấu hình
so sánh được chạy trên cùng máy; không phải kết quả do hai thành viên khác tự thực hiện.
answer_bearing=true khi cùng một chunk có đúng doc_id và đủ các cụm bằng chứng yêu cầu.
Hit@3 đo việc tìm thấy ít nhất một chunk như vậy; không tự động chứng minh câu trả lời LLM đúng.
Gold answer và bằng chứng được giữ để người đọc đối chiếu. chunk_index bắt đầu từ 0.

## Chiến lược: heading

Tham số: {"chunk_size": 500}
Số chunks: 15 | Hit@3: 5/5 (100.0%)

### Q1

Câu hỏi gốc: Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua?
Metadata filter: null
Gold answer: Mở mục Tôi > Đơn mua trên ứng dụng Shopee để xem tiến trình đơn hàng.
Bằng chứng yêu cầu: [{"doc_id": "buyer-order-status", "required_phrases": ["Tôi > Đơn mua", "tiến trình"]}]

Top-3 không lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-order-status | chunk_index=0
score=0.7929057036904136 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79472
Metadata: {"audience": "buyer", "category": "order-status", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-order-status", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-order-status.md", "source_section": "Hướng dẫn kiểm tra trạng thái và lưu ý về vận đơn", "source_url": "https://help.shopee.vn/portal/4/article/79472", "strategy": "heading", "title": "Xem trạng thái đơn mua Shopee"}
Nội dung chunk đầy đủ:
    # Xem trạng thái đơn mua
    ## Nơi xem và ý nghĩa
    
    Trên ứng dụng, mở Tôi > Đơn mua để xem tiến trình. Chờ xác nhận nghĩa là hệ thống đang kiểm tra đơn; Chờ lấy hàng nghĩa là thông tin đã đến người bán để chuẩn bị bàn giao. Đang giao cho biết kiện đang tới người nhận; Đã giao nghĩa là giao thành công. Các mục khác phản ánh việc đánh giá sản phẩm, hủy đơn hoặc trả hàng.

Rank 2 | doc_id=buyer-track-chat | chunk_index=0
score=0.7687925528220172 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79600
Metadata: {"audience": "buyer", "category": "order-tracking", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-track-chat", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-track-chat.md", "source_section": "Các bước tra cứu bằng mã đơn hàng", "source_url": "https://help.shopee.vn/portal/4/article/79600", "strategy": "heading", "title": "Tra cứu đơn trong phần trò chuyện Shopee"}
Nội dung chunk đầy đủ:
    # Tra cứu bằng công cụ trò chuyện
    ## Dùng mã đơn hàng
    
    Sao chép mã đơn tại trang chi tiết đơn rồi mở phần trò chuyện với Shopee. Dán mã vào ô nhập thông tin để hệ thống trả lại trạng thái tương ứng. Kết quả còn hiển thị các lựa chọn hỗ trợ giao gấp và hủy/hoàn tiền.

Rank 3 | doc_id=buyer-order-status | chunk_index=1
score=0.7569024694214791 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79472
Metadata: {"audience": "buyer", "category": "order-status", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-order-status", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-order-status.md", "source_section": "Hướng dẫn kiểm tra trạng thái và lưu ý về vận đơn", "source_url": "https://help.shopee.vn/portal/4/article/79472", "strategy": "heading", "title": "Xem trạng thái đơn mua Shopee"}
Nội dung chunk đầy đủ:
    # Xem trạng thái đơn mua
    ## Tra cứu vận chuyển
    
    Khi đơn bắt đầu giao, người mua có thể xem hành trình ngay trong ứng dụng. Mã vận đơn cũng dùng để tra cứu tại website của hãng vận chuyển tương ứng; cần phân biệt mã này với mã đơn hàng.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua?

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Để xem trạng thái đơn mua trên ứng dụng Shopee, bạn cần vào mục **Tôi > Đơn mua** [1].

### Q2

Câu hỏi gốc: Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không?
Metadata filter: {"audience": "buyer"}
Gold answer: Không tự động hủy ngay: phải chờ người bán chấp nhận. Nếu người bán từ chối, đơn vẫn tiếp tục giao.
Bằng chứng yêu cầu: [{"doc_id": "buyer-cancel-order", "required_phrases": ["Chờ lấy hàng", "phải đợi người bán chấp nhận", "nếu bị từ chối, đơn vẫn tiếp tục giao"]}]

Top-3 có lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-cancel-order | chunk_index=0
score=0.8247665105709695 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "heading", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    ## Hãng vận chuyển khác SPX
    
    Ở Chờ xác nhận, yêu cầu có thể hủy ngay. Khi Chờ lấy hàng, phải đợi người bán chấp nhận; nếu bị từ chối, đơn vẫn tiếp tục giao. Các trạng thái khác không nhận yêu cầu theo quy tắc này.

Rank 2 | doc_id=buyer-cancel-order | chunk_index=1
score=0.8147024236178098 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "heading", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    ## Ngoại lệ SPX Express
    
    Một số tài khoản được áp dụng hủy ngay trước khi kiện tới trạm giao hàng của SPX. Tài khoản ngoài nhóm áp dụng phải theo quy tắc của các hãng khác; không hiểu đây là quyền áp dụng cho mọi người mua.

Rank 3 | doc_id=buyer-cancelled-order | chunk_index=1
score=0.7170991718097096 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "heading", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    ## Vì sao đơn bị hủy?
    
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa thanh toán kịp hạn đối với đơn trả trước, hoặc hãng vận chuyển không giao được sau nhiều lần thử. Số lần giao tối đa tùy hãng, bài viết không nêu một con số chung. Nếu lý do hiển thị không đúng thực tế, liên hệ chăm sóc khách hàng để được hỗ trợ.

Đối chứng top-3 bỏ filter; hit@3=true

Rank 1 | doc_id=buyer-cancel-order | chunk_index=0
score=0.8247665105709695 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "heading", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    ## Hãng vận chuyển khác SPX
    
    Ở Chờ xác nhận, yêu cầu có thể hủy ngay. Khi Chờ lấy hàng, phải đợi người bán chấp nhận; nếu bị từ chối, đơn vẫn tiếp tục giao. Các trạng thái khác không nhận yêu cầu theo quy tắc này.

Rank 2 | doc_id=buyer-cancel-order | chunk_index=1
score=0.8147024236178098 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "heading", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    ## Ngoại lệ SPX Express
    
    Một số tài khoản được áp dụng hủy ngay trước khi kiện tới trạm giao hàng của SPX. Tài khoản ngoài nhóm áp dụng phải theo quy tắc của các hãng khác; không hiểu đây là quyền áp dụng cho mọi người mua.

Rank 3 | doc_id=buyer-cancelled-order | chunk_index=1
score=0.7170991718097096 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "heading", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    ## Vì sao đơn bị hủy?
    
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa thanh toán kịp hạn đối với đơn trả trước, hoặc hãng vận chuyển không giao được sau nhiều lần thử. Số lần giao tối đa tùy hãng, bài viết không nêu một con số chung. Nếu lý do hiển thị không đúng thực tế, liên hệ chăm sóc khách hàng để được hỗ trợ.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không?
Vai trò của người hỏi: người mua. Phạm vi tài liệu: {"audience": "buyer"}

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Đối với đơn hàng do hãng vận chuyển khác SPX đang ở trạng thái "Chờ lấy hàng", bạn không thể hủy ngay mà phải đợi người bán chấp nhận yêu cầu. Nếu người bán từ chối, đơn hàng sẽ vẫn tiếp tục được giao [1].

### Q3

Câu hỏi gốc: Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không?
Metadata filter: null
Gold answer: Không khôi phục đơn đã hủy để giao lại. Cần đặt đơn mới; có thể trao đổi giá với shop, không mặc định giữ được ưu đãi cũ.
Bằng chứng yêu cầu: [{"doc_id": "buyer-cancelled-order", "required_phrases": ["không thể khôi phục", "đặt đơn mới", "thay vì mặc định giữ được ưu đãi cũ"]}]

Top-3 không lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-cancelled-order | chunk_index=0
score=0.8118810555886322 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "heading", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    ## Có khôi phục để giao lại không?
    
    Đơn mang trạng thái Đã hủy không thể khôi phục để giao lại. Muốn mua tiếp, khách cần đặt đơn mới; có thể trao đổi với shop về mức giá trước khi đặt lại, thay vì mặc định giữ được ưu đãi cũ.

Rank 2 | doc_id=buyer-cancelled-order | chunk_index=1
score=0.7390347549380963 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "heading", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    ## Vì sao đơn bị hủy?
    
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa thanh toán kịp hạn đối với đơn trả trước, hoặc hãng vận chuyển không giao được sau nhiều lần thử. Số lần giao tối đa tùy hãng, bài viết không nêu một con số chung. Nếu lý do hiển thị không đúng thực tế, liên hệ chăm sóc khách hàng để được hỗ trợ.

Rank 3 | doc_id=seller-cancel-request | chunk_index=0
score=0.7136861936759996 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "heading", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    # Phản hồi yêu cầu hủy trong Kênh Quản Lý Shop
    ## Xử lý yêu cầu của người mua
    
    Người bán mở Đơn hủy > Chờ phản hồi > Xem thêm để quyết định đồng ý hoặc từ chối. Đồng ý làm đơn chuyển sang Đã hủy; từ chối đưa đơn về Đã đóng gói trong nhóm Chờ lấy hàng. Đây là thao tác phía người bán trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua hàng.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không?

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Đơn hàng đã ở trạng thái Đã hủy không thể khôi phục để giao lại [1]. Nếu muốn mua tiếp, khách hàng cần đặt đơn mới và không mặc định giữ được ưu đãi cũ (có thể trao đổi với shop về mức giá trước khi đặt lại) [1].

### Q4

Câu hỏi gốc: Đơn trả trước bằng thẻ tín dụng hoặc ghi nợ cần thanh toán trong bao lâu, nếu quá hạn thì sao?
Metadata filter: null
Gold answer: Hoàn tất trong 12 giờ kể từ lúc đặt hàng thành công; quá hạn không thanh toán thì hệ thống tự động hủy đơn.
Bằng chứng yêu cầu: [{"doc_id": "buyer-prepayment", "required_phrases": ["12 giờ", "kể từ khi đặt hàng thành công", "tự động hủy"]}]

Top-3 không lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-prepayment | chunk_index=0
score=0.8186722653822052 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u
Metadata: {"audience": "buyer", "category": "payment-deadline", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-prepayment", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-prepayment.md", "source_section": "Dòng thẻ tín dụng/ghi nợ trong bảng và phần tra cứu hạn", "source_url": "https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u", "strategy": "heading", "title": "Hạn thanh toán đơn trả trước"}
Nội dung chunk đầy đủ:
    # Thanh toán cho đơn trả trước
    ## Thanh toán bằng thẻ
    
    Với thẻ tín dụng hoặc ghi nợ, thời hạn hoàn tất thanh toán là 12 giờ kể từ khi đặt hàng thành công. Nếu không thanh toán trong hạn quy định, hệ thống tự động hủy đơn; đơn chưa thanh toán được xem là chưa hoàn tất. Mốc này không dùng chung cho mọi phương thức thanh toán.

Rank 2 | doc_id=buyer-prepayment | chunk_index=1
score=0.7534433371156877 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u
Metadata: {"audience": "buyer", "category": "payment-deadline", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-prepayment", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-prepayment.md", "source_section": "Dòng thẻ tín dụng/ghi nợ trong bảng và phần tra cứu hạn", "source_url": "https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u", "strategy": "heading", "title": "Hạn thanh toán đơn trả trước"}
Nội dung chunk đầy đủ:
    # Thanh toán cho đơn trả trước
    ## Kiểm tra hạn của đơn cụ thể
    
    Xem hạn trên màn hình báo đặt hàng thành công. Cũng có thể mở Tôi, chọn Chờ xác nhận trong Đơn mua, mở đơn cần xem rồi tìm phần Chờ thanh toán. Dùng hạn hiển thị của chính đơn đó khi kiểm tra.

Rank 3 | doc_id=buyer-cancelled-order | chunk_index=1
score=0.6447610851760971 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "heading", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    ## Vì sao đơn bị hủy?
    
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa thanh toán kịp hạn đối với đơn trả trước, hoặc hãng vận chuyển không giao được sau nhiều lần thử. Số lần giao tối đa tùy hãng, bài viết không nêu một con số chung. Nếu lý do hiển thị không đúng thực tế, liên hệ chăm sóc khách hàng để được hỗ trợ.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Đơn trả trước bằng thẻ tín dụng hoặc ghi nợ cần thanh toán trong bao lâu, nếu quá hạn thì sao?

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Đối với đơn hàng trả trước bằng thẻ tín dụng hoặc ghi nợ, thời hạn hoàn tất thanh toán là 12 giờ kể từ khi đặt hàng thành công [1]. Nếu không thanh toán trong thời hạn quy định, hệ thống sẽ tự động hủy đơn hàng [1].

### Q5

Câu hỏi gốc: Tôi xử lý yêu cầu hủy đơn hàng như thế nào?
Metadata filter: {"audience": "seller"}
Gold answer: Với vai trò người bán trên Kênh Quản Lý Shop: vào Đơn hủy > Chờ phản hồi > Xem thêm, đồng ý hoặc từ chối. Đồng ý chuyển sang Đã hủy; từ chối về Đã đóng gói trong Chờ lấy hàng.
Bằng chứng yêu cầu: [{"doc_id": "seller-cancel-request", "required_phrases": ["Đơn hủy > Chờ phản hồi > Xem thêm", "Đồng ý làm đơn chuyển sang Đã hủy", "từ chối đưa đơn về Đã đóng gói"]}]

Top-3 có lọc metadata; hit@3=true

Rank 1 | doc_id=seller-cancel-request | chunk_index=0
score=0.7706995665317576 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "heading", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    # Phản hồi yêu cầu hủy trong Kênh Quản Lý Shop
    ## Xử lý yêu cầu của người mua
    
    Người bán mở Đơn hủy > Chờ phản hồi > Xem thêm để quyết định đồng ý hoặc từ chối. Đồng ý làm đơn chuyển sang Đã hủy; từ chối đưa đơn về Đã đóng gói trong nhóm Chờ lấy hàng. Đây là thao tác phía người bán trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua hàng.

Rank 2 | doc_id=seller-cancel-request | chunk_index=1
score=0.7238944031526252 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "heading", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    # Phản hồi yêu cầu hủy trong Kênh Quản Lý Shop
    ## Các nguyên nhân hủy
    
    Tài liệu liệt kê trường hợp người bán xác nhận trễ, bàn giao cho hãng vận chuyển trễ sau khi xác nhận, hoặc người mua hủy. Bài viết không nêu số ngày chung cho các thời hạn này, vì vậy không suy ra mốc ngày cụ thể từ bản hướng dẫn này.

Rank 3 | doc_id=seller-failed-delivery | chunk_index=1
score=0.677785229582525 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/1/article/102523
Metadata: {"audience": "seller", "category": "failed-delivery", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "seller-failed-delivery", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-failed-delivery.md", "source_section": "Mục 1–3 về theo dõi, nhập kho và yêu cầu hỗ trợ", "source_url": "https://help.shopee.vn/portal/1/article/102523", "strategy": "heading", "title": "Theo dõi kiện giao thất bại và hàng hoàn"}
Nội dung chunk đầy đủ:
    # Xử lý kiện giao không thành công
    ## Hàng hỏng hoặc trạng thái không khớp
    
    Nếu hàng hoàn hư hỏng, cần sớm liên hệ chăm sóc khách hàng để hỗ trợ khiếu nại. Quay video khi mở kiện hoàn giúp lưu bằng chứng sự cố. Khi trạng thái hệ thống khác thực tế, có thể xuất danh sách đơn thành Excel để đối chiếu và gửi yêu cầu hỗ trợ. Hướng dẫn này không quy định một thời hạn khiếu nại tính bằng số ngày.

Đối chứng top-3 bỏ filter; hit@3=true

Rank 1 | doc_id=seller-cancel-request | chunk_index=0
score=0.7706995665317576 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "heading", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    # Phản hồi yêu cầu hủy trong Kênh Quản Lý Shop
    ## Xử lý yêu cầu của người mua
    
    Người bán mở Đơn hủy > Chờ phản hồi > Xem thêm để quyết định đồng ý hoặc từ chối. Đồng ý làm đơn chuyển sang Đã hủy; từ chối đưa đơn về Đã đóng gói trong nhóm Chờ lấy hàng. Đây là thao tác phía người bán trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua hàng.

Rank 2 | doc_id=buyer-cancel-order | chunk_index=2
score=0.7568481109421223 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 2, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "heading", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    ## Thao tác và giới hạn
    
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước được hoàn theo phương thức thanh toán và chính sách tương ứng khi hủy thành công.

Rank 3 | doc_id=buyer-cancel-order | chunk_index=0
score=0.7349534580552289 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "heading", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    ## Hãng vận chuyển khác SPX
    
    Ở Chờ xác nhận, yêu cầu có thể hủy ngay. Khi Chờ lấy hàng, phải đợi người bán chấp nhận; nếu bị từ chối, đơn vẫn tiếp tục giao. Các trạng thái khác không nhận yêu cầu theo quy tắc này.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Tôi xử lý yêu cầu hủy đơn hàng như thế nào?
Vai trò của người hỏi: người bán. Phạm vi tài liệu: {"audience": "seller"}

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Để xử lý yêu cầu hủy đơn hàng trên Kênh Quản Lý Shop, người bán thực hiện các bước sau:

1. Truy cập vào mục Đơn hủy [1].
2. Chọn "Chờ phản hồi" [1].
3. Chọn "Xem thêm" để quyết định đồng ý hoặc từ chối yêu cầu [1]:
   - Nếu bạn chọn **Đồng ý**: Đơn hàng sẽ chuyển sang trạng thái Đã hủy [1].
   - Nếu bạn chọn **Từ chối**: Đơn hàng sẽ được đưa về trạng thái Đã đóng gói trong nhóm Chờ lấy hàng [1].

Lưu ý: Đây là thao tác thực hiện trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua hàng [1].

## Chiến lược: fixed_size

Tham số: {"chunk_size": 350, "overlap": 50}
Số chunks: 15 | Hit@3: 5/5 (100.0%)

### Q1

Câu hỏi gốc: Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua?
Metadata filter: null
Gold answer: Mở mục Tôi > Đơn mua trên ứng dụng Shopee để xem tiến trình đơn hàng.
Bằng chứng yêu cầu: [{"doc_id": "buyer-order-status", "required_phrases": ["Tôi > Đơn mua", "tiến trình"]}]

Top-3 không lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-order-status | chunk_index=0
score=0.7874992400085488 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79472
Metadata: {"audience": "buyer", "category": "order-status", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-order-status", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-order-status.md", "source_section": "Hướng dẫn kiểm tra trạng thái và lưu ý về vận đơn", "source_url": "https://help.shopee.vn/portal/4/article/79472", "strategy": "fixed_size", "title": "Xem trạng thái đơn mua Shopee"}
Nội dung chunk đầy đủ:
    # Xem trạng thái đơn mua
    
    ## Nơi xem và ý nghĩa
    Trên ứng dụng, mở Tôi > Đơn mua để xem tiến trình. Chờ xác nhận nghĩa là hệ thống đang kiểm tra đơn; Chờ lấy hàng nghĩa là thông tin đã đến người bán để chuẩn bị bàn giao. Đang giao cho biết kiện đang tới người nhận; Đã giao nghĩa là giao thành công. Các mục khác phản ánh việc đánh giá sản phẩm, hủy đ

Rank 2 | doc_id=buyer-track-chat | chunk_index=0
score=0.7772088256541808 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79600
Metadata: {"audience": "buyer", "category": "order-tracking", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-track-chat", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-track-chat.md", "source_section": "Các bước tra cứu bằng mã đơn hàng", "source_url": "https://help.shopee.vn/portal/4/article/79600", "strategy": "fixed_size", "title": "Tra cứu đơn trong phần trò chuyện Shopee"}
Nội dung chunk đầy đủ:
    # Tra cứu bằng công cụ trò chuyện
    
    ## Dùng mã đơn hàng
    Sao chép mã đơn tại trang chi tiết đơn rồi mở phần trò chuyện với Shopee. Dán mã vào ô nhập thông tin để hệ thống trả lại trạng thái tương ứng. Kết quả còn hiển thị các lựa chọn hỗ trợ giao gấp và hủy/hoàn tiền.
    
    ## Xem đơn khác
    Trong giao diện trò chuyện, mục Những đơn khác cho phép chọn các đ

Rank 3 | doc_id=buyer-order-status | chunk_index=1
score=0.7670998776353547 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79472
Metadata: {"audience": "buyer", "category": "order-status", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-order-status", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-order-status.md", "source_section": "Hướng dẫn kiểm tra trạng thái và lưu ý về vận đơn", "source_url": "https://help.shopee.vn/portal/4/article/79472", "strategy": "fixed_size", "title": "Xem trạng thái đơn mua Shopee"}
Nội dung chunk đầy đủ:
    ác mục khác phản ánh việc đánh giá sản phẩm, hủy đơn hoặc trả hàng.
    
    ## Tra cứu vận chuyển
    Khi đơn bắt đầu giao, người mua có thể xem hành trình ngay trong ứng dụng. Mã vận đơn cũng dùng để tra cứu tại website của hãng vận chuyển tương ứng; cần phân biệt mã này với mã đơn hàng.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua?

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Để xem trạng thái đơn mua trên ứng dụng Shopee, bạn cần mở mục **Tôi** > **Đơn mua** [1].

### Q2

Câu hỏi gốc: Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không?
Metadata filter: {"audience": "buyer"}
Gold answer: Không tự động hủy ngay: phải chờ người bán chấp nhận. Nếu người bán từ chối, đơn vẫn tiếp tục giao.
Bằng chứng yêu cầu: [{"doc_id": "buyer-cancel-order", "required_phrases": ["Chờ lấy hàng", "phải đợi người bán chấp nhận", "nếu bị từ chối, đơn vẫn tiếp tục giao"]}]

Top-3 có lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-cancel-order | chunk_index=1
score=0.8500795037481681 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "fixed_size", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
     ngay trước khi kiện tới trạm giao hàng của SPX. Tài khoản ngoài nhóm áp dụng phải theo quy tắc của các hãng khác; không hiểu đây là quyền áp dụng cho mọi người mua.
    
    ## Thao tác và giới hạn
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước

Rank 2 | doc_id=buyer-cancel-order | chunk_index=0
score=0.8295895924188273 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "fixed_size", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    
    ## Hãng vận chuyển khác SPX
    Ở Chờ xác nhận, yêu cầu có thể hủy ngay. Khi Chờ lấy hàng, phải đợi người bán chấp nhận; nếu bị từ chối, đơn vẫn tiếp tục giao. Các trạng thái khác không nhận yêu cầu theo quy tắc này.
    
    ## Ngoại lệ SPX Express
    Một số tài khoản được áp dụng hủy ngay trước khi kiện tới trạm giao hàng của SPX. T

Rank 3 | doc_id=buyer-cancelled-order | chunk_index=0
score=0.7286149496074483 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "fixed_size", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    
    ## Có khôi phục để giao lại không?
    Đơn mang trạng thái Đã hủy không thể khôi phục để giao lại. Muốn mua tiếp, khách cần đặt đơn mới; có thể trao đổi với shop về mức giá trước khi đặt lại, thay vì mặc định giữ được ưu đãi cũ.
    
    ## Vì sao đơn bị hủy?
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa tha

Đối chứng top-3 bỏ filter; hit@3=true

Rank 1 | doc_id=buyer-cancel-order | chunk_index=1
score=0.8500795037481681 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "fixed_size", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
     ngay trước khi kiện tới trạm giao hàng của SPX. Tài khoản ngoài nhóm áp dụng phải theo quy tắc của các hãng khác; không hiểu đây là quyền áp dụng cho mọi người mua.
    
    ## Thao tác và giới hạn
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước

Rank 2 | doc_id=buyer-cancel-order | chunk_index=0
score=0.8295895924188273 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "fixed_size", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    
    ## Hãng vận chuyển khác SPX
    Ở Chờ xác nhận, yêu cầu có thể hủy ngay. Khi Chờ lấy hàng, phải đợi người bán chấp nhận; nếu bị từ chối, đơn vẫn tiếp tục giao. Các trạng thái khác không nhận yêu cầu theo quy tắc này.
    
    ## Ngoại lệ SPX Express
    Một số tài khoản được áp dụng hủy ngay trước khi kiện tới trạm giao hàng của SPX. T

Rank 3 | doc_id=buyer-cancelled-order | chunk_index=0
score=0.7286149496074483 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "fixed_size", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    
    ## Có khôi phục để giao lại không?
    Đơn mang trạng thái Đã hủy không thể khôi phục để giao lại. Muốn mua tiếp, khách cần đặt đơn mới; có thể trao đổi với shop về mức giá trước khi đặt lại, thay vì mặc định giữ được ưu đãi cũ.
    
    ## Vì sao đơn bị hủy?
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa tha

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không?
Vai trò của người hỏi: người mua. Phạm vi tài liệu: {"audience": "buyer"}

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Đối với đơn hàng do hãng vận chuyển khác SPX, khi đơn đang ở trạng thái Chờ lấy hàng, bạn không thể hủy ngay mà phải đợi người bán chấp nhận yêu cầu. Nếu người bán từ chối, đơn hàng sẽ vẫn tiếp tục được giao [2].

### Q3

Câu hỏi gốc: Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không?
Metadata filter: null
Gold answer: Không khôi phục đơn đã hủy để giao lại. Cần đặt đơn mới; có thể trao đổi giá với shop, không mặc định giữ được ưu đãi cũ.
Bằng chứng yêu cầu: [{"doc_id": "buyer-cancelled-order", "required_phrases": ["không thể khôi phục", "đặt đơn mới", "thay vì mặc định giữ được ưu đãi cũ"]}]

Top-3 không lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-cancelled-order | chunk_index=0
score=0.8003309949064328 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "fixed_size", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    
    ## Có khôi phục để giao lại không?
    Đơn mang trạng thái Đã hủy không thể khôi phục để giao lại. Muốn mua tiếp, khách cần đặt đơn mới; có thể trao đổi với shop về mức giá trước khi đặt lại, thay vì mặc định giữ được ưu đãi cũ.
    
    ## Vì sao đơn bị hủy?
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa tha

Rank 2 | doc_id=buyer-cancel-order | chunk_index=1
score=0.7386908874861094 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "fixed_size", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
     ngay trước khi kiện tới trạm giao hàng của SPX. Tài khoản ngoài nhóm áp dụng phải theo quy tắc của các hãng khác; không hiểu đây là quyền áp dụng cho mọi người mua.
    
    ## Thao tác và giới hạn
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước

Rank 3 | doc_id=seller-cancel-request | chunk_index=0
score=0.7164566574771827 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "fixed_size", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    # Phản hồi yêu cầu hủy trong Kênh Quản Lý Shop
    
    ## Xử lý yêu cầu của người mua
    Người bán mở Đơn hủy > Chờ phản hồi > Xem thêm để quyết định đồng ý hoặc từ chối. Đồng ý làm đơn chuyển sang Đã hủy; từ chối đưa đơn về Đã đóng gói trong nhóm Chờ lấy hàng. Đây là thao tác phía người bán trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua 

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không?

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Đơn hàng Shopee đã ở trạng thái Đã hủy thì không thể khôi phục để giao lại [1]. Nếu muốn mua tiếp, khách hàng cần đặt đơn mới [1]. Ngoài ra, khách hàng không mặc định giữ được ưu đãi cũ mà có thể trao đổi với shop về mức giá trước khi đặt lại [1].

### Q4

Câu hỏi gốc: Đơn trả trước bằng thẻ tín dụng hoặc ghi nợ cần thanh toán trong bao lâu, nếu quá hạn thì sao?
Metadata filter: null
Gold answer: Hoàn tất trong 12 giờ kể từ lúc đặt hàng thành công; quá hạn không thanh toán thì hệ thống tự động hủy đơn.
Bằng chứng yêu cầu: [{"doc_id": "buyer-prepayment", "required_phrases": ["12 giờ", "kể từ khi đặt hàng thành công", "tự động hủy"]}]

Top-3 không lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-prepayment | chunk_index=0
score=0.8055637058371284 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u
Metadata: {"audience": "buyer", "category": "payment-deadline", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-prepayment", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-prepayment.md", "source_section": "Dòng thẻ tín dụng/ghi nợ trong bảng và phần tra cứu hạn", "source_url": "https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u", "strategy": "fixed_size", "title": "Hạn thanh toán đơn trả trước"}
Nội dung chunk đầy đủ:
    # Thanh toán cho đơn trả trước
    
    ## Thanh toán bằng thẻ
    Với thẻ tín dụng hoặc ghi nợ, thời hạn hoàn tất thanh toán là 12 giờ kể từ khi đặt hàng thành công. Nếu không thanh toán trong hạn quy định, hệ thống tự động hủy đơn; đơn chưa thanh toán được xem là chưa hoàn tất. Mốc này không dùng chung cho mọi phương thức thanh toán.
    
    ## Kiểm tra hạn của đơn

Rank 2 | doc_id=buyer-prepayment | chunk_index=1
score=0.7176499385559189 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u
Metadata: {"audience": "buyer", "category": "payment-deadline", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-prepayment", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-prepayment.md", "source_section": "Dòng thẻ tín dụng/ghi nợ trong bảng và phần tra cứu hạn", "source_url": "https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u", "strategy": "fixed_size", "title": "Hạn thanh toán đơn trả trước"}
Nội dung chunk đầy đủ:
    i phương thức thanh toán.
    
    ## Kiểm tra hạn của đơn cụ thể
    Xem hạn trên màn hình báo đặt hàng thành công. Cũng có thể mở Tôi, chọn Chờ xác nhận trong Đơn mua, mở đơn cần xem rồi tìm phần Chờ thanh toán. Dùng hạn hiển thị của chính đơn đó khi kiểm tra.

Rank 3 | doc_id=buyer-cancel-order | chunk_index=2
score=0.6976666605718709 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 2, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "fixed_size", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
     khi bị từ chối không gửi lại được. Tiền trả trước được hoàn theo phương thức thanh toán và chính sách tương ứng khi hủy thành công.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Đơn trả trước bằng thẻ tín dụng hoặc ghi nợ cần thanh toán trong bao lâu, nếu quá hạn thì sao?

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Đối với đơn hàng trả trước bằng thẻ tín dụng hoặc ghi nợ, thời hạn hoàn tất thanh toán là 12 giờ kể từ khi đặt hàng thành công [1]. Nếu không thanh toán trong thời hạn quy định, hệ thống sẽ tự động hủy đơn hàng [1].

### Q5

Câu hỏi gốc: Tôi xử lý yêu cầu hủy đơn hàng như thế nào?
Metadata filter: {"audience": "seller"}
Gold answer: Với vai trò người bán trên Kênh Quản Lý Shop: vào Đơn hủy > Chờ phản hồi > Xem thêm, đồng ý hoặc từ chối. Đồng ý chuyển sang Đã hủy; từ chối về Đã đóng gói trong Chờ lấy hàng.
Bằng chứng yêu cầu: [{"doc_id": "seller-cancel-request", "required_phrases": ["Đơn hủy > Chờ phản hồi > Xem thêm", "Đồng ý làm đơn chuyển sang Đã hủy", "từ chối đưa đơn về Đã đóng gói"]}]

Top-3 có lọc metadata; hit@3=true

Rank 1 | doc_id=seller-cancel-request | chunk_index=0
score=0.772160879660285 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "fixed_size", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    # Phản hồi yêu cầu hủy trong Kênh Quản Lý Shop
    
    ## Xử lý yêu cầu của người mua
    Người bán mở Đơn hủy > Chờ phản hồi > Xem thêm để quyết định đồng ý hoặc từ chối. Đồng ý làm đơn chuyển sang Đã hủy; từ chối đưa đơn về Đã đóng gói trong nhóm Chờ lấy hàng. Đây là thao tác phía người bán trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua 

Rank 2 | doc_id=seller-cancel-request | chunk_index=1
score=0.7216234190031878 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "fixed_size", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
     Shop, không phải thao tác hủy trong ứng dụng mua hàng.
    
    ## Các nguyên nhân hủy
    Tài liệu liệt kê trường hợp người bán xác nhận trễ, bàn giao cho hãng vận chuyển trễ sau khi xác nhận, hoặc người mua hủy. Bài viết không nêu số ngày chung cho các thời hạn này, vì vậy không suy ra mốc ngày cụ thể từ bản hướng dẫn này.

Rank 3 | doc_id=seller-failed-delivery | chunk_index=0
score=0.6768247620348151 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/1/article/102523
Metadata: {"audience": "seller", "category": "failed-delivery", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "seller-failed-delivery", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-failed-delivery.md", "source_section": "Mục 1–3 về theo dõi, nhập kho và yêu cầu hỗ trợ", "source_url": "https://help.shopee.vn/portal/1/article/102523", "strategy": "fixed_size", "title": "Theo dõi kiện giao thất bại và hàng hoàn"}
Nội dung chunk đầy đủ:
    # Xử lý kiện giao không thành công
    
    ## Theo dõi và nhận lại
    Hệ thống ghi nhận tự động các đơn Shopee giao thất bại. Người bán theo dõi tiến trình hoàn hàng tại mục Giao không thành công. Khi kiện về đủ và nguyên vẹn, thực hiện nhập lại kho rồi xác nhận.
    
    ## Hàng hỏng hoặc trạng thái không khớp
    Nếu hàng hoàn hư hỏng, cần sớm liên hệ chăm sóc khách h

Đối chứng top-3 bỏ filter; hit@3=true

Rank 1 | doc_id=seller-cancel-request | chunk_index=0
score=0.772160879660285 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "fixed_size", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    # Phản hồi yêu cầu hủy trong Kênh Quản Lý Shop
    
    ## Xử lý yêu cầu của người mua
    Người bán mở Đơn hủy > Chờ phản hồi > Xem thêm để quyết định đồng ý hoặc từ chối. Đồng ý làm đơn chuyển sang Đã hủy; từ chối đưa đơn về Đã đóng gói trong nhóm Chờ lấy hàng. Đây là thao tác phía người bán trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua 

Rank 2 | doc_id=buyer-cancel-order | chunk_index=1
score=0.7500276844223659 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "fixed_size", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
     ngay trước khi kiện tới trạm giao hàng của SPX. Tài khoản ngoài nhóm áp dụng phải theo quy tắc của các hãng khác; không hiểu đây là quyền áp dụng cho mọi người mua.
    
    ## Thao tác và giới hạn
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước

Rank 3 | doc_id=buyer-cancel-order | chunk_index=0
score=0.7491865681577554 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "fixed_size", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    
    ## Hãng vận chuyển khác SPX
    Ở Chờ xác nhận, yêu cầu có thể hủy ngay. Khi Chờ lấy hàng, phải đợi người bán chấp nhận; nếu bị từ chối, đơn vẫn tiếp tục giao. Các trạng thái khác không nhận yêu cầu theo quy tắc này.
    
    ## Ngoại lệ SPX Express
    Một số tài khoản được áp dụng hủy ngay trước khi kiện tới trạm giao hàng của SPX. T

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Tôi xử lý yêu cầu hủy đơn hàng như thế nào?
Vai trò của người hỏi: người bán. Phạm vi tài liệu: {"audience": "seller"}

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Để xử lý yêu cầu hủy đơn hàng trên Kênh Người Bán, bạn thực hiện các bước sau:

1. Truy cập vào mục **Đơn hủy** trên Kênh Quản Lý Shop [1].
2. Tại đây, bạn chọn **Chờ phản hồi** và nhấn **Xem thêm** để đưa ra quyết định [1]:
   - Nếu bạn **Đồng ý**: Đơn hàng sẽ chuyển sang trạng thái Đã hủy [1].
   - Nếu bạn **Từ chối**: Đơn hàng sẽ được đưa về trạng thái Đã đóng gói trong nhóm Chờ lấy hàng [1].

Lưu ý: Đây là thao tác thực hiện trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua hàng [1].

## Chiến lược: recursive

Tham số: {"chunk_size": 500}
Số chunks: 13 | Hit@3: 5/5 (100.0%)

### Q1

Câu hỏi gốc: Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua?
Metadata filter: null
Gold answer: Mở mục Tôi > Đơn mua trên ứng dụng Shopee để xem tiến trình đơn hàng.
Bằng chứng yêu cầu: [{"doc_id": "buyer-order-status", "required_phrases": ["Tôi > Đơn mua", "tiến trình"]}]

Top-3 không lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-order-status | chunk_index=0
score=0.7894605320699383 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79472
Metadata: {"audience": "buyer", "category": "order-status", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-order-status", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-order-status.md", "source_section": "Hướng dẫn kiểm tra trạng thái và lưu ý về vận đơn", "source_url": "https://help.shopee.vn/portal/4/article/79472", "strategy": "recursive", "title": "Xem trạng thái đơn mua Shopee"}
Nội dung chunk đầy đủ:
    # Xem trạng thái đơn mua
    
    ## Nơi xem và ý nghĩa
    Trên ứng dụng, mở Tôi > Đơn mua để xem tiến trình. Chờ xác nhận nghĩa là hệ thống đang kiểm tra đơn; Chờ lấy hàng nghĩa là thông tin đã đến người bán để chuẩn bị bàn giao. Đang giao cho biết kiện đang tới người nhận; Đã giao nghĩa là giao thành công. Các mục khác phản ánh việc đánh giá sản phẩm, hủy đơn hoặc trả hàng.
    

Rank 2 | doc_id=buyer-track-chat | chunk_index=0
score=0.7787719278453015 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79600
Metadata: {"audience": "buyer", "category": "order-tracking", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-track-chat", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-track-chat.md", "source_section": "Các bước tra cứu bằng mã đơn hàng", "source_url": "https://help.shopee.vn/portal/4/article/79600", "strategy": "recursive", "title": "Tra cứu đơn trong phần trò chuyện Shopee"}
Nội dung chunk đầy đủ:
    # Tra cứu bằng công cụ trò chuyện
    
    ## Dùng mã đơn hàng
    Sao chép mã đơn tại trang chi tiết đơn rồi mở phần trò chuyện với Shopee. Dán mã vào ô nhập thông tin để hệ thống trả lại trạng thái tương ứng. Kết quả còn hiển thị các lựa chọn hỗ trợ giao gấp và hủy/hoàn tiền.
    
    ## Xem đơn khác
    Trong giao diện trò chuyện, mục Những đơn khác cho phép chọn các đơn đang giao để xem tình trạng. Hướng dẫn này tra cứu bằng mã đơn hàng đã sao chép từ trang chi tiết đơn.

Rank 3 | doc_id=buyer-order-status | chunk_index=1
score=0.7186276694752539 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79472
Metadata: {"audience": "buyer", "category": "order-status", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-order-status", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-order-status.md", "source_section": "Hướng dẫn kiểm tra trạng thái và lưu ý về vận đơn", "source_url": "https://help.shopee.vn/portal/4/article/79472", "strategy": "recursive", "title": "Xem trạng thái đơn mua Shopee"}
Nội dung chunk đầy đủ:
    ## Tra cứu vận chuyển
    Khi đơn bắt đầu giao, người mua có thể xem hành trình ngay trong ứng dụng. Mã vận đơn cũng dùng để tra cứu tại website của hãng vận chuyển tương ứng; cần phân biệt mã này với mã đơn hàng.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua?

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Để xem trạng thái đơn mua trên ứng dụng Shopee, bạn cần mở mục **Tôi** > **Đơn mua** [1].

### Q2

Câu hỏi gốc: Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không?
Metadata filter: {"audience": "buyer"}
Gold answer: Không tự động hủy ngay: phải chờ người bán chấp nhận. Nếu người bán từ chối, đơn vẫn tiếp tục giao.
Bằng chứng yêu cầu: [{"doc_id": "buyer-cancel-order", "required_phrases": ["Chờ lấy hàng", "phải đợi người bán chấp nhận", "nếu bị từ chối, đơn vẫn tiếp tục giao"]}]

Top-3 có lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-cancel-order | chunk_index=0
score=0.8352375699285338 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "recursive", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    
    ## Hãng vận chuyển khác SPX
    Ở Chờ xác nhận, yêu cầu có thể hủy ngay. Khi Chờ lấy hàng, phải đợi người bán chấp nhận; nếu bị từ chối, đơn vẫn tiếp tục giao. Các trạng thái khác không nhận yêu cầu theo quy tắc này.
    
    ## Ngoại lệ SPX Express
    Một số tài khoản được áp dụng hủy ngay trước khi kiện tới trạm giao hàng của SPX. Tài khoản ngoài nhóm áp dụng phải theo quy tắc của các hãng khác; không hiểu đây là quyền áp dụng cho mọi người mua.
    

Rank 2 | doc_id=buyer-cancel-order | chunk_index=1
score=0.7247226123593289 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "recursive", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    ## Thao tác và giới hạn
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước được hoàn theo phương thức thanh toán và chính sách tương ứng khi hủy thành công.

Rank 3 | doc_id=buyer-cancelled-order | chunk_index=1
score=0.7208571033105283 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "recursive", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    ## Vì sao đơn bị hủy?
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa thanh toán kịp hạn đối với đơn trả trước, hoặc hãng vận chuyển không giao được sau nhiều lần thử. Số lần giao tối đa tùy hãng, bài viết không nêu một con số chung. Nếu lý do hiển thị không đúng thực tế, liên hệ chăm sóc khách hàng để được hỗ trợ.

Đối chứng top-3 bỏ filter; hit@3=true

Rank 1 | doc_id=buyer-cancel-order | chunk_index=0
score=0.8352375699285338 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "recursive", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    # Người mua yêu cầu hủy đơn
    
    ## Hãng vận chuyển khác SPX
    Ở Chờ xác nhận, yêu cầu có thể hủy ngay. Khi Chờ lấy hàng, phải đợi người bán chấp nhận; nếu bị từ chối, đơn vẫn tiếp tục giao. Các trạng thái khác không nhận yêu cầu theo quy tắc này.
    
    ## Ngoại lệ SPX Express
    Một số tài khoản được áp dụng hủy ngay trước khi kiện tới trạm giao hàng của SPX. Tài khoản ngoài nhóm áp dụng phải theo quy tắc của các hãng khác; không hiểu đây là quyền áp dụng cho mọi người mua.
    

Rank 2 | doc_id=buyer-cancel-order | chunk_index=1
score=0.7247226123593289 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "recursive", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    ## Thao tác và giới hạn
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước được hoàn theo phương thức thanh toán và chính sách tương ứng khi hủy thành công.

Rank 3 | doc_id=buyer-cancelled-order | chunk_index=1
score=0.7208571033105283 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "recursive", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    ## Vì sao đơn bị hủy?
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa thanh toán kịp hạn đối với đơn trả trước, hoặc hãng vận chuyển không giao được sau nhiều lần thử. Số lần giao tối đa tùy hãng, bài viết không nêu một con số chung. Nếu lý do hiển thị không đúng thực tế, liên hệ chăm sóc khách hàng để được hỗ trợ.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không?
Vai trò của người hỏi: người mua. Phạm vi tài liệu: {"audience": "buyer"}

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Đối với đơn hàng do hãng vận chuyển khác SPX đang ở trạng thái "Chờ lấy hàng", bạn không thể hủy ngay mà phải đợi người bán chấp nhận yêu cầu hủy. Nếu người bán từ chối, đơn hàng sẽ vẫn tiếp tục được giao [1].

### Q3

Câu hỏi gốc: Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không?
Metadata filter: null
Gold answer: Không khôi phục đơn đã hủy để giao lại. Cần đặt đơn mới; có thể trao đổi giá với shop, không mặc định giữ được ưu đãi cũ.
Bằng chứng yêu cầu: [{"doc_id": "buyer-cancelled-order", "required_phrases": ["không thể khôi phục", "đặt đơn mới", "thay vì mặc định giữ được ưu đãi cũ"]}]

Top-3 không lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-cancelled-order | chunk_index=0
score=0.8146507993930208 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "recursive", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    
    ## Có khôi phục để giao lại không?
    Đơn mang trạng thái Đã hủy không thể khôi phục để giao lại. Muốn mua tiếp, khách cần đặt đơn mới; có thể trao đổi với shop về mức giá trước khi đặt lại, thay vì mặc định giữ được ưu đãi cũ.
    

Rank 2 | doc_id=buyer-cancelled-order | chunk_index=1
score=0.7367034710241377 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "recursive", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    ## Vì sao đơn bị hủy?
    Các khả năng gồm shop không xác nhận hoặc bàn giao đúng hạn, bên mua chưa thanh toán kịp hạn đối với đơn trả trước, hoặc hãng vận chuyển không giao được sau nhiều lần thử. Số lần giao tối đa tùy hãng, bài viết không nêu một con số chung. Nếu lý do hiển thị không đúng thực tế, liên hệ chăm sóc khách hàng để được hỗ trợ.

Rank 3 | doc_id=buyer-cancel-order | chunk_index=1
score=0.7243239956860187 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "recursive", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    ## Thao tác và giới hạn
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước được hoàn theo phương thức thanh toán và chính sách tương ứng khi hủy thành công.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không?

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Đơn hàng đã ở trạng thái Đã hủy không thể khôi phục để giao lại [1]. Nếu muốn mua tiếp, khách hàng cần đặt đơn mới và không mặc định giữ được ưu đãi cũ (khách hàng có thể trao đổi với shop về mức giá trước khi đặt lại) [1].

### Q4

Câu hỏi gốc: Đơn trả trước bằng thẻ tín dụng hoặc ghi nợ cần thanh toán trong bao lâu, nếu quá hạn thì sao?
Metadata filter: null
Gold answer: Hoàn tất trong 12 giờ kể từ lúc đặt hàng thành công; quá hạn không thanh toán thì hệ thống tự động hủy đơn.
Bằng chứng yêu cầu: [{"doc_id": "buyer-prepayment", "required_phrases": ["12 giờ", "kể từ khi đặt hàng thành công", "tự động hủy"]}]

Top-3 không lọc metadata; hit@3=true

Rank 1 | doc_id=buyer-prepayment | chunk_index=0
score=0.8137692339298644 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u
Metadata: {"audience": "buyer", "category": "payment-deadline", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-prepayment", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-prepayment.md", "source_section": "Dòng thẻ tín dụng/ghi nợ trong bảng và phần tra cứu hạn", "source_url": "https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u", "strategy": "recursive", "title": "Hạn thanh toán đơn trả trước"}
Nội dung chunk đầy đủ:
    # Thanh toán cho đơn trả trước
    
    ## Thanh toán bằng thẻ
    Với thẻ tín dụng hoặc ghi nợ, thời hạn hoàn tất thanh toán là 12 giờ kể từ khi đặt hàng thành công. Nếu không thanh toán trong hạn quy định, hệ thống tự động hủy đơn; đơn chưa thanh toán được xem là chưa hoàn tất. Mốc này không dùng chung cho mọi phương thức thanh toán.
    

Rank 2 | doc_id=buyer-prepayment | chunk_index=1
score=0.7113021764440534 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u
Metadata: {"audience": "buyer", "category": "payment-deadline", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-prepayment", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-prepayment.md", "source_section": "Dòng thẻ tín dụng/ghi nợ trong bảng và phần tra cứu hạn", "source_url": "https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u", "strategy": "recursive", "title": "Hạn thanh toán đơn trả trước"}
Nội dung chunk đầy đủ:
    ## Kiểm tra hạn của đơn cụ thể
    Xem hạn trên màn hình báo đặt hàng thành công. Cũng có thể mở Tôi, chọn Chờ xác nhận trong Đơn mua, mở đơn cần xem rồi tìm phần Chờ thanh toán. Dùng hạn hiển thị của chính đơn đó khi kiểm tra.

Rank 3 | doc_id=buyer-cancel-order | chunk_index=1
score=0.6518374456190995 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "recursive", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    ## Thao tác và giới hạn
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước được hoàn theo phương thức thanh toán và chính sách tương ứng khi hủy thành công.

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Đơn trả trước bằng thẻ tín dụng hoặc ghi nợ cần thanh toán trong bao lâu, nếu quá hạn thì sao?

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Đối với đơn hàng trả trước bằng thẻ tín dụng hoặc ghi nợ, thời hạn hoàn tất thanh toán là 12 giờ kể từ khi đặt hàng thành công [1]. Nếu không thanh toán trong thời hạn quy định, hệ thống sẽ tự động hủy đơn hàng [1].

### Q5

Câu hỏi gốc: Tôi xử lý yêu cầu hủy đơn hàng như thế nào?
Metadata filter: {"audience": "seller"}
Gold answer: Với vai trò người bán trên Kênh Quản Lý Shop: vào Đơn hủy > Chờ phản hồi > Xem thêm, đồng ý hoặc từ chối. Đồng ý chuyển sang Đã hủy; từ chối về Đã đóng gói trong Chờ lấy hàng.
Bằng chứng yêu cầu: [{"doc_id": "seller-cancel-request", "required_phrases": ["Đơn hủy > Chờ phản hồi > Xem thêm", "Đồng ý làm đơn chuyển sang Đã hủy", "từ chối đưa đơn về Đã đóng gói"]}]

Top-3 có lọc metadata; hit@3=true

Rank 1 | doc_id=seller-cancel-request | chunk_index=0
score=0.7668376528751506 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "recursive", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    # Phản hồi yêu cầu hủy trong Kênh Quản Lý Shop
    
    ## Xử lý yêu cầu của người mua
    Người bán mở Đơn hủy > Chờ phản hồi > Xem thêm để quyết định đồng ý hoặc từ chối. Đồng ý làm đơn chuyển sang Đã hủy; từ chối đưa đơn về Đã đóng gói trong nhóm Chờ lấy hàng. Đây là thao tác phía người bán trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua hàng.
    

Rank 2 | doc_id=seller-cancel-request | chunk_index=1
score=0.6988919598323349 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "recursive", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    ## Các nguyên nhân hủy
    Tài liệu liệt kê trường hợp người bán xác nhận trễ, bàn giao cho hãng vận chuyển trễ sau khi xác nhận, hoặc người mua hủy. Bài viết không nêu số ngày chung cho các thời hạn này, vì vậy không suy ra mốc ngày cụ thể từ bản hướng dẫn này.

Rank 3 | doc_id=seller-failed-delivery | chunk_index=1
score=0.6835081058069924 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/1/article/102523
Metadata: {"audience": "seller", "category": "failed-delivery", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "seller-failed-delivery", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-failed-delivery.md", "source_section": "Mục 1–3 về theo dõi, nhập kho và yêu cầu hỗ trợ", "source_url": "https://help.shopee.vn/portal/1/article/102523", "strategy": "recursive", "title": "Theo dõi kiện giao thất bại và hàng hoàn"}
Nội dung chunk đầy đủ:
    ## Hàng hỏng hoặc trạng thái không khớp
    Nếu hàng hoàn hư hỏng, cần sớm liên hệ chăm sóc khách hàng để hỗ trợ khiếu nại. Quay video khi mở kiện hoàn giúp lưu bằng chứng sự cố. Khi trạng thái hệ thống khác thực tế, có thể xuất danh sách đơn thành Excel để đối chiếu và gửi yêu cầu hỗ trợ. Hướng dẫn này không quy định một thời hạn khiếu nại tính bằng số ngày.

Đối chứng top-3 bỏ filter; hit@3=true

Rank 1 | doc_id=seller-cancel-request | chunk_index=0
score=0.7668376528751506 | answer_bearing=true
Nguồn: https://help.shopee.vn/portal/1/article/98754
Metadata: {"audience": "seller", "category": "cancellation", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "seller-cancel-request", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "seller-cancel-request.md", "source_section": "Mục B.5 Đơn hủy trong Kênh Quản Lý Shop", "source_url": "https://help.shopee.vn/portal/1/article/98754", "strategy": "recursive", "title": "Người bán phản hồi yêu cầu hủy"}
Nội dung chunk đầy đủ:
    # Phản hồi yêu cầu hủy trong Kênh Quản Lý Shop
    
    ## Xử lý yêu cầu của người mua
    Người bán mở Đơn hủy > Chờ phản hồi > Xem thêm để quyết định đồng ý hoặc từ chối. Đồng ý làm đơn chuyển sang Đã hủy; từ chối đưa đơn về Đã đóng gói trong nhóm Chờ lấy hàng. Đây là thao tác phía người bán trên Kênh Quản Lý Shop, không phải thao tác hủy trong ứng dụng mua hàng.
    

Rank 2 | doc_id=buyer-cancel-order | chunk_index=1
score=0.7519299004952688 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79182
Metadata: {"audience": "buyer", "category": "cancellation", "chunk_index": 1, "content_type": "authored-summary", "doc_id": "buyer-cancel-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancel-order.md", "source_section": "Mục 1, 2.1 và lưu ý: điều kiện hủy theo hãng/trạng thái", "source_url": "https://help.shopee.vn/portal/4/article/79182", "strategy": "recursive", "title": "Điều kiện người mua yêu cầu hủy đơn"}
Nội dung chunk đầy đủ:
    ## Thao tác và giới hạn
    Mở đơn trong mục Tôi, chọn thao tác hủy, chỉ định lý do rồi xác nhận. Mỗi đơn chỉ có một lần yêu cầu hủy; sau khi bị từ chối không gửi lại được. Tiền trả trước được hoàn theo phương thức thanh toán và chính sách tương ứng khi hủy thành công.

Rank 3 | doc_id=buyer-cancelled-order | chunk_index=0
score=0.7379581301412796 | answer_bearing=false
Nguồn: https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y
Metadata: {"audience": "buyer", "category": "cancelled-order", "chunk_index": 0, "content_type": "authored-summary", "doc_id": "buyer-cancelled-order", "document_version": "not-stated", "language": "vi", "license_or_permission": "team-authored-summary-of-public-facts", "platform": "shopee", "retrieved_at": "2026-09-20", "source_file": "buyer-cancelled-order.md", "source_section": "Phần khôi phục đơn và các nguyên nhân hủy", "source_url": "https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y", "strategy": "recursive", "title": "Đơn đã hủy và các nguyên nhân thường gặp"}
Nội dung chunk đầy đủ:
    # Sau khi đơn đã bị hủy
    
    ## Có khôi phục để giao lại không?
    Đơn mang trạng thái Đã hủy không thể khôi phục để giao lại. Muốn mua tiếp, khách cần đặt đơn mới; có thể trao đổi với shop về mức giá trước khi đặt lại, thay vì mặc định giữ được ưu đãi cũ.
    

Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):
Tôi xử lý yêu cầu hủy đơn hàng như thế nào?
Vai trò của người hỏi: người bán. Phạm vi tài liệu: {"audience": "seller"}

Câu trả lời agent nguyên văn (answer_mode=gemini; dùng top-3 chính ở trên):
Để xử lý yêu cầu hủy đơn hàng trên Kênh Người Bán, bạn thực hiện các bước sau:

1. Truy cập vào mục **Đơn hủy** trên Kênh Người Bán [1].
2. Chọn **Chờ phản hồi** [1].
3. Chọn **Xem thêm** để quyết định đồng ý hoặc từ chối yêu cầu hủy [1]:
   - Nếu bạn **đồng ý**, đơn hàng sẽ chuyển sang trạng thái **Đã hủy** [1].
   - Nếu bạn **từ chối**, đơn hàng sẽ quay trở lại trạng thái **Đã đóng gói** trong nhóm **Chờ lấy hàng** [1].

Lưu ý: Đây là thao tác thực hiện trên Kênh Người Bán, không phải thao tác hủy trong ứng dụng mua hàng [1].
