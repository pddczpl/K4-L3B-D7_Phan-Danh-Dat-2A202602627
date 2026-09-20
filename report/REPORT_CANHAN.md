# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Phan Danh Đạt

**Mã sinh viên:** 2A202602627

**Lớp:** K4-L3B

**Nhóm:** G23 — 3 thành viên; Nguyễn Văn A và Nguyễn Văn B là tên tạm của hai thành viên còn lại.

**Đề tài đã chọn:** Đơn hàng Shopee — theo dõi, hủy đơn, thanh toán và xử lý đơn của người mua/người bán.

**Ngày thực hiện:** 20/09/2026

**Phạm vi thực hiện:** Hoàn thiện mã nguồn cá nhân, warm-up, thí nghiệm cosine, chuẩn bị 7 tài liệu tóm lược từ nguồn chính thức và chạy đúng 5 câu hỏi trên chiến lược cá nhân HeadingChunker. Hai cấu hình FixedSize và Recursive được chạy trên cùng máy để đối chiếu; đây chưa phải bằng chứng hai thành viên khác tự thực hiện bài. Phần trình bày và thảo luận nhóm vẫn cần diễn ra thực tế.

Nguồn xuất phát là [danh mục Đơn hàng Shopee](https://help.shopee.vn/portal/4/category/60-%25C4%2590%25C6%25A1n-H%25C3%25A0ng-V%25E1%25BA%25ADn-Chuy%25E1%25BB%2583n/703-%25C4%2590%25C6%25A1n-h%25C3%25A0ng?page=1). Xem [ghi chú nguồn và cách biên soạn](../docs/SHOPEE_DATA_NOTES.md), [báo cáo nhóm](REPORT_NHOM.md) và [5 câu hỏi dùng chung](../data/shopee-orders/benchmark_queries.json).

## 1. Khởi động (Warm-up)

### 1.1. Cosine similarity

Cosine đo độ cùng hướng của hai vector, trong khoảng [-1, 1]. Với embedding ngữ nghĩa, điểm cao thường biểu thị nội dung gần nhau nhưng không chứng minh hai câu cùng đúng hoặc cùng kết luận.

**Ví dụ dự đoán cao:** “Đơn hàng đã hủy không thể được giao lại.” và “Không thể khôi phục đơn hàng đã hủy để tiếp tục giao.” Hai câu diễn đạt cùng ý bằng từ khác nhau.

**Ví dụ dự đoán thấp:** “Tôi kiểm tra trạng thái đơn hàng trong ứng dụng Shopee.” và “Đội bóng ghi bàn ở cuối trận đấu.” Nội dung đơn hàng và bóng đá khác nhau.

Cosine loại ảnh hưởng của độ lớn vector, tập trung so sánh hướng. Nếu hai vector đều được chuẩn hóa về độ dài 1 thì Euclid và cosine cho cùng thứ tự xếp hạng vì `d² = 2 − 2 × cosine`; không khẳng định cosine luôn tốt hơn mọi metric.

### 1.2. Bài toán chunking

```text
10.000 ký tự, chunk_size=500, overlap=50:
ceil((10000 − 50) / (500 − 50)) = ceil(9950 / 450) = 23 chunk.

Tăng overlap lên 100:
ceil((10000 − 100) / (500 − 100)) = ceil(9900 / 400) = 25 chunk.
```

Đã kiểm chứng bằng `FixedSizeChunker`; [file kết quả](individual_results_gemini.json) ghi đúng **23** và **25**. Tăng overlap giữ thêm ngữ cảnh ở ranh giới nhưng tăng dung lượng, số lần embedding và đoạn trùng khi truy xuất. Công thức dùng với tài liệu dài và tham số hợp lệ `0 <= overlap < chunk_size`.

## 2. Hướng tiếp cận của tôi

### 2.1. Các hàm chia nhỏ

**`SentenceChunker.chunk`:** Dùng `re.split(r"(?<=[.!?])\s+", text.strip())` để tách ở khoảng trắng sau dấu kết thúc câu; lookbehind giữ lại dấu câu. Loại đoạn rỗng rồi nhóm tối đa `max_sentences_per_chunk` câu bằng dấu cách. Chuỗi rỗng hoặc chỉ có khoảng trắng trả `[]`; câu cuối không có dấu chấm vẫn được giữ.

Giới hạn: regex đơn giản có thể tách sai chữ viết tắt như `TS. An` hoặc `v.v.`, và không nhận biết đầy đủ dấu ngoặc kép kết thúc câu. Số `3.14` không bị tách bởi regex này vì sau dấu chấm không có khoảng trắng. Sentence chunking giới hạn số câu, không giới hạn số ký tự.

**`RecursiveChunker.chunk` / `_split`:** Thử lần lượt `\n\n`, `\n`, `. `, dấu cách, rồi cắt theo ký tự. Mảnh quá dài được đệ quy bằng separator tiếp theo; những mảnh ngắn liền kề được gom trong giới hạn `chunk_size`. Giữ separator cùng nội dung để ghép các chunk trở lại thu được chính xác văn bản ban đầu.

Ba trường hợp dừng: văn bản rỗng trả `[]`; văn bản vừa kích thước trả một chunk; hết separator hoặc gặp separator rỗng thì cắt trực tiếp theo ký tự. `chunk_size <= 0` bị từ chối. Cắt cuối cùng theo ký tự có thể tách giữa từ, còn ưu tiên ranh giới lớn có thể tạo chunk chưa đầy.

**`compute_similarity`:** Tái sử dụng `_dot`, tính tích vô hướng chia cho tích hai chuẩn Euclid. Trả `0.0` khi một vector có chuẩn bằng 0 (kể cả hai vector rỗng); báo `ValueError` nếu số chiều khác nhau; chặn sai số làm tròn ngoài [-1, 1].

**`ChunkingStrategyComparator.compare`:** Chạy cả ba chiến lược, trả đúng các khóa `fixed_size`, `by_sentences`, `recursive`, mỗi mục có `count`, `avg_length`, `chunks`. Với baseline `chunk_size=200`, FixedSize dùng overlap 20 (`min(50, chunk_size // 10)`), Sentence dùng 3 câu/chunk; dữ liệu rỗng cho độ dài trung bình 0.

### 2.2. EmbeddingStore

**Khởi tạo:** Dùng store trong bộ nhớ theo hướng dẫn Giai đoạn 1 tại `day7-lab-data-foundations.md`, mục 5. Store này không lưu bền sau khi chương trình kết thúc và không cần ChromaDB.

**`_make_record` / `add_documents`:** Mỗi `Document` đầu vào thành đúng một record; store không tự chunk. Mỗi record có ID nội bộ tăng dần, nội dung, embedding và bản sao sâu của metadata. Giữ nguyên `metadata['doc_id']` nếu người gọi đã gán tên tài liệu gốc, nếu chưa thì lấy `Document.id`; thêm tài liệu trùng ID vẫn tạo record mới.

**`_search_records` / `search`:** Nhúng câu hỏi, tính dot product với từng vector trong tập ứng viên, sắp xếp điểm giảm dần rồi lấy `top_k`. Với vector đơn vị, dot product bằng cosine; với backend tự cung cấp chưa chuẩn hóa, điểm chỉ là dot product và không được mặc định diễn giải là cosine. Kết quả trả `id`, `content`, `metadata`, `score`, không in toàn bộ vector; metadata trả về cũng được sao chép để không làm thay đổi store. Kho rỗng và `top_k <= 0` trả `[]`.

**`search_with_filter`:** Lọc trước khi xếp hạng, yêu cầu tất cả trường trong bộ lọc khớp chính xác. Cách này giữ cơ hội xuất hiện cho tài liệu hợp lệ có điểm thấp hơn các tài liệu sai đối tượng; nếu lọc sau top-k thì các vị trí có thể đã bị tài liệu sai chiếm hết. `audience='both'` không tự khớp bộ lọc `audience='buyer'`; corpus Shopee hiện tách rõ buyer/seller và không dùng giá trị both.

**`delete_document`:** Xóa mọi record có `metadata['doc_id']` trùng tài liệu gốc và trả `True` khi thực sự xóa được ít nhất một chunk; trả `False` nếu không tìm thấy. `get_collection_size` trả số record hiện có.

### 2.3. KnowledgeBaseAgent

Lưu `store` và `llm_fn`, sau đó thực hiện đúng ba bước: truy xuất top-k → dựng prompt → gọi `llm_fn`. Prompt có `Context`, `Question`, các chunk đánh số `[1]`, `[2]`, ... và nguồn ưu tiên `source_url`, `source`, `doc_id`, cuối cùng ID record; yêu cầu câu trả lời trích dẫn số nguồn và chỉ dựa trên ngữ cảnh.

Nếu store không trả chunk, agent trả thông báo chưa tìm thấy thông tin và không gọi LLM. Nếu có chunk nhưng thiếu đáp án, prompt yêu cầu nói rõ thiếu thông tin; đây là chỉ dẫn cho LLM, không phải bảo đảm tự động rằng model sẽ luôn tuân thủ. Agent cũng coi chỉ dẫn nằm trong tài liệu là dữ liệu tham khảo.

### 2.4. Chiến lược riêng theo tiêu đề/mục

Tôi dùng **`HeadingChunker(chunk_size=500)`** cho corpus đơn hàng Shopee. Chunker tách theo heading Markdown từ `#` đến `######`, giữ heading cha và con trong mỗi chunk, rồi dùng RecursiveChunker chia tiếp phần thân quá dài. Nhờ vậy một đoạn về ngoại lệ SPX vẫn mang tiêu đề riêng, ít bị hiểu lẫn với quy tắc các hãng khác.

Phần thân không quá 500 ký tự tính cả heading được giữ nguyên theo section; fragment được chuẩn hóa xuống dòng và strip khoảng trắng ngoài. Heading xuất hiện trong code fence không bị coi là mục mới. Nếu heading quá dài khiến phần thân còn dưới 1/4 ngân sách ký tự, code chia cả section để giữ giới hạn kích thước, có thể không lặp đủ heading trong từng mảnh.

Đây là heading do nhóm biên tập trong các **bản tóm lược**, không phải toàn bộ cấu trúc HTML của Shopee. Corpus nhỏ nên không suy rộng chiến lược thắng cho mọi tài liệu.

### 2.5. Nạp dữ liệu và chạy RAG thật

Bảy file trong `data/shopee-orders/` được tách frontmatter trước khi embedding. Mỗi chunk giữ `doc_id`, `source_url`, `retrieved_at`, `document_version`, `audience`, `category`, `language`, `chunk_index` và tên chiến lược. `doc_id` trỏ về file gốc; `audience` có 5 tài liệu buyer và 2 tài liệu seller.

Embedding dùng **gemini-embedding-001**, 3.072 chiều, task `RETRIEVAL_DOCUMENT` cho đoạn và `RETRIEVAL_QUERY` cho câu hỏi; vector được chuẩn hóa L2 trước dot product. Sinh trả lời dùng **gemini-3.1-flash-lite**, temperature 0, tối đa 2.048 token, qua KnowledgeBaseAgent với ngữ cảnh thực truy xuất. Không đưa gold answer vào prompt và không âm thầm đổi sang mock khi API lỗi.

Lọc metadata thực hiện trước top-k. Với Q5, câu hỏi cố ý không chứa vai trò; bộ lọc seller vừa giới hạn tài liệu vừa cung cấp vai trò người bán khi dựng câu hỏi gửi LLM. Có lưu truy xuất không lọc để đối chiếu, nhưng không gọi LLM riêng trên các kết quả không lọc; không suy ra mức tăng độ đúng câu trả lời từ riêng phép đối chiếu này.

Cache embedding phân biệt model, task và nội dung; cache câu trả lời phân biệt model, thiết lập và prompt. Cache và `.env` được Git bỏ qua. Kết quả có cả hash corpus/câu hỏi để đối chiếu dữ liệu chạy.

### 2.6. Comparator cốt lõi trên 3 tài liệu Shopee

Giữ baseline cốt lõi `chunk_size=200`, FixedSize overlap 20, Sentence 3 câu/chunk. Bảng này khác cấu hình benchmark cuối cùng Heading 500 / FixedSize 350–50 / Recursive 500.

| Tài liệu | Chiến lược | Số chunk | Ký tự trung bình |
|---|---|---:|---:|
| `data/shopee-orders/buyer-cancel-order.md` | `fixed_size` | 4 | 198.00 |
| `data/shopee-orders/buyer-cancel-order.md` | `by_sentences` | 3 | 242.67 |
| `data/shopee-orders/buyer-cancel-order.md` | `recursive` | 8 | 91.50 |
| `data/shopee-orders/buyer-cancelled-order.md` | `fixed_size` | 4 | 163.25 |
| `data/shopee-orders/buyer-cancelled-order.md` | `by_sentences` | 3 | 196.67 |
| `data/shopee-orders/buyer-cancelled-order.md` | `recursive` | 6 | 98.83 |
| `data/shopee-orders/buyer-order-status.md` | `fixed_size` | 4 | 159.50 |
| `data/shopee-orders/buyer-order-status.md` | `by_sentences` | 2 | 288.00 |
| `data/shopee-orders/buyer-order-status.md` | `recursive` | 7 | 82.57 |

Sentence giữ câu nhưng không ràng buộc 200 ký tự. FixedSize có overlap và có thể cắt giữa ý; Recursive gom các mảnh ngắn theo ưu tiên separator. Cần kiểm tra đoạn chứa đủ đáp án thay vì đánh giá chiến lược chỉ qua số chunk.

## 3. Hoàn thiện code và kiểm thử

Môi trường: Windows, Python 3.11.9, pytest 9.1.1. **42/42 bài test gốc đạt; tổng cộng 81/81 đạt**: 42 bài gốc + 20 bài biên cho core + 11 bài HeadingChunker + 8 bài benchmark/cache/bằng chứng/lọc. Test chạy offline, không cần API key.

Đầu ra thực của `python -m pytest tests/ -v`, lưu riêng trong [pytest_shopee.txt](pytest_shopee.txt):

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- F:\Personal_Project\Vin\K4-L3B-D7_Phan-Danh-Dat-2A202602627\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: F:\Personal_Project\Vin\K4-L3B-D7_Phan-Danh-Dat-2A202602627
plugins: anyio-4.15.1
collecting ... collected 81 items

tests/test_edge_cases.py::test_sentence_chunker_ignores_empty_input[] PASSED [  1%]
tests/test_edge_cases.py::test_sentence_chunker_ignores_empty_input[ \t\n  ] PASSED [  2%]
tests/test_edge_cases.py::test_sentence_chunker_preserves_punctuation_and_final_sentence PASSED [  3%]
tests/test_edge_cases.py::test_recursive_chunker_preserves_content_and_enforces_size[None] PASSED [  4%]
tests/test_edge_cases.py::test_recursive_chunker_preserves_content_and_enforces_size[separators1] PASSED [  6%]
tests/test_edge_cases.py::test_recursive_chunker_preserves_content_and_enforces_size[separators2] PASSED [  7%]
tests/test_edge_cases.py::test_recursive_chunker_preserves_content_and_enforces_size[separators3] PASSED [  8%]
tests/test_edge_cases.py::test_recursive_chunker_merges_adjacent_short_lines PASSED [  9%]
tests/test_edge_cases.py::test_empty_comparison_has_no_chunks_or_division_by_zero PASSED [ 11%]
tests/test_edge_cases.py::test_cosine_is_scale_invariant_and_accepts_empty_vectors PASSED [ 12%]
tests/test_edge_cases.py::test_cosine_rejects_different_dimensions_instead_of_truncating PASSED [ 13%]
tests/test_edge_cases.py::test_store_copies_metadata_on_ingest_and_on_search PASSED [ 14%]
tests/test_edge_cases.py::test_store_defaults_doc_id_without_mutating_document_metadata PASSED [ 16%]
tests/test_edge_cases.py::test_duplicate_ids_append_and_delete_removes_every_matching_record PASSED [ 17%]
tests/test_edge_cases.py::test_delete_uses_original_doc_id_and_keeps_other_documents PASSED [ 18%]
tests/test_edge_cases.py::test_filter_all_fields_before_ranking_and_top_k PASSED [ 19%]
tests/test_edge_cases.py::test_nonpositive_top_k_returns_no_results[0] PASSED [ 20%]
tests/test_edge_cases.py::test_nonpositive_top_k_returns_no_results[-1] PASSED [ 22%]
tests/test_edge_cases.py::test_agent_passes_retrieved_context_source_and_question_to_llm PASSED [ 23%]
tests/test_edge_cases.py::test_agent_with_empty_store_does_not_call_llm PASSED [ 24%]
tests/test_heading_chunking.py::test_blank_markdown_has_no_chunks[] PASSED [ 25%]
tests/test_heading_chunking.py::test_blank_markdown_has_no_chunks[ \n\t\r\n ] PASSED [ 27%]
tests/test_heading_chunking.py::test_child_section_keeps_parents_but_not_sibling_heading PASSED [ 28%]
tests/test_heading_chunking.py::test_long_section_repeats_context_and_retains_body_in_order PASSED [ 29%]
tests/test_heading_chunking.py::test_preamble_and_empty_sections_are_retained PASSED [ 30%]
tests/test_heading_chunking.py::test_hash_lines_inside_fenced_code_are_not_section_boundaries PASSED [ 32%]
tests/test_heading_chunking.py::test_oversized_heading_falls_back_without_losing_content PASSED [ 33%]
tests/test_heading_chunking.py::test_long_heading_does_not_repeat_for_every_few_body_characters PASSED [ 34%]
tests/test_heading_chunking.py::test_document_without_headings_uses_recursive_body_splitting PASSED [ 35%]
tests/test_heading_chunking.py::test_nonpositive_chunk_size_is_rejected[0] PASSED [ 37%]
tests/test_heading_chunking.py::test_nonpositive_chunk_size_is_rejected[-1] PASSED [ 38%]
tests/test_shopee_benchmark.py::test_metadata_is_preserved_but_not_embedded PASSED [ 39%]
tests/test_shopee_benchmark.py::test_evidence_requires_all_phrases_in_same_chunk_and_doc PASSED [ 40%]
tests/test_shopee_benchmark.py::test_validation_rejects_wrong_query_count_and_invented_evidence PASSED [ 41%]
tests/test_shopee_benchmark.py::test_rag_uses_filtered_context_original_query_embeddings_and_only_15_answers PASSED [ 43%]
tests/test_shopee_benchmark.py::test_mock_output_is_explicitly_an_offline_non_llm_smoke PASSED [ 44%]
tests/test_shopee_benchmark.py::test_embedding_cache_is_separated_by_task_and_vectors_are_normalized PASSED [ 45%]
tests/test_shopee_benchmark.py::test_api_errors_never_expose_response_or_key PASSED [ 46%]
tests/test_shopee_benchmark.py::test_generation_cache_preserves_model_settings_and_disables_function_calls PASSED [ 48%]
tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED [ 49%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED [ 50%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED [ 51%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED [ 53%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED [ 54%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED [ 55%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED [ 56%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED [ 58%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED [ 59%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED   [ 60%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED [ 61%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED [ 62%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED [ 64%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED    [ 65%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED [ 66%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED [ 67%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED [ 69%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED [ 70%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED   [ 71%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED [ 72%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED [ 74%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED [ 75%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED [ 76%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED [ 77%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED [ 79%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED [ 80%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED [ 81%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED [ 82%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED [ 83%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED [ 85%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED [ 86%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED [ 87%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED [ 88%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED [ 90%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED [ 91%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED [ 92%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED [ 93%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED [ 95%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED [ 96%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 98%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]

============================= 81 passed in 0.25s ==============================
```

Demo theo đề tài được chạy bằng `python -m scripts.run_shopee_benchmark --provider gemini --llm gemini`, sinh 15 câu trả lời thật cho 3 cấu hình × 5 câu hỏi. Bản chạy hoàn tất có 11 lượt sinh mới và 4 câu trả lời từ cache của lượt cùng cấu hình trước đó; toàn bộ embedding đọc lại từ cache sau khi đã gọi API thành công. Đây không phải phản hồi của `demo_llm` giả lập trong starter.

## 4. Dự đoán độ tương tự

Đã đổi cả 5 cặp câu sang đề tài đơn hàng và lưu [dự đoán](similarity_predictions.json) **trước khi chạy lại**: cặp 2 cao nhất, cặp 4 thấp nhất. Các câu là ví dụ tự tạo, không phải điều khoản áp dụng chung của Shopee.

Dùng `gemini-embedding-001`, 3.072 chiều, task `SEMANTIC_SIMILARITY`, rồi gọi `compute_similarity()` của mã nguồn cá nhân. [Kết quả Gemini](individual_results_gemini.json) và [đối chứng Mock](individual_results_mock.json) lưu điểm và thời gian thực chạy.

| Cặp | Câu A | Câu B | Dự đoán trước chạy | Cosine Gemini |
|---|---|---|---|---:|
| 1 | Tôi muốn biết kiện hàng của mình đang ở đâu. | Làm thế nào để theo dõi quá trình vận chuyển đơn tôi đã mua? | Cao; cùng nhu cầu theo dõi hành trình kiện hàng. | 0.892952 |
| 2 | Đơn hàng đã hủy không thể được giao lại. | Không thể khôi phục đơn hàng đã hủy để tiếp tục giao. | Cao nhất; hai cách diễn đạt cùng ý về đơn đã hủy. | 0.973387 |
| 3 | Tôi cần hủy đơn hàng trước khi giao. | Tôi muốn xem hạn thanh toán của đơn hàng. | Trung bình; cùng đơn hàng nhưng khác nhu cầu xử lý. | 0.774130 |
| 4 | Tôi kiểm tra trạng thái đơn hàng trong ứng dụng Shopee. | Đội bóng ghi bàn ở cuối trận đấu. | Thấp nhất; khác chủ đề và ý nghĩa. | 0.708120 |
| 5 | Người mua có thể hủy đơn hàng. | Người mua không thể hủy đơn hàng. | Cao về chủ đề dù từ phủ định đảo ngược kết luận. | 0.883427 |

Dự đoán cao nhất/thấp nhất đều đúng. Cặp 4 khác chủ đề vẫn đạt **0,708120**, nên không thể mặc định một ngưỡng tuyệt đối như 0,7 là đủ kết luận liên quan. Cặp 5 trái nghĩa vì phủ định nhưng vẫn đạt **0,883427**: cần đọc điều kiện thực trong nguồn, không coi similarity là phép kiểm tra đúng/sai.

| Cặp | Gemini | Mock |
|---|---:|---:|
| 1 | 0.892952 | -0.162627 |
| 2 | 0.973387 | -0.155716 |
| 3 | 0.774130 | -0.070208 |
| 4 | 0.708120 | 0.191777 |
| 5 | 0.883427 | -0.251230 |

Mock xếp cặp 4 cao nhất và cặp 5 thấp nhất. Nó băm MD5 để sinh vector giả ngẫu nhiên, phục vụ kiểm thử cấu trúc, không đo ngữ nghĩa.

## 5. Kết quả truy xuất của tôi

### 5.1. Cấu hình và kết quả 5 câu hỏi

Chiến lược cá nhân: HeadingChunker 500, **15 chunk từ 7 tài liệu**, `top_k=3`. Q2 lọc buyer, Q5 lọc seller; các câu khác không lọc. Bảng dưới tóm tắt câu trả lời thực; nội dung nguyên vẹn và top-3 nằm ở [ket_qua_benchmark.txt](ket_qua_benchmark.txt), [chi tiết benchmark](SHOPEE_BENCHMARK_DETAILS.md) và [JSON gốc](shopee_benchmark_gemini_gemini.json).

| Câu | Câu hỏi dùng chung | Top-1 (doc_id#chunk_index, cosine) | Đủ bằng chứng? | Agent trả lời (tóm tắt) |
|---|---|---|---|---|
| Q1 | Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua? | `buyer-order-status#0` (0.792906) | Có; chứa đủ bằng chứng | Vào Tôi > Đơn mua [1]. |
| Q2 | Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không? | `buyer-cancel-order#0` (0.824767) | Có; chứa đủ bằng chứng | Chờ người bán chấp nhận; nếu từ chối thì đơn tiếp tục giao [1]. |
| Q3 | Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không? | `buyer-cancelled-order#0` (0.811881) | Có; chứa đủ bằng chứng | Không khôi phục; đặt đơn mới, không mặc định giữ ưu đãi cũ [1]. |
| Q4 | Đơn trả trước bằng thẻ tín dụng hoặc ghi nợ cần thanh toán trong bao lâu, nếu quá hạn thì sao? | `buyer-prepayment#0` (0.818672) | Có; chứa đủ bằng chứng | 12 giờ từ khi đặt thành công; không thanh toán kịp thì tự hủy [1]. |
| Q5 | Tôi xử lý yêu cầu hủy đơn hàng như thế nào? | `seller-cancel-request#0` (0.770700) | Có; chứa đủ bằng chứng | Trên Kênh Quản Lý Shop: Đơn hủy > Chờ phản hồi > Xem thêm. Đồng ý → Đã hủy; từ chối → Đã đóng gói / Chờ lấy hàng [1]. |

**Hit@3: 5/5; top-1 chứa đủ bằng chứng: 5/5; đối chiếu nội dung: 5/5 câu trả lời đúng các ý của gold và có trích nguồn.** Đây là kết quả trên corpus nhỏ đã chọn, không phải kết luận tổng quát về Shopee.

### 5.2. Top-3 cụ thể

| Câu | Hạng 1 | Hạng 2 | Hạng 3 |
|---|---|---|---|
| Q1 | `buyer-order-status#0` (0.792906) | `buyer-track-chat#0` (0.768793) | `buyer-order-status#1` (0.756902) |
| Q2 | `buyer-cancel-order#0` (0.824767) | `buyer-cancel-order#1` (0.814702) | `buyer-cancelled-order#1` (0.717099) |
| Q3 | `buyer-cancelled-order#0` (0.811881) | `buyer-cancelled-order#1` (0.739035) | `seller-cancel-request#0` (0.713686) |
| Q4 | `buyer-prepayment#0` (0.818672) | `buyer-prepayment#1` (0.753443) | `buyer-cancelled-order#1` (0.644761) |
| Q5 | `seller-cancel-request#0` (0.770700) | `seller-cancel-request#1` (0.723894) | `seller-failed-delivery#1` (0.677785) |

Một chunk được đánh dấu đủ bằng chứng khi đúng tài liệu **và chứa toàn bộ cụm điều kiện/đáp án đã định nghĩa trong cùng chunk**. Hit@3 là chỉ số truy xuất; không tự đánh dấu câu trả lời đúng chỉ vì tìm được đúng doc_id. Nội dung các câu trả lời được [đọc đối chiếu riêng](shopee_answer_review.json).

### 5.3. Metadata có giúp không?

Với Q5 “Tôi xử lý yêu cầu hủy đơn hàng như thế nào?”, không lọc thì top-3 Heading gồm 1 chunk seller và 2 chunk buyer. Lọc `audience=seller` giữ 3/3 chunk thuộc đối tượng người bán. Chunk đủ đáp án đã ở hạng 1 ngay cả khi chưa lọc, nên **Hit@3 không tăng**; cải thiện đo được là loại các hướng dẫn sai vai trò khỏi ngữ cảnh. Q2 cho cùng top-3 trước/sau lọc buyer trong lần chạy này.

### 5.4. So sánh và phân tích lỗi

| Cấu hình trên cùng máy | Số chunk | Hit@3 | Top-1 đủ bằng chứng | Trả lời hoàn toàn đúng | Điểm tham khảo theo rubric |
|---|---:|---:|---:|---:|---:|
| Heading 500 — chiến lược của Đạt | 15 | 5/5 | 5/5 | 5/5 | 10/10 |
| FixedSize 350, overlap 50 — cấu hình đối chiếu | 15 | 5/5 | 4/5 | 4/5 | 8/10 |
| Recursive 500 — cấu hình đối chiếu | 13 | 5/5 | 5/5 | 4/5 | 9/10 |

Điểm trong bảng là **tham khảo khi đọc đối chiếu rubric**, không phải điểm giảng viên; hai cấu hình đối chiếu không phải kết quả hai thành viên đã tự thực hiện.

**Lỗi xếp hạng:** Ở Q2, FixedSize đưa đoạn ngoại lệ SPX lên hạng 1 (0,8501), còn đoạn đủ quy tắc hãng khác ở hạng 2 (0,8296). Agent vẫn trả lời đúng nhờ trích [2], nhưng nếu chỉ lấy top-1 sẽ thiếu điều kiện cần. Heading giữ nhãn mục nên trong lần chạy này đoạn đúng nằm hạng 1. Có thể thử đổi kích thước/overlap hoặc thêm reranking ở lần nghiên cứu sau; chưa chạy các thay đổi đó.

**Lỗi grounding:** Ở Q5, Recursive truy xuất đúng nguồn nhưng Gemini thay tên **Kênh Quản Lý Shop** bằng **Kênh Người Bán** nhiều lần; FixedSize cũng bị nhầm ở câu mở đầu. Đây là sai lệch tên giao diện, dù các bước và nhánh đồng ý/từ chối vẫn đúng. Cần yêu cầu giữ nguyên tên tính năng trong nguồn và kiểm tra câu trả lời theo những thực thể quan trọng; chưa khẳng định cách sửa này đã được kiểm nghiệm.

**Bài học từ thực nghiệm:** Retrieval tốt không đảm bảo generation đúng; lọc metadata giúp giới hạn đối tượng nhưng không tự sửa tên giao diện do LLM tạo ra. Chưa có bài học từ demo với thành viên/nhóm khác vì buổi trình bày và thảo luận chưa diễn ra.

## 6. Tự đánh giá tiến độ

| Hạng mục cá nhân | Điểm tối đa | Bằng chứng đã có |
|---|---:|---|
| Khởi động | 5 | Giải thích cosine; kiểm chứng 23/25 chunk |
| Hướng tiếp cận | 10 | Core, heading, metadata, prompt và giới hạn |
| Hoàn thiện code | 30 | 42/42 test gốc, tổng 81/81 |
| Dự đoán cosine | 5 | 5 cặp đơn hàng, dự đoán trước chạy, Gemini và Mock |
| Truy xuất cá nhân | 10 | 5 câu hỏi cố định, top-3, trả lời thật, đối chiếu và failure case |
| **Tổng** | **60** | **Đã có bằng chứng kỹ thuật cho các mục; điểm chính thức do giảng viên đánh giá** |

Nhóm cần thay hai tên tạm bằng thông tin thật, mỗi người tự chạy cấu hình riêng và thực hiện phần demo/thảo luận để hoàn tất hoạt động nhóm.

## 7. Chạy lại

```powershell
.\venv\Scripts\python.exe -m pytest tests/ -v
.\venv\Scripts\python.exe -m scripts.run_individual_checks --provider gemini
.\venv\Scripts\python.exe -m scripts.run_individual_checks --provider mock
.\venv\Scripts\python.exe -m scripts.run_shopee_benchmark --provider mock
.\venv\Scripts\python.exe -m scripts.run_shopee_benchmark --provider gemini --llm gemini
.\venv\Scripts\python.exe -m scripts.export_shopee_results --details
```

Nếu dựng môi trường mới: dùng Python 3.11, cài `requirements.txt` và `requirements-gemini.txt`. Khóa đọc từ `.env`; không đưa khóa vào Git. Các script cập nhật JSON và bản xuất chi tiết; báo cáo phân tích này là ảnh chụp kết quả ngày 20/09/2026, cần đối chiếu lại nếu corpus hoặc cấu hình thay đổi.
