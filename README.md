

---

# Simple Python Projects in Streamlit

This repository contains a collection of simple Python projects built with **Streamlit**. All projects are included in a single `main.py` file, providing a variety of interactive web applications to showcase different functionalities.

---

## Projects

### 1. **To-Do List App**
- A simple to-do list application where users can add, delete, and view tasks.
- The app allows users to maintain a personal task list with basic CRUD operations.

### 2. **BMI Calculator**
- A body mass index (BMI) calculator where users can input their weight and height, and get their BMI along with an interpretation of the result (underweight, normal, overweight, etc.).

### 3. **Simple Weather App**
- A basic weather app that allows users to enter a city and get the current weather data, including temperature, humidity, and weather condition.
- Uses a free weather API for data retrieval.

### 4. **Random Joke Generator**
- A fun app that fetches and displays random jokes from a joke API.
- The app can be used to get a quick laugh with just a click.

### 5. **Currency Converter**
- A simple currency converter that allows users to convert between different currencies using real-time exchange rates.

---

## Technologies Used

- **Streamlit**: Framework for building interactive web apps.
- **Requests**: For fetching data from external APIs (e.g., weather, currency rates).
- **Python**: Backend logic for all applications.

---

## Setup Instructions

### Prerequisites

- Python 3.x
- Streamlit

### Steps to Set Up:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/simple-python-streamlit.git
   cd simple-python-streamlit
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

The app will be available at [http://localhost:8501](http://localhost:8501).

---

## License

MIT License

---
