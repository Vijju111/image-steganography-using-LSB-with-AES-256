# Image Steganography Web App

This project is a web application that allows users to securely hide and retrieve confidential messages within images using advanced AES-256 encryption and LSB (Least Significant Bit) steganography techniques.

## Features

- **User Authentication:** Register and login with secure password hashing.
- **Message Embedding:** Encrypt and embed secret messages into images.
- **Message Extraction:** Extract and decrypt hidden messages from stego images.
- **Capacity Check:** See how much data can be hidden in a selected image.
- **Modern UI:** Responsive frontend with clear instructions.

## Tech Stack

- **Backend:** Python, Flask, Flask-Bcrypt, Pillow, NumPy, PyCryptodome, SQLite
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

```
backend/
    app.py          # Main Flask app
    auth.py         # User authentication logic
    stegano.py      # Steganography and encryption logic
frontend/
    templates/      # HTML templates
    static/         # CSS, JS, images
database.db         # SQLite database
requirements.txt    # Python dependencies
```

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd image-steg-project2
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv myenv
   myenv\Scripts\activate   # On Windows
   # or
   source myenv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```sh
   python backend/app.py
   ```

5. **Access the app:**
   Open your browser and go to [http://localhost:5000](http://localhost:5000)

## Usage

- **Register:** Create a new account.
- **Login:** Access the home page.
- **Embed Message:** Upload an image, enter your secret message and password, and download the stego image.
- **Extract Message:** Upload a stego image and enter the password to reveal the hidden message.

## Security Notes

- Messages are encrypted with AES-256 before embedding.
- Passwords are hashed using bcrypt.
- Only image files (PNG, JPEG, BMP) are accepted.

## License

This project is for educational purposes.

---

**Developed by:** GARIDEPALLI VIJAY
