# 🏨 Travel Booking Application

## 📌 Overview
A simple **travel booking web application** built with **Django** that allows users to:
- 🔹 View available travel options (Flight, Train, Bus)
- 🔹 Book tickets and manage bookings
- 🔹 Register/Login/Logout using Django Authentication
- 🔹 Cancel bookings if needed
- 🔹 Search & filter travel options

---

## 🚀 Features
### ✅ **Backend (Django)**
- **User Authentication**: Register, Login, Logout
- **Profile Management**: Users can update their profile
- **Travel Options**: 
  - Store travel details (Type, Source, Destination, Date & Time, Price, Seats)
- **Booking System**:
  - Users can book, cancel, and view bookings (past & active)
  - Available seats update dynamically
- **Admin Panel**: Manage bookings & users
- **Database**: Uses **MySQL**

### 🎨 **Frontend (Django Templates + Bootstrap)**
- **Mobile Responsive UI**
- **Easy Navigation** with Bootstrap Styling
- **Booking Forms** with Validation
- **Tabbed UI** for Active, Past, and Cancelled Bookings

---

## 🛠️ Setup & Installation (Single Command Execution)
### **1️⃣ Clone the Repository & Set Up the Virtual Environment**
```sh
git clone https://github.com/yourusername/travel-booking.git && cd travel-booking
python3 -m venv venv && source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py createsuperuser
python3 manage.py runserver
