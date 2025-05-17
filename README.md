# 🏟️ Turf Booking System

A Django-based web application for booking sports turfs. Players can register, select time slots, make demo payments, and give feedback. Turf owners can manage bookings. The project includes a machine learning model that predicts sentiment (positive/negative) from feedback.

---

## ✅ Features
- Player & Turf Owner registration/login
- Turf slot booking
- Demo payment system
- Feedback system with ML sentiment analysis
- Admin panel for control and management

---

## ⚙️ Technologies Used
- **Backend:** Python, Django
- **Database:** SQLite
- **ML:** Scikit-learn (TF-IDF + SVM)
- **Frontend (optional):** Bootstrap

---

## 🚀 How to Run This Project

```bash
# Clone the repo
git clone https://github.com/Karma022p/turf-booking-system.git
cd turf-booking-system

# Install dependencies
pip install -r requirements.txt

# Run the server
python manage.py runserver
