# WorkUrWay

**WorkUrWay** is a Flask-based web application designed to help users discover and manage information about cafes, including amenities like Wi-Fi, power sockets,
and after signup and login users can explore the menu at the cafes, add to cart and order online.


## Features

* Browse a list of cafes with details such as location, amenities, seating capacity, and coffee prices.
* Add new cafes to the database through a user-friendly form.
* Edit existing cafe information, including updating coffee prices.
* Responsive design using Bootstrap 5.
* User registration and login.
* Menu items at the cafes.
* Users can add to cart their items and order online.
* Users get order confirmation through Email notification.

## Technologies Used

* Python 3.13
* Flask
* Flask-WTF
* Flask-SQLAlchemy
* SQLite
* Bootstrap 5

## Installation

**1. Clone the repository:**

   ```bash
   git clone https://github.com/GajananBhise/WorkUrWay.git
   cd WorkUrWay
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**

   Create a `.env` file in the root directory and add the following:

   ```env
   FLASK_APP=main.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///cafes.db
   EMAIL=your Email address
   GMAIL_APP_PASSWORD= your gmail app password    
   ```

5. **Run the application:**

   ```bash
   flask run
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.

## Project Structure

```
cafe-order-app/
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── show_cafe.html
│   ├── menu.html
│   ├── add.html
│   ├── update_price.html
│   ├── check_out.html
│   ├── confirm_order.html
│   └── header.html / footer.html
├── forms.py
├── app.py
├── .env
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
