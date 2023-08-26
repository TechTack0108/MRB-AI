from autocorrect import Speller
from langdetect import detect

extracted_text = """
Đính kèm thư của HGU trả lời đề xuất phụ lục sửa đổi bổ sung hợp đồng

niếp cận và sở hữu bất cứ phần Công trường nào mang thời hạn nêu tại Tiến độ bàn
giao từng phần và Bản vẽ bàn giao từng phần.”
Trong Tiếu khoản 8.7(d), cụm từ “Ngày khởi công” trong cột “Ngày quan trọng” sẽ

; được thay thế bởi cụm từ “Ngày tiếp cận toàn bộ công trường”.

° Thứ hai: Có thể chấp nhận = đổi nếu HGU có thể chứng minh
rằng Thời gian Hoan thành (khong phải chậm trễ trong một công việc cụ
thé mà Thời gian cho Hoàn thành tổng thé) đã chậm do chậm trễ trong
Mốc Ngày từ việc bàn giao muộn của Chủ đầu tư. Phần này cuối cùng sẽ
chuyển đến và được giải quyết ở mục 8.7 và 20.1.

Kết luận: Không thay đổi tiêu đề cột. Lưu ý rang việc bàn giao công trường
muộn không ảnh hưởng đến mốc ngày thiết kế do HGU thực hiện sau Ngày
khởi công — _

_ĐIỀU3, BỒI THƯỜNG

_ ĐIỀU: 3. Cy THƯỜNG C GHI Pui

i 3.1. | Chỉ phí cho Ngày khởi ông † bị chậm trễ

3.1.1 Các bên thống nhất rằng Ngày khởi công là ngày 06/02/2017 và Nhà thầu có
quyền nhận toàn bộ tổn thất, chi phí và mọi khoản phí tổn khác phát sinh trong thời
gian từ ngày sau ngay ký kết Thỏa thuận hợp đồng (nghĩa là ngày 01/11/2015) cho đến
! Ngày khởi công bị chậm trễ ("Chi phí cho Ngày khởi công bị chậm trễ").

3.1.2 Tổng Chi phí cho Ngày khởi công bị chậm trễ USD 3.831.359, Euro 281.647 và
VND 3.668.452.317 và Chủ đầu tư phải trả khoản chỉ phí này cho Nhà thầu trong vòng
90 ngày sau khi ký kết Hợp đồng sửa đổi, bổ sung số 01.

Đề xuất bị từ chối..

3.1. Sau tháng 11/2015 đến Ngày khởi công, trừ khi Chủ đầu tư yêu cầu rõ
ràng, Chủ đầu tư không có nghĩa vụ phải hỗ trợ bất kỳ chỉ phí nào phát sinh
bởi Liên danh, nhà thầu đã chọn ở lại Hà Nội đến Ngày khởi công.

HGU lẽ ra đã có thể khiếu nại về tình trạng này trong vòng 180 ngày (GCC
8.1)

3.2. Về chỉ phí: Nhà thầu không cung cấp bất kỳ phân tích chỉ tiết giá trị yêu
cầu trong đính kèm của thư này và phụ lục sửa đối bd sung hợp đồng, do đó,
không thể phân tích để xem xét thêm.

Chỉ có thé xem xét chỉ phí dựa trên giải trình chỉ tiết xác nhận về bất kỳ yêu
cầu cụ thé nào của Chủ đầu tư về huy động trước Ngày khởi công, dẫn đến
phát sinh một số chi phí.

¡ 3.2. Chỉ phí cho Thời gian hoàn thành điều chỉnh

| 3.2.1 Các bên thống nhất rằng Nhà thầu có quyền nhận toàn bộ tốn thất, chi phí và

mọi khoản phí tổn khác và lợi nhuận phát sinh từ việc gia hạn 11,5 tháng từ Ngày khởi
công cho đến Thời gian hoàn thành điều chỉnh theo Khoản 2.2 của Hợp đồng sửa đổi,

bổ sung số 01 ("Chi phí cho Thời gian hoàn thành điều chỉnh").

Đề xuất bị từ chối.

Cần xác định chi phí phát sinh dựa trên phân tích chi phí cụ thể cần đệ trình
và trên cơ sở hợp đồng được sử dụng để xác định khối lượng phát sinh cần
thiết.

Ví dụ, có thể xem xét điều chỉnh hạng mục “Huy động”. Nhà thầu có trách
nhiệm trình bày rõ ràng yêu cầu và cung cấp chứng cứ.


"""

# detect the language of the text
lang = detect(extracted_text)

spell = Speller(only_replacements=False, lang=lang)

print(spell(extracted_text))
