# Công cụ giải quyết Toán Rời Rạc #
Website hỗ trợ giải các bài toán rời rạc: logic mệnh đề, ánh xạ, quan hệ, đại số Boolean...
## Giới thiệu
Đây là một ứng dụng web được xây dựng nhằm hỗ trợ sinh viên học môn Toán rời rạc.
Website cung cấp các công cụ tính toán và kiểm tra tự động cho nhiều dạng bài thường gặp.
## Tính năng chính
1. Logic cơ bản
- Tạo bảng chân trị
- Kiểm tra hằng đúng, sai
- So sách hai vế
2. Phương pháp đếm
- Kiểm tra đơn ánh
- Kiểm tra song ánh
- Kiểm tra toàn ánh
- Ánh xạ ngược
- Định lí chuồng chim bồ câu
3. Quan hệ
- Cộng, trừ Modulo
- Nhân đồng dư Modulo
- Mũ đồng dư Modulo
- Kiểm tra các tính chất của quan hệ
- Vẽ biểu đồ Hasse
4. Đại số Boolean
- Tính đại số boolean
- Kiểm tra các tính chất của đại số boolean
- Kiểm tra dàn bù phân phối
- Lấy danh sách nguyên tử
- Lấy tự tối thiểu
- Lấy tự tối đại
- Rút gọn biểu thức boolean
- Vẽ biểu đồ Karnaugh
# Công nghê sử dụng
- Ngôn ngữ lập trình: Python 3
- Framework: Django
- Html/css
- Deployment: Render
- Cơ sở dữ liệu: Postgres
# Cấu trúc thư mục
discrete_structure.github.io/
|──counting/ # Phương pháp đếm và định lí chuồng chim bồ câu
|──logic/ # Logic mệnh đề & đại số Boolean
|──relation/ # Quan hệ & ánh xạ
|──static/
|──discrete_structure/
| |──asgi.py
| |──settings.py
| |──urls.py
| |──wsgi.py
|──templates/
|──ultis/
|──manage.py
# Chạy dự án ở local

đường dẫn đến trang web: https://discrete-structure-github-io.onrender.com
