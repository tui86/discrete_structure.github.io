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
## Công nghê sử dụng
- Ngôn ngữ lập trình: Python 3
- Framework: Django
- Html/css
- Deployment: Render
- Cơ sở dữ liệu: Postgres
## Cấu trúc thư mục
```
discrete_structure.github.io/
├── counting/              # Phương pháp đếm & định lí chuồng chim bồ câu
├── logic/                 # Logic mệnh đề & đại số Boolean
├── relation/              # Quan hệ & ánh xạ
├── static/
├── templates/
├── utils/
├── discrete_structure/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```
## Cách chạy project ở local
1. Clone repository
2. Tạo virtual environment
3. Cài đặt thư viện
4. Chạy migrate
5. Run server
## Deploy
Project được deploy trên Render sử dụng Gunicorn và WhiteNoise để phục vụ static files.
đường dẫn đến trang web: https://discrete-structure-github-io.onrender.com
## Cách sử dụng
1. Truy cập trang chủ theo đường dẫn
2. Chọn chức năng cần sử dụng
3. Nhập dữ liệu theo hướng dẫn
4. Nhấn submit để xem kết quả
## Khác
Mỗi chức năng đều được ghi nhận số lần người dùng sử dụng thông qua decorator và database.
Dữ liệu này có thể dùng để thống kê mức độ phổ biến của các chức năng.
Có thể xem dữ liệu này thông qua trang admin.
đường dẫn file dữ liệu thuật toán của chương trình: https://github.com/tui86/discrete_structure
## Hướng phát triển
- Cải thiện giao diện người dùng
- Thêm đăng nhập để lưu lịch sử
- Xuất kết quả dưới dạng file
- Hỗ trợ thêm bài toán nâng cao
