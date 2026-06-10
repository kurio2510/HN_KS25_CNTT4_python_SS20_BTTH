import logging

logging.basicConfig(
    filename="arena_tickets.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ticket_db =[
    {
        "ticket_id": "T01",
        "buyer_name": "Nguyen Van A",
        "price": 500.0,
        "status": "Booked",
        "seat": ("A", 1)
    },
    {
        "ticket_id": "T02",
        "buyer_name": "Tran Thi B",
        "price": 300.0,
        "status": "Cancelled",
        "seat": ("B", 5)
    },
    {
        "ticket_id": "T03",
        "buyer_name": "Le Van C",
        "price": 500.0,
        "status": "Booked",
        "seat": ("A", 2)
    }
]

def calculate_total_revenue(ticket_list):
    total = 0.0
    for ticket in ticket_list:
        if ticket.get("status") == "Booked":
            total += ticket.get("price", 0)
    return total

def display_tickets(tickets):
    if not tickets:
        print("Hiện chưa có vé nào trong hệ thống.")
        return
    print("\n--- DANH SÁCH VÉ ---")
    print("Mã Vé | Tên Khách Hàng      | Giá Vé | Chỗ Ngồi | Trạng Thái")
    print("-" * 60)
    for ticket in tickets:
        try:
            seat = ticket["seat"]

            status = ticket["status"]
            if status == "Cancelled":
                status += " [ĐÃ HỦY]"
            print(
                f"{ticket['ticket_id']:<6} | "
                f"{ticket['buyer_name']:<20} | "
                f"{ticket['price']:<6} | "
                f"{seat[0]}-{seat[1]:<6} | "
                f"{status}"
            )
        except KeyError as e:
            print("Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
            logging.error(f"Missing key while displaying ticket: {e}")
    print("-" * 60)
    logging.info("User viewed ticket list.")

def book_ticket(tickets):
    print("\n--- ĐẶT VÉ MỚI ---")

    ticket_id = input("Nhập mã vé: ").strip()
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            print(f"Lỗi: Mã vé {ticket_id} đã tồn tại.")
            logging.warning(f"Duplicate ticket ID entered: {ticket_id}")
            return
    buyer_name = input("Nhập tên khách hàng: ").strip()
    while True:
        try:
            price = float(input("Nhập giá vé: "))
            if price <= 0:
                print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Giá vé phải là số. Vui lòng nhập lại.")
            logging.warning("Invalid price input while booking ticket")
    area = input("Nhập khu vực ghế: ").upper()
    while True:
        try:
            seat_number = int(input("Nhập số ghế: "))
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")
    new_ticket = {
        "ticket_id": ticket_id,
        "buyer_name": buyer_name,
        "price": price,
        "status": "Booked",
        "seat": (area, seat_number)
    }
    tickets.append(new_ticket)
    print(
        f"\nThành công: Đã đặt vé {ticket_id} cho khách hàng {buyer_name}."
    )
    logging.info(
        f"Booked new ticket {ticket_id} for {buyer_name}"
    )

def change_seat(tickets):
    print("\n--- ĐỔI CHỖ NGỒI ---")
    ticket_id = input("Nhập mã vé cần đổi chỗ: ").strip()
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            new_area = input("Nhập khu vực ghế mới: ").upper()
            while True:
                try:
                    new_seat = int(input("Nhập số ghế mới: "))
                    break
                except ValueError:
                    print("Số ghế phải là số nguyên. Vui lòng nhập lại.")
            ticket["seat"] = (new_area, new_seat)
            print(
                f"\nThành công: Đã đổi chỗ vé {ticket_id} sang {new_area}-{new_seat}."
            )
            logging.info(
                f"Seat changed for ticket {ticket_id} to {new_area}-{new_seat}"
            )
            return
    print(f"\nKhông tìm thấy vé mang mã {ticket_id}.")
    logging.warning(
        f"Change seat failed - Ticket {ticket_id} not found"
    )

def cancel_ticket(tickets):
    print("\n--- HỦY VÉ ---")
    ticket_id = input("Nhập mã vé cần hủy: ").strip()
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            if ticket["status"] == "Cancelled":
                print(
                    f"\nVé {ticket_id} đã ở trạng thái Cancelled trước đó."
                )
                return
            ticket["status"] = "Cancelled"
            print(f"\nThành công: Vé {ticket_id} đã được hủy.")
            logging.warning(
                f"Ticket {ticket_id} has been cancelled."
            )
            return
    print(f"\nKhông tìm thấy vé mang mã {ticket_id}.")
    logging.warning(
        f"Cancel ticket failed - Ticket {ticket_id} not found"
    )

def calculate_revenue(tickets):
    print("\n--- BÁO CÁO DOANH THU ---")
    try:
        revenue = 0.0
        booked_count = 0
        cancelled_count = 0
        for ticket in tickets:
            if ticket["status"] == "Booked":
                booked_count += 1
                revenue += ticket["price"]
            elif ticket["status"] == "Cancelled":
                cancelled_count += 1
        print(f"Tổng số vé đã đặt: {booked_count}")
        print(f"Tổng số vé đã hủy: {cancelled_count}")
        print(f"Tổng doanh thu hợp lệ: {revenue}")
        logging.info(
            f"Revenue report generated. Total: {revenue}"
        )
    except KeyError as e:
        print("Lỗi: Một vé đang bị thiếu dữ liệu doanh thu.")
        print("Tổng doanh thu hợp lệ: 0.0")
        logging.error(
            f"Missing key while calculating revenue: {e}"
        )

def show_menu():
    print("\n=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===")
    print("1. Xem danh sách vé đã bán")
    print("2. Đặt vé mới")
    print("3. Đổi chỗ ngồi (Cập nhật vé)")
    print("4. Hủy vé")
    print("5. Báo cáo doanh thu")
    print("6. Thoát chương trình")
    print("========================================")
if __name__ == "__main__":

    while True:
        show_menu()
        choice = input("Chọn chức năng (1-6): ").strip()
        if choice == "1":
            display_tickets(ticket_db)
        elif choice == "2":
            book_ticket(ticket_db)
        elif choice == "3":
            change_seat(ticket_db)
        elif choice == "4":
            cancel_ticket(ticket_db)
        elif choice == "5":
            calculate_revenue(ticket_db)
        elif choice == "6":
            print(
                "\nCảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports."
            )

            logging.info(
                "Ticket management system closed."
            )
            break
        else:
            print("Lựa chọn không hợp lệ.")
