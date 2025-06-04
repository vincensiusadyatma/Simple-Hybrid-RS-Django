# Hybrid Recommendation System Schemes

This project implements **three recommendation system schemes** tailored to the **user status** within the application. Each recommendation type adapts to the availability of user data, ensuring relevant and personalized suggestions.

## Recommendation System Schemes Based on User Status

| User Status                          | Recommendation Method                    | Description                                                                 |
|-------------------------------------|------------------------------------------|-----------------------------------------------------------------------------|
| 🔹 1. First-Time Visitor (No Login, No Data)   | Rating-Based Filtering (Popularity-Based)    | Recommends items with high average ratings or popularity across all users. Ideal for first-time visitors without any personal or interaction data. |
| 🔹 2. Logged In (Only Personal Data) | Content-Based Filtering                  | Uses user's personal preferences such as budget range, preferred hotel types, and desired facilities. |
| 🔹 3. Logged In (With History)       | Collaborative Filtering / Hybrid Filtering | Suggests options based on users with similar behaviors, ratings, or booking histories. Combines content and collaborative methods for improved accuracy. |

---

##  Key Concepts

- **Demographic Filtering**: Simulates group-level preferences when individual data is not available.
- **Content-Based Filtering**: Analyzes user’s profile and preferred attributes to recommend similar items.
- **Collaborative Filtering**: Leverages community data — users with similar tastes — for generating suggestions.
- **Hybrid Filtering**: Combines multiple filtering methods for optimal recommendations.

---

## Technologies Used

- Language : Python
- Database: SQL Lite
- Framework: Django


## How To Use

1. **Kloning Repositori**
   ```bash
   
   https://github.com/vincensiusadyatma/Simple-Hybrid-RS-Django.git
   
2. **Create Virtual ENV**
   ```bash
   python -m venv venv

3. **Activate the virtual env (gitbash)**
   ```bash
   source venv/Scripts/activate
   
4. **Activate the virtual env (cmd)**
   ```bash
   venv/Scripts/activate.bat

5. **Install the requirements**
   ```bash
   pip install -r requirements.txt

5. **Change Directory Project**
   ```bash
   cd hybrid_rs_project

5. **Database SQL Lite Migrations**
   ```bash
   python manage.py migrate

5. **Run Seeder**
   ```bash
   python manage.py seed_all
   
5. **Run API**
   ```bash
   python manage.py runserver



---





