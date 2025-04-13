# School Class Ranking System / Система рейтинга школьных классов

## English

### Description

This is a web application built with Flask designed to track and rank school classes based on points awarded across various criteria. It features a public view for students and parents to see rankings and class details, and an administrative panel for managing the system. The application uses SQLAlchemy for database operations (with SQLite as the default database) and Redis for caching ranking results to improve performance.

### Features

* **Public View:**
    * Displays Top 3 ranked classes for selected age groups (e.g., "young" and "old").
    * Allows selecting a specific class to view detailed points per criterion.
    * Provides links to download criteria and schedule documents (PDF).
    * Shows a description of the assessment methodology.
* **Admin Panel (Login Required):**
    * Dashboard view with class rankings for selected groups.
    * Add points to classes for specific criteria with descriptions.
    * Manage classes (add/delete) per age group.
    * Manage criteria (add/edit/delete name and coefficient).
    * Manage users (add/delete users, assign permissions for managing classes, criteria, and other users).
    * Update own user profile (username, password).
    * Upload criteria and schedule PDF files.
    * Option to clear the database (classes and points - use with caution!).
* **Technology:**
    * User authentication using Flask-Login.
    * Database interaction via Flask-SQLAlchemy.
    * Caching with Redis.

### Technologies Used

* Python 3.x
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Redis
* Werkzeug
* HTML, CSS, JavaScript (including Vue.js in some templates)

### Setup and Running

1.  **Prerequisites:**
    * Python 3 installed.
    * Redis server installed and running on the default port (`localhost:6379`). You can usually download it from [redis.io](https://redis.io/docs/getting-started/installation/).
2.  **Clone or Download:** Get the project code onto your local machine.
3.  **Create Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the Application:**
    ```bash
    python run.py
    ```
6.  **Access:** Open your web browser and go to `http://127.0.0.1:2000` (or the IP/Port specified in `config.py` if changed).

### Admin Access

* **URL:** Access the admin panel usually via the login button on the main page, or potentially directly (though direct access might redirect if not logged in). The main admin page after login is `/admin`.
* **Default Credentials:**
    * Username: `admin`
    * Password: `pass`
* **IMPORTANT:** For security reasons, you **MUST** change the default admin password immediately after your first login via the admin panel's "Lietotājs" (User) section.

---

## Русский

### Описание

Это веб-приложение, созданное с использованием Flask, предназначенное для отслеживания и ранжирования школьных классов на основе баллов, начисляемых по различным критериям. Оно включает публичную часть для учеников и родителей, где можно увидеть рейтинги и детали по классам, и административную панель для управления системой. Приложение использует SQLAlchemy для работы с базой данных (SQLite по умолчанию) и Redis для кэширования результатов рейтинга с целью повышения производительности.

### Возможности

* **Публичный раздел:**
    * Отображение Топ-3 классов в рейтинге для выбранных возрастных групп (например, "младшая" и "старшая").
    * Позволяет выбрать конкретный класс для просмотра детальной информации о баллах по каждому критерию.
    * Предоставляет ссылки для скачивания документов с критериями и расписанием (PDF).
    * Показывает описание методики оценки.
* **Панель администратора (Требуется вход):**
    * Главная страница с рейтингом классов для выбранной группы.
    * Добавление баллов классам по конкретным критериям с описанием.
    * Управление классами (добавление/удаление) по возрастным группам.
    * Управление критериями (добавление/редактирование/удаление названия и коэффициента).
    * Управление пользователями (добавление/удаление пользователей, назначение прав на управление классами, критериями и другими пользователями).
    * Обновление собственного профиля пользователя (имя пользователя, пароль).
    * Загрузка PDF-файлов с критериями и расписанием.
    * Возможность очистки базы данных (классы и баллы - использовать с осторожностью!).
* **Технологии:**
    * Аутентификация пользователей с помощью Flask-Login.
    * Взаимодействие с базой данных через Flask-SQLAlchemy.
    * Кэширование с помощью Redis.

### Используемые технологии

* Python 3.x
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Redis
* Werkzeug
* HTML, CSS, JavaScript (включая Vue.js в некоторых шаблонах)

### Установка и запуск

1.  **Предварительные требования:**
    * Установленный Python 3.
    * Установленный и запущенный сервер Redis на порту по умолчанию (`localhost:6379`). Обычно его можно скачать с [redis.io](https://redis.io/docs/getting-started/installation/).
2.  **Клонировать или скачать:** Получите код проекта на ваш локальный компьютер.
3.  **Создать виртуальное окружение (Рекомендуется):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # В Windows используйте `venv\Scripts\activate`
    ```
4.  **Установить зависимости:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Запустить приложение:**
    ```bash
    python run.py
    ```
6.  **Доступ:** Откройте ваш веб-браузер и перейдите по адресу `http://127.0.0.1:2000` (или по IP/порту, указанному в `config.py`, если он был изменен).

### Доступ к панели администратора

* **URL:** Доступ к панели администратора обычно осуществляется через кнопку входа на главной странице или, возможно, напрямую (хотя прямой доступ может перенаправить, если вы не вошли в систему). Главная страница администратора после входа - `/admin`.
* **Учетные данные по умолчанию:**
    * Имя пользователя: `admin`
    * Пароль: `pass`
* **ВАЖНО:** Из соображений безопасности вы **ДОЛЖНЫ** изменить пароль администратора по умолчанию сразу после первого входа в систему через раздел "Lietotājs" (Пользователь) в панели администратора.