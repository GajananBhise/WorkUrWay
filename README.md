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
* Admin only access to manage menu items at the particular cafe, adding menu items to the database.

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
CafeandWifi/
│
├── .env                       # Environment variables
├── .gitignore                # Git ignore file
├── Procfile                  # For deployment on Render or Heroku
├── README.md                 # Project description and documentation
├── requirements.txt          # List of Python dependencies
│
├── main.py                   # Main Flask application
├── forms.py                  # Flask-WTF form definitions
│
├── instance/
│   └── cafes.db              # SQLite database (local development)
│
├── static/
│   └── images/               # Static image assets
│       ├── bg.jpg
│       ├── cafe_logo.jpg
│       ├── chair.png
│       ├── chair1.png
│       ├── location_icon.png
│       └── sanitary.png
│
├── templates/                # HTML templates (Jinja2)
│   ├── add.html
│   ├── add_menu_item_to_database.html
│   ├── cafe_cards.html
│   ├── check_out.html
│   ├── confirm_order.html
│   ├── footer.html
│   ├── header.html
│   ├── index.html
│   ├── login.html
│   ├── manage_menu_at_cafe.html
│   ├── menu.html
│   ├── register.html
│   ├── search.html
│   ├── show_cafe.html
│   └── update_price.html


## Checkout live website
https://workurway.onrender.com/

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
