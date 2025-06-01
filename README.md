# WorkUrWay

**WorkUrWay** is a Flask-based web application designed to help users discover and manage information about cafes, including amenities like Wi-Fi, power sockets, and more.

## Features

* Browse a list of cafes with details such as location, amenities, seating capacity, and coffee prices.
* Add new cafes to the database through a user-friendly form.
* Edit existing cafe information, including updating coffee prices.
* Responsive design using Bootstrap 5.

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
   ```

5. **Run the application:**

   ```bash
   flask run
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.

## Project Structure

```
WorkUrWay/
├── static/
│   └── images/
├── templates/
│   ├── header.html
│   ├── footer.html
│   ├── index.html
│   ├── search.html
│   └── edit_price.html
├── forms.py
├── main.py
├── requirements.txt
├── Procfile
└── .gitignore
```

## Checkout live website
https://workurway.onrender.com/

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
