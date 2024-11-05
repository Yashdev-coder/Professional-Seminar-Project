import qrcode
import os

def generate_qr_code(data, file_name='qr_code.png', save_directory='qr_codes'):
    """
    Generates a QR Code with the given data and saves it as an image.

    Parameters:
        data (str): The data to be embedded in the QR code.
        file_name (str): The name of the output QR code image file (default: 'qr_code.png').
        save_directory (str): The directory where the QR code image will be saved (default: 'qr_codes').

    Returns:
        str: The path to the saved QR code image.
    """
    # Create the directory if it does not exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Generate the QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Define the file path
    file_path = os.path.join(save_directory, file_name)

    # Save the image
    img.save(file_path)

    return file_path

if __name__ == "__main__":
    # Example usage
    sample_data = "https://example.com/attendance?id=12345"
    qr_path = generate_qr_code(sample_data, file_name='attendance_qr.png')
    print(f"QR code generated and saved at: {qr_path}")
