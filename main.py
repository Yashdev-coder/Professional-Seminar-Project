import qrcode
import sqlite3
import datetime
import cv2
from pyzbar.pyzbar import decode

# Database Setup
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                student_id TEXT,
                student_name TEXT,
                timestamp TEXT
            )''')
conn.commit()

# Generate QR Code
def generate_qr_code(student_id, student_name):
    data = f"{student_id},{student_name}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{student_id}_qr.png")
    print(f"QR Code generated for {student_name} with ID {student_id}")

# Scan QR Code
def scan_qr_code():
    cap = cv2.VideoCapture(0)
    print("Scanning for QR codes. Press 'q' to quit.")
    while True:
        success, frame = cap.read()
        if success:
            for barcode in decode(frame):
                data = barcode.data.decode('utf-8')
                student_id, student_name = data.split(',')
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Insert into the database
                c.execute("INSERT INTO attendance (student_id, student_name, timestamp) VALUES (?, ?, ?)",
                          (student_id, student_name, timestamp))
                conn.commit()
                print(f"Attendance marked for {student_name} (ID: {student_id}) at {timestamp}")

            cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Main Menu
def main():
    while True:
        print("\nQR Code Attendance System")
        print("1. Generate QR Code for Student")
        print("2. Scan QR Code for Attendance")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            student_id = input("Enter Student ID: ")
            student_name = input("Enter Student Name: ")
            generate_qr_code(student_id, student_name)
        elif choice == '2':
            scan_qr_code()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
