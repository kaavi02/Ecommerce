# KavyNest – Django E-Commerce Website
<!-- Deployed on Vercel with Aiven MySQL -->
A modern, responsive e-commerce web platform built with Python & Django. **KavyNest** caters to multi-category online retail, featuring traditional ethnic wear (such as Kasavu sarees and Kurtha sets), jewellery, footwear, and beauty essentials.

---

## 📌 Project Features

* **User Authentication & Authorization:** Secure registration, login, session persistence, and custom logout workflows.
* **Product Catalog & Dynamic Search:** Home page grid with real-time keyword search and category filters.
* **Shopping Cart Subsystem:** Dynamic item additions, quantity adjustments, and live subtotal calculations.
* **Wishlist Tracking:** Bookmark favorite items for quick access and future purchases.
* **Checkout & Order Processing:** Collects shipping details, supports-COD and simulated online payment, and generates instant order summaries.
* **Admin Control Panel:** Fully functional Django `/admin/` suite for CRUD operations on products, categories, and customer orders.

---

## 🛠️ Technology Stack

| Component | Technologies Used |
| :--- | :--- |
| **Backend** | Python 3.10+, Django 4.x / 5.x (MVT Architecture) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Bootstrap 5, FontAwesome 6 |
| **Database** | MySQL 8.0 (MySQL Workbench) / SQLite 3 |
| **Tools & IDE** | Visual Studio Code, Git, GitHub |

---

## ⚙️ Code Architecture & Flow

The project follows Django's **Model-View-Template (MVT)** design pattern:

```text
[ Browser / HTTP Request ][cite: 1, 2]
           │
           ▼
    [ urls.py ] ────────► Routes URL patterns[cite: 1, 2]
           │
           ▼
   [ views.py ] ◄──────► [ models.py ] ◄──────► [ MySQL Database ][cite: 1, 2]
 (Business Logic)         (Data ORM)           (Persistent Storage)[cite: 1, 2]
           │
           ▼
[ templates/*.html ] ───► Renders output (Extends base.html)[cite: 1, 2]
