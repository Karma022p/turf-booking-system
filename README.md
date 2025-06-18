# 🏟️ Turf Booking System

A full-stack Django web application that allows players to book sports turfs, connect with other players, and give feedback — enhanced with machine learning sentiment analysis.

---

## 🚀 Project Overview

This project aims to simplify the process of sports turf booking through a centralized platform that connects players, turf owners, and admins. The system also uses machine learning to analyze user feedback and improve service quality.

---

## 🔑 Key Features

- 🧍‍♂️ **User Roles:** Player, Turf Owner, and Admin
- 🕒 **Slot Booking:** Book and manage turf slots with date/time selection
- 💳 **Demo Payment System:** Simulated payment workflow
- 💬 **Chatbot:** Handles booking-related queries using ML
- 🤖 **Sentiment Analysis:** Classifies user feedback as Positive or Negative using TF-IDF + SVM
- 📍 **Location-Based Filtering:** (Using pin-code)
- 📊 **Admin Panel:** Manage users, turfs, and payments
- 📱 **Responsive UI:** Frontend styled with Bootstrap

---

## 🛠️ Tech Stack

| Layer         | Technology Used                 |
|---------------|----------------------------------|
| **Frontend**  | HTML, CSS, Bootstrap             |
| **Backend**   | Python, Django                   |
| **Database**  | SQLite (for dev) → PostgreSQL (for prod) |
| **ML**        | Scikit-learn (TF-IDF, SVM, Random Forest) |
| **Deployment (planned)** | AWS / Heroku             |

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/turf-booking-system.git
cd turf-booking-system

# 2. Create virtual environment (optional)
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Run the server
python manage.py runserver
