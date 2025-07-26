# 🤝 Helping Hands - Slot Booking System

Helping Hands is a modern slot booking system that enables organizations with multiple branches and sections to manage appointments efficiently. The system provides separate interfaces for regular users and administrators, ensuring smooth operations and excellent user experience.

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.0+
- **Database**: PostgreSQL 13+
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Migrations**: Flask-Migrate
- **Password Hashing**: Werkzeug Security

### Frontend
- **Template Engine**: Jinja2
- **Styling**: Custom CSS with modern design
- **JavaScript**: Vanilla JS with SweetAlert2
- **Icons**: Font Awesome
- **Responsive Design**: CSS Grid & Flexbox

### Development Tools
- **Version Control**: Git
- **Database Management**: pgAdmin/psql
- **Development Server**: Flask Development Server


## ✨ Features

### 👤 User Features
- **User Registration & Authentication**
  - Secure login/logout system
  - Profile management with photo upload
  - Password encryption and validation

- **Slot Booking System**
  - Browse available slots by branch and section
  - Real-time availability checking
  - Easy booking with date/time selection
  - Booking confirmation and management

- **My Bookings Dashboard**
  - View upcoming and past bookings
  - Cancel bookings with confirmation
  - Booking history tracking

- **Feedback & Rating System**
  - Submit ratings (1-5 stars) for completed bookings
  - Add detailed comments and reviews
  - View feedback history

- **Calendar Integration**
  - Visual calendar view of bookings
  - Monthly/weekly booking overview
  - Easy navigation between dates

### 🛠️ Admin Features
- **Comprehensive Admin Dashboard**
  - System overview and statistics
  - Quick access to all management tools
  - Real-time booking insights

- **User Management**
  - View all registered users
  - Promote users to admin status
  - User search and filtering
  - Account management

- **Branch & Section Management**
  - Add/edit/delete branches
  - Manage sections within branches
  - Location and service categorization

- **Slot Management**
  - Create and manage time slots
  - Set availability schedules
  - Bulk slot operations
  - Slot utilization tracking

- **Booking Management**
  - View all bookings across system
  - Filter by date, branch, section, user
  - Booking status management
  - Export booking data

- **Feedback Management**
  - Monitor customer feedback and ratings
  - Filter low-rated experiences
  - Respond to customer concerns
  - Quality assurance tracking

- **Sale Days Management**
  - Configure promotional periods
  - Set special booking rules
  - Manage seasonal campaigns



## 📁 Project Structure

```
Helping_Hands/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models.py                   # Database models
│   ├── routes/                     # Route blueprints
│   │   ├── auth.py                 # Authentication routes
│   │   ├── user_dashboard.py       # User dashboard
│   │   ├── book_my_slot.py         # Booking functionality
│   │   ├── my_bookings.py          # User bookings management
│   │   ├── calendar_view.py        # Calendar interface
│   │   ├── feedback.py             # Feedback system
│   │   ├── admin.py                # Admin dashboard
│   │   ├── manage_users.py         # User management
│   │   ├── manage_branches.py      # Branch management
│   │   ├── manage_sections.py      # Section management
│   │   ├── manage_bookings.py      # Booking management
│   │   ├── manage_slots.py         # Slot management
│   │   ├── manage_feedback.py      # Feedback management
│   │   └── manage_sale_days.py     # Sale days management
│   ├── templates/                  # HTML templates
│   │   ├── base.html               # Base template
│   │   ├── login.html              # Login page
│   │   ├── dashboard.html          # User dashboard
│   │   ├── book_slot.html          # Booking interface
│   │   ├── my_bookings.html        # User bookings
│   │   ├── calendar_view.html      # Calendar view
│   │   ├── profile.html            # User profile
│   │   └── admin/                  # Admin templates
│   │       ├── dashboard.html      # Admin dashboard
│   │       ├── bookings_dashboard.html
│   │       ├── users_dashboard.html
│   │       ├── branches_dashboard.html
│   │       ├── sections_dashboard.html
│   │       ├── feedback_dashboard.html
│   │       ├── sale_days.html
│   │       ├── create_slot.html
│   │       ├── edit_slot.html
│   │       └── partials/           # Reusable components
│   └── static/                     # Static files
│       ├── styles.css              # Main stylesheet
│       ├── helping_logo.png        # Application logo
│       └── uploads/                # User uploaded files
├── migrations/                     # Database migrations
├── seed_db.py                      # Database seeding script
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 13 or higher
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/Siddhant-Thapa/Helping-Hands
<<<<<<< HEAD
cd Helping-Hands-Software
=======
cd Helping-Hands
>>>>>>> dcc0e3a (updated readme)
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Required Packages
```bash
pip install flask flask-sqlalchemy flask-migrate flask-login psycopg2-binary werkzeug
```

## ⚙️ Configuration

### Environment Setup
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_secret_key_here
<<<<<<< HEAD
DATABASE_URL=postgresql://username:password@localhost/helping_hand
=======
DATABASE_URL=postgresql://username:enter_your_password_here@localhost/helping_hand
>>>>>>> dcc0e3a (updated readme)
FLASK_ENV=development
FLASK_DEBUG=True
```

<<<<<<< HEAD
### Database Configuration
Update the database URI in `app/__init__.py`:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:your_password@localhost/helping_hand"
```

=======
>>>>>>> dcc0e3a (updated readme)
## 🗄️ Database Setup

### Step 1: Create PostgreSQL Database
```sql
-- Connect to PostgreSQL as superuser
CREATE DATABASE helping_hand;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE helping_hand TO your_username;
```

### Step 2: Initialize Database
```bash
# Initialize migration repository
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### Step 3: Seed Database with Sample Data
```bash
python seed_db.py
```

This will populate the database with:
- **Branches**: Indiranagar, Whitefield, Malleshwaram, Koramangala, HSR Layout
- **Sections**: Electronics, Clothing, Shoes, Furniture, Grocery (Non-Veg), Veg

## 🎮 Usage

### Starting the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

### Default Access
- **Admin Account**: Create through user registration, then promote via database
- **User Account**: Register through the web interface


## 🔗 API Endpoints

### Authentication
- `GET /` - Home page
- `GET /login` - Login page
- `POST /login` - User authentication
- `GET /register` - Registration page
- `POST /register` - User registration
- `GET /logout` - User logout

### User Dashboard
- `GET /dashboard` - User dashboard
- `GET /profile` - User profile
- `POST /profile` - Update profile

### Booking System
- `GET /book-slot` - Booking interface
- `POST /book-slot` - Create booking
- `GET /my-bookings` - User bookings
- `POST /cancel-booking/<id>` - Cancel booking
- `GET /calendar` - Calendar view

### Feedback System
- `GET /feedback` - Feedback interface
- `POST /rate/<booking_id>` - Submit feedback

### Admin Panel
- `GET /admin` - Admin dashboard
- `GET /admin/users` - User management
- `GET /admin/branches` - Branch management
- `GET /admin/sections` - Section management
- `GET /admin/bookings` - Booking management
- `GET /admin/slots` - Slot management
- `GET /admin/feedback` - Feedback management
- `GET /admin/sale-days` - Sale days management

## 📸 Screenshots

<<<<<<< HEAD
### User Interface
- **Dashboard**: Clean, intuitive user dashboard with booking overview
- **Booking System**: Easy-to-use slot selection with real-time availability
- **Calendar View**: Visual representation of bookings and availability

### Admin Interface
- **Admin Dashboard**: Comprehensive system overview with statistics
- **Management Panels**: Dedicated interfaces for all system components
- **Responsive Design**: Mobile-friendly admin interface
=======
### 🛠️ Admin Interface

#### 📊 Admin Dashboard
![Admin Dashboard](static/screenshots/admin_dashboard.png)

#### 🏢 Branch Management
![Branches Dashboard](static/screenshots/branches_dashboard.png)

#### 🧩 Slot Management
![Slot Management](static/screenshots/slot_management.png)

#### 👥 User Approvals
![User Approval](static/screenshots/user_approval.png)

--------------------------------------------------------------

### 🧑‍💻 User Interface

#### 🏠 User Dashboard
![User Dashboard](static/screenshots/user_dashboard.png)

#### 📅 Weekly Slot View
![Weekly Slot View](static/screenshots/weekly_slot_view.png)

#### 📆 Book a Slot
![Book a Slot](static/screenshots/book_a_slot.png)

#### 📚 My Bookings
![My Bookings](static/screenshots/my_booking.png)


>>>>>>> dcc0e3a (updated readme)


## 🤝 Contributing

We welcome contributions to improve the Helping Hands system!

### How to Contribute
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**


### Areas for Contribution
- 🐛 Bug fixes and improvements
- ✨ New features and enhancements
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations
- 🧪 Test coverage expansion

<<<<<<< HEAD
=======
🐞 Known Issues
Star Rating Always Shows 1 Star in Admin Panel
When submitting feedback, the selected star rating (1–5) is not reflected correctly. All feedback entries currently display as 1 star, regardless of the user selection.

-Status: Identified

-Root Cause: Likely due to incorrect form data binding or missing JS integration for star input (sweetalert templete used there likely cause of the issue)

-Fix Planned: Yes, to be addressed in upcoming patch

>>>>>>> dcc0e3a (updated readme)

## 📞 Support

For support, questions, or suggestions:
- **GitHub Issues**: [Create an issue](https://github.com/Siddhant-Thapa/Helping-Hands/issues)
- **Email**: [Contact the team](mailto:thapasiddhant9@gmail.com)

---

**Made with ❤️ by the Helping Hands Team**

<<<<<<< HEAD
*Empowering organizations with efficient slot booking management*
=======
*Empowering organizations with efficient slot booking management*
>>>>>>> dcc0e3a (updated readme)
