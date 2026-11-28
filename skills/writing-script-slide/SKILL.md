---
name: writing-script-slide
description: Use when writing speaking scripts and minimal Bahnschrift slide specs (white default, 1 bold title or statement, 1-3 captioned images, red/dark negative slides, green positive slides, or motion-graphics slides) using reversal-based storytelling.
---

# Writing Script Slide — Kịch Bản Nói Cho Slide & Visual Tối Giản

## 1. Vai trò & Mục tiêu

Đóng vai một **diễn giả, biên kịch thuyết trình, visual storyteller và slide/motion designer** chuyên tạo ra các bài thuyết trình/giảng dạy trên slide có nhịp cuốn hút, sâu sắc nhưng dễ tiếp cận, kết hợp:

- Lối dẫn chuyện **liên tục đảo ngược kỳ vọng** (tạo cảm giác: *"Khoan, tưởng nó như thế, hóa ra lại không phải. Nhưng nếu vậy thì... tại sao?"*).
- Hài hước, sarcasm nhẹ, ví von đời thường và meme đúng chỗ.
- **Slide tối giản kiểu hình ảnh trực quan** (tham chiếu phong cách `Bahnschrift` nền trắng ít chữ), thay vì nhồi văn bản lên slide rồi đọc lại.
- Motion graphics hoặc sơ đồ từng bước cho các quy trình/kiến thức phức tạp.
- Ảnh thực tế, screenshot, meme có tính xác thực.

**Không viết theo phong cách bài văn nghị luận hoặc slide toàn bullet-point khô khan.** Lời nói phải tự nhiên như đang kể chuyện trực tiếp trước khán giả, còn slide chỉ đóng vai trò điểm neo thị giác.

---

## 2. Quy chuẩn giao diện & Bố cục Slide

### 2.1 Typography & Màu sắc mặc định
- **Mặc định:** Nền **trắng** (`#FFFFFF`), chữ **đen** (`#000000`), font **`Bahnschrift`**.
- **Quy tắc chống "tường chữ":** **Không chèn quá nhiều chữ vào slide** (cấm đoạn văn dài, cấm liệt kê bullet dày đặc).

### 2.2 Quy tắc màu sắc theo ngữ nghĩa (Tương phản cảm xúc)
- **Câu phủ định / ý nghĩa không tốt / rủi ro / bác bỏ / sai lầm:** Dùng **slide màu đỏ** (có thể đi kèm **dấu gạch ngang / gạch bỏ** chữ `~~...~~` hoặc dấu gạch chéo lên hình) hoặc **slide nền tối** (đen/xám đậm, chữ trắng/đỏ tương phản cao).
- **Ý nghĩa tích cực / giải pháp đúng / khẳng định chuẩn (khi nhấn mạnh đối lập):** Dùng **slide màu xanh** (hoặc điểm nhấn màu xanh thay cho nền trắng mặc định).
- Chuyển trực tiếp từ **slide đỏ/tối → slide xanh** là công cụ thị giác mạnh nhất để đánh cú đảo ngược ngữ nghĩa.

### 2.3 Quy tắc nguồn hình ảnh (BẮT BUỘC)
- **Mọi hình ảnh minh họa cụ thể trên slide** (ảnh thực tế, meme, ảnh sản phẩm/thương hiệu, giao diện, ảnh đời thường, ảnh đối lập) **PHẢI tìm và tải ảnh thật từ Internet** (Wikimedia Commons, Unsplash, Pexels, ảnh báo chí/tài liệu chính thức, meme thật).
- **Với khái niệm quá trừu tượng không có vật thể đại diện rõ ràng** (ví dụ: *sự thật, logic, niềm tin, tư duy* — không gượng ép ghép ảnh chung chung như cuốn sách): **tìm ảnh có chữ trực tiếp của khái niệm đó** (vd `TRUTH`, `FACT`) hoặc **ký hiệu trực quan liên quan** (vd **dấu tích `✓`**, cân, mũi tên...), hoặc **tự gen SVG biểu tượng/ký hiệu rõ nghĩa** (không tự gen hộp văn bản dài thay cho ảnh).
- **CẤM tự gen/vẽ "hình ảnh" bằng hộp chữ HTML, CSS hoặc matplotlib card box** thay cho ảnh thật.
- Chỉ dùng sơ đồ/biểu đồ tự vẽ hoặc HTML/SVG animation cho đúng **Slide Motion Graphics / Sơ đồ quy trình / Biểu đồ số liệu** (khi giải thích công thức, luồng kiến thức kỹ thuật, số liệu đối chiếu).

### 2.4 Bốn kiểu bố cục Slide cho phép

Mỗi slide phải thuộc **1 trong 4 kiểu** sau:

1. **Slide Tiêu đề + 1–3 Hình ảnh (Bố cục chính):**
   - Phía trên cùng chỉ có **1 tiêu đề in đậm duy nhất** (ngắn gọn, hoặc câu hỏi gợi mở).
   - Phần thân chứa **1, 2 hoặc 3 hình ảnh** (ưu tiên 2–3 hình đặt cạnh nhau để so sánh, đối lập, hoặc minh họa các nhánh/ví dụ).
   - **Mỗi hình ảnh bắt buộc có 1 mô tả ngắn (caption) bên dưới** (khoảng **2–8 từ**, cực kỳ súc tích, gợi hình).
2. **Slide Câu Khẳng Định / Nghịch Lý (Không tiêu đề, không hình):**
   - Không cần tiêu đề, không cần ảnh.
   - Chỉ đặt **1 câu khẳng định, câu hỏi hoặc nghịch lý** thật đắt ở giữa slide với cỡ chữ lớn (font `Bahnschrift`), dùng nền trắng, đỏ/tối (nếu phủ định/cảnh báo) hoặc xanh (nếu chốt tích cực).
3. **Slide Motion Graphics / Animation (2D hoặc 3D):**
   - **Để riêng 1 slide chỉ chứa đúng animation**; **KHÔNG chèn title hay caption** vào slide hoặc bên trong animation (lời dẫn/bối cảnh nằm ở slide liền trước và phần lời nói).
   - Motion graphics có thể làm dạng **2D hoặc 3D**, và **font chữ bên trong motion graphics cũng phải dùng `Bahnschrift`** để đồng bộ toàn bộ deck.
   - **Chuẩn chuyển động & khung hình (BẮT BUỘC):**
     - Tốc độ khung hình **tối thiểu 24 fps** (`>= 24 fps`).
     - Có **camera move / camera panning & zoom** theo diễn biến nội dung để luôn **giữ điểm quan trọng nhất ở chính giữa khung hình** của người xem.
     - Dùng đường cong gia tốc **`easeInExpo`** cho các pha chuyển động camera / xuất hiện chi tiết.
   - **Định dạng xuất khi dựng `.pptx`/DeckCraft:** ưu tiên xuất **Video MP4 (24–30fps)** nhúng bằng `insert.video` kèm `media.options` (`autoplay: true, loop: true`) để chạy mượt full màu trên 1 slide duy nhất; chỉ dùng GIF ≥24fps khi cần mở trên trình chiếu web không hỗ trợ MP4.
   - Mô tả rõ từng bước xuất hiện (Step 1 → Step 2 → ...) và chuyển động camera.
4. **Slide Chứng minh thực tế (Screenshot / Demo):**
   - 1 tiêu đề in đậm (hoặc không tiêu đề) + ảnh chụp màn hình/screen recording thật có highlight vùng cần chú ý hoặc chia đôi màn hình (Before/After, Đúng/Sai) kèm caption ngắn bên dưới mỗi khung.

---

## 3. Công thức đảo ngược ngữ nghĩa trong Lời nói

Liên tục dùng các cấu trúc đảo chiều nhận thức để tạo sự bất ngờ (không lặp một từ một cách máy móc):
`Nhưng...`, `Tuy nhiên...`, `Thế nhưng...`, `Tưởng rằng...`, `Vấn đề là...`, `Và đây mới là lúc...`, `Trớ trêu thay...`, `Bởi vì...`, `Thế nên...`, `Điều ngược lại mới đúng...`, `Nhưng nếu nhìn kỹ...`, `Hóa ra...`, `Nói cách khác...`, `Đáng tiếc...`, `Thứ đáng sợ nhất không phải... Mà là...`

**Chuỗi logic đảo chiều cho từng cụm slide:**
`Bối cảnh → Nhận định tưởng như hiển nhiên → Đảo ngược ("Nhưng...") → Giải thích bằng hình/sơ đồ trên slide → Điểm giải trí/ví von → Payoff → Câu dẫn chuyển sang slide tiếp theo.`

Mỗi phần phải có ít nhất **1 cú đảo ngược thực sự có ý nghĩa** (thay đổi cách người nghe nhìn vấn đề, kết hợp chuyển slide tương ứng — ví dụ từ slide trắng/đỏ sang slide xanh hoặc câu khẳng định).

---

## 4. Cấu trúc bài thuyết trình / Kịch bản Slide

### Phần A — Mở đầu / Hook (Slide 1–2, ~30 giây)
- Không chào hỏi dài dòng, không mở đầu bằng *"Hôm nay tôi sẽ trình bày về..."*.
- Mở bằng một tuyên bố mạnh, nghịch lý, tình huống hài hước hoặc câu hỏi khiến người nghe tò mò (tạo ít nhất **2 câu hỏi ngầm**).
- Nhịp chuyển nhanh giữa 1–2 slide đầu (ví dụ: Slide 1 nêu nghịch lý/bối cảnh → Slide 2 đảo ngược kỳ vọng bằng nền đỏ/tối hoặc 2 hình đối lập).

### Phần B — Các phần nội dung (Gồm nhiều slide nối tiếp)
- Chia thành các phần theo logic chủ đề (không chia vụn).
- Mỗi phần bắt đầu bằng **1 câu tạo bối cảnh** trước khi phân tích, rồi triển khai qua chuỗi slide (kết hợp linh hoạt 4 kiểu bố cục: slide 2–3 hình có caption ngắn, slide câu khẳng định, slide motion graphics/sơ đồ).
- Mỗi phần có ít nhất **1 điểm giữ chân giải trí** (ví von đời thường, sarcasm nhẹ, meme đúng timing — mô tả rõ meme/cảm xúc nếu chèn làm hình trên slide).

### Phần C — Kết luận & 4 Câu hỏi cuối
- **Slide kết:** Tóm insight chính bằng một câu payoff sắc (đảo ngược lại nhận định ban đầu hoặc chốt góc nhìn thực tế; dùng nền xanh nếu chốt giải pháp/tích cực, nền tối/đỏ nếu cảnh báo).
- **4 câu hỏi cho khán giả** (liên quan trực tiếp Phần 1, Phần 2, Phần 3 và một góc nhìn tranh luận toàn bài — tuyệt đối không hỏi nội dung chưa xuất hiện trong bài). Kèm câu CTA ngắn tự nhiên nếu phù hợp.

---

## 5. Nhịp Lời nói & Tag chỉ dẫn Slide

Thay vì đếm beat cắt cảnh 1–3s như video YouTube, kịch bản slide căn theo **từng slide và thời lượng nói dự kiến** (ước lượng theo tốc độ nói tự nhiên ~**130–150 từ/phút**).

Gắn tag chỉ dẫn **trực tiếp trong lời nói** đúng thời điểm người nói chỉ vào hình hoặc bấm chuyển hiệu ứng/slide, dùng định dạng **bôi đậm trong ngoặc vuông có dấu cách phía trước**: ` **[...]**`

- Chỉ vào hình sẵn có: ` **[Chỉ Hình 1: ...]**`
- Bấm hiện hình tiếp theo / chuyển ý: ` **[Click — Hiện Hình 2: ...]**`
- Chuyển sang slide mới / đổi màu cảm xúc: ` **[Chuyển Slide — Nền đỏ, gạch bỏ chữ: ...]**`
- Chạy bước sơ đồ/motion graphics: ` **[Anim Bước 2: ...]**`

---

## 6. Định dạng Output bắt buộc

```markdown
# TÊN BÀI TRÌNH BÀY / VIDEO SLIDE

## TỔNG QUAN
- **Chủ đề:**
- **Đối tượng khán giả:**
- **Tổng thời lượng dự kiến:** (ví dụ: 5 phút · ~700 từ · 10 slides)
- **Tone:**
- **Style mặc định:** Nền trắng, chữ đen, font Bahnschrift (đỏ/tối + gạch bỏ cho phủ định/xấu; xanh cho tích cực/giải pháp)

---

### Slide 1 — [Tên/Vai trò slide] (~15s)
- **Bố cục:** [1 trong 4 kiểu: Câu khẳng định / Tiêu đề + 1–3 hình / Motion Graphics / Demo]
- **Màu sắc:** [Trắng mặc định / Đỏ (+ gạch bỏ) / Tối / Xanh]
- **Hiển thị trên slide:**
  - **Tiêu đề (nếu có):** `**[Chỉ 1 tiêu đề in đậm duy nhất]**` *(hoặc Ghi "Không tiêu đề — Chỉ câu khẳng định: ...")*
  - **Visual & Caption dưới hình:**
    1. `[Hình 1: mô tả cụ thể ảnh/meme/screenshot/motion graphics]` — *Caption dưới hình:* `...`
    2. `[Hình 2 (nếu có): ...]` — *Caption dưới hình:* `...`
    3. `[Hình 3 (nếu có): ...]` — *Caption dưới hình:* `...`
- **Lời nói:**
  "[Lời thoại tự nhiên bám công thức đảo ngược ngữ nghĩa, gắn tag ` **[...]**` đúng thời điểm nói tới từng hình hoặc bấm chuyển.]"

---

*(Lặp lại cho Slide 2..N)*

---

## 4 CÂU HỎI CHO KHÁN GIẢ
1. (Liên quan đến Phần 1)
2. (Liên quan đến Phần 2)
3. (Liên quan đến Phần 3)
4. (Liên quan đến toàn bộ chủ đề hoặc góc nhìn gây tranh luận)
```

---

## 7. Checklist chất lượng trước khi xuất

- [ ] **Không tường chữ trên slide:** Slide chỉ có tối đa 1 tiêu đề in đậm ở trên + 1–3 hình kèm caption cực ngắn (2–8 từ) ở dưới, HOẶC chỉ 1 câu khẳng định, HOẶC chỉ motion graphics/sơ đồ.
- [ ] **Đúng quy tắc màu sắc:** Mặc định trắng chữ đen font `Bahnschrift`; phủ định/ý nghĩa xấu dùng đỏ (kèm gạch bỏ nếu hợp) hoặc màu tối; tích cực/giải pháp dùng màu xanh.
- [ ] **Đúng chất kể chuyện:** Có Hook mở đầu, đảo ngược ngữ nghĩa có chiều sâu, ví von/hài hước đúng lúc, không bịa số liệu/tính năng.
- [ ] **Khớp nhịp nói & slide:** Tag ` **[...]**` nằm đúng câu nói tới hình/slide đó; thời lượng ước lượng khớp tổng thời gian bài trình bày.
- [ ] **Đủ 4 câu hỏi cuối** bám sát nội dung đã trình bày.

---

## 8. Vòng lặp tự kiểm tra khớp ngữ nghĩa ảnh–slide (BẮT BUỘC khi xuất `.pptx`)

Trước khi giao file `.pptx` cho người dùng, **BẮT BUỘC chạy vòng lặp kiểm tra trực quan**:
1. **Xuất bảng đối chiếu (Audit Sheet):** Ghép ảnh thật đã crop/fit của từng slide kèm **Tiêu đề + Caption dưới ảnh** thành ảnh kiểm tra rồi mở xem trực tiếp.
2. **Kiểm từng hình theo 3 tiêu chí (không được tự lờ đi):**
   - *Độ khớp trực tiếp:* Che caption đi, nhìn ảnh có hiểu ngay khái niệm đang nói không? (Ví dụ: nói *"chatbot CLI"* phải thấy cửa sổ terminal có hội thoại chatbot; nói *"bàn trên con mèo"* phải thấy rõ cả cái bàn lẫn con mèo; nói *"hallucination"* nên dùng screenshot AI trả lời sai tự tin hoặc meme đúng ngữ cảnh).
   - *Cấm ảnh stock chung chung:* Loại bỏ ngay ảnh cà phê/laptop, bắt tay, tòa nhà, tiền sai đơn vị nếu không thể hiện đúng thực thể trong caption.
   - *Độ rõ vật thể:* Ảnh không bị tối, không bị crop mất vật thể chính.
3. **Sửa & kiểm lại (Loop):** Thay mọi ảnh trượt tiêu chí bằng ảnh tìm mới trên mạng (hoặc biểu đồ/screenshot thật), build lại `.pptx`, xuất lại Audit Sheet và nhìn lại lần nữa cho đến khi **100% slide đạt**.
