# autufb

Auto Facebook Bot - Công cụ tự động hóa Facebook

## Tính năng dừng an toàn ("dừng đi")

Dự án này đã được cập nhật với tính năng dừng an toàn để có thể dừng quá trình automation một cách graceful.

### Cách dừng automation:

1. **Dừng bằng phím tắt**: Nhấn `Ctrl+C` để dừng ngay lập tức
2. **Dừng bằng file**: Tạo file `stop.txt` trong thư mục gốc để dừng sau khi hoàn thành tác vụ hiện tại

### Cách sử dụng:

```bash
# Chạy automation comment
python main.py

# Chạy automation rời nhóm/bỏ theo dõi  
python leave_groups_unfollow.py

# Để dừng: nhấn Ctrl+C hoặc tạo file stop.txt
touch stop.txt
```

### Cài đặt:

```bash
chmod +x install.sh
./install.sh
```

Automation sẽ tự động dọn dẹp và đóng browser khi dừng.