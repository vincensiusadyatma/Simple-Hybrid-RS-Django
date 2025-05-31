# 🔍 Hybrid Recommendation System Schemes

This project implements **three recommendation system schemes** tailored to the **user status** within the application. Each recommendation type adapts to the availability of user data, ensuring relevant and personalized suggestions.

## ✅ Recommendation System Schemes Based on User Status

| User Status                          | Recommendation Method                    | Description                                                                 |
|-------------------------------------|------------------------------------------|-----------------------------------------------------------------------------|
| 🔹 1. First-Time Visitor (No Login, No Data)   | Rating-Based Filtering (Popularity-Based)    | Recommends items with high average ratings or popularity across all users. Ideal for first-time visitors without any personal or interaction data. |
| 🔹 2. Not Logged In                 | Demographic Filtering                    | Recommendations based on general user categories like location. |
| 🔹 3. Logged In (Only Personal Data) | Content-Based Filtering                  | Uses user's personal preferences such as budget range, preferred hotel types, and desired facilities. |
| 🔹 4. Logged In (With History)       | Collaborative Filtering / Hybrid Filtering | Suggests options based on users with similar behaviors, ratings, or booking histories. Combines content and collaborative methods for improved accuracy. |

---

## 📌 Key Concepts

- **Demographic Filtering**: Simulates group-level preferences when individual data is not available.
- **Content-Based Filtering**: Analyzes user’s profile and preferred attributes to recommend similar items.
- **Collaborative Filtering**: Leverages community data — users with similar tastes — for generating suggestions.
- **Hybrid Filtering**: Combines multiple filtering methods for optimal recommendations.

---

## 🛠 Technologies Used

- Language : Python
- Database: SQL Lite
- Framework: Django

---





