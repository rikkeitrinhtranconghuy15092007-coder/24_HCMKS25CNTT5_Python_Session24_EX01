# Hệ thống quản lý hóa đơn Rikkei Coffee - Đã bảo mật và đồng bộ
class CoffeeOrder:
    # Thuộc tính của lớp (Class Attribute)
    __vat_rate = 0.10  # Để private để tránh việc chỉnh sửa trực tiếp bên ngoài

    def __init__(self, table_number):
        self.table_number = table_number
        # Khắc phục lỗ hổng 1: Sử dụng __ để kích hoạt Name Mangling (Private attribute)
        self.__total_amount = 0  

    # Phương thức thêm tiền món ăn vào hóa đơn
    def add_item(self, price):
        if price > 0:
            self.__total_amount += price

    # Khắc phục lỗ hổng 1: Tạo thuộc tính chỉ đọc (Getter) cho tổng tiền ban đầu
    @property
    def total_amount(self):
        return self.__total_amount

    # Getter để bên ngoài có thể xem mức thuế hiện tại thông qua instance hoặc class
    @property
    def vat_rate(self):
        return CoffeeOrder.__vat_rate

    # Tính tổng tiền khách phải trả (đã cộng VAT)
    def calculate_final_bill(self):
        return self.__total_amount + (self.__total_amount * CoffeeOrder.__vat_rate)

    # Khắc phục lỗ hổng 2: Sử dụng Class Method để cập nhật thuộc tính Class chung
    @classmethod
    def update_vat_rate(cls, new_rate):
        if 0 <= new_rate <= 1:
            cls.__vat_rate = new_rate


# --- KỊCH BẢN KIỂM CHỨNG & CHỐNG TẤN CÔNG ---

# Khách vào quán, hệ thống mở hóa đơn cho 2 bàn
order_table1 = CoffeeOrder("Bàn 1")
order_table2 = CoffeeOrder("Bàn 2")

# Khách gọi món
order_table1.add_item(50000)  # Bàn 1 gọi Cà phê sữa (50k)
order_table2.add_item(30000)  # Bàn 2 gọi Trà đào (30k)

print("--- Thử nghiệm hành vi gian lận và cập nhật thuế ---")

# 1. Nhân viên cố tình gian lận tự gán đè tổng tiền của Bàn 1 về 0
try:
    order_table1.total_amount = 0  # Dòng này sẽ gây lỗi vì property không có setter
except AttributeError as e:
    print(f"[BẢO MẬT]: Ngăn chặn hành vi can thiệp hóa đơn trái phép! Lỗi: {e}")

# Kiếm chứng việc đổi tên biến riêng tư (Mặc dù gán trực tiếp thuộc tính động, biến thật vẫn an toàn)
order_table1.__total_amount = 0  # Python sẽ hiểu là tạo ra 1 biến dynamic mới, không ảnh hưởng tới biến private thực sự bên trong

# 2. Quản lý chi nhánh cập nhật thuế VAT xuống 8% (0.08) cho TOÀN HỆ THỐNG bằng Class Method
CoffeeOrder.update_vat_rate(0.08)

print("\n--- KẾT QUẢ ĐẦU RA HỆ THỐNG ---")
print(f"Tổng tiền Bàn 1 gốc (Chưa VAT): {order_table1.total_amount} VNĐ (Không bị sửa về 0)")
print(f"Tổng tiền Bàn 1 phải trả (sau VAT 8%): {order_table1.calculate_final_bill()} VNĐ")
print(f"Thuế VAT đang áp dụng cho Bàn 1: {order_table1.vat_rate * 100}%")
print(f"Thuế VAT đang áp dụng cho Bàn 2: {order_table2.vat_rate * 100}%")