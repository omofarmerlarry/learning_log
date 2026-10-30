# 📚 Learning Log

A full-stack Django web application designed to help users log, organize, and track their learning journeys across various topics and subjects in real time.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-5.0+-green.svg)
![Deployment](https://img.shields.io/badge/deployed%20on-Render-informational.svg)

---

## 🌟 Features

- **User Authentication & Authorization:** Secure user registration, login, and logout mechanics using custom Django forms (email/SMTP integration removed for streamlined local and production setup) ensuring complete user data isolation.
- **Topic & Entry Management:** Full CRUD capability to create custom learning topics and append detailed journal entries with custom inline deletion flows.
- **Markdown & Reading Time Support:** Write and view rich entry contents formatted with Markdown syntax, paired with automatic reading time estimates (in minutes) for each log.
- **Production Ready:** Configured for cloud production environments with secure environment variables and static asset handling via Gunicorn.
- **Responsive UI:** Clean frontend styled using modern template inheritance and Bootstrap components.
---

## 🛠️ Tech Stack

- **Backend:** Python, Django 5.x
- **Frontend:** HTML5, Custom CSS3, Bootstrap 5, Django Template Language (DTL), Markdown
- **Production WSGI Server:** Gunicorn
- **Version Control:** Git, GitHub
- **Hosting & Cloud Deployment:** Render

---

## 🚀 Getting Started Locally

Follow these steps to run the application on your local machine.

### Prerequisites

- Python 3.10+ installed
- Git installed

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/omofarmerlarry/learning_log.git](https://github.com/omofarmerlarry/learning_log.git)
   cd learning_log
