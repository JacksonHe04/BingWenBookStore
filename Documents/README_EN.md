# README for BingWenBookStore

## Introduction

**BingWenBookStore** is a comprehensive online bookstore project developed as a course project for the Database Principles course at the Southeast University School of Computer Science and Engineering. The name pays homage to the founder of Southeast University, **Guo Bingwen**.

### Team Members

- **何锦诚**: Frontend development and UI design
- **郑宇榕**: Backend development
- **刘睿哲**: Product management and operations

This project integrates a user-friendly front-end interface with a robust backend to provide a seamless e-commerce experience.

## Features

- Comprehensive book management system
- User-friendly cart and order system
- Secure user authentication and payment gateway
- Modern UI with responsive design

## Project Structure

```
BingWenBookStore/
├── BookStoreBackend/       # Django-based backend
├── Documents/              # Design and reports
├── Frontend-Vite/          # Vite-powered Vue.js frontend
├── Resources/              # Data sources and analysis
└── README.md               # This README file
```

## Setup Guide

### Prerequisites

Ensure the following tools are installed:

- **Node.js**: v16+
- **Python**: v3.10+
- **MySQL**: Latest stable version

### Backend Setup

1. Navigate to the `BookStoreBackend` directory:

    ```bash
    cd BookStoreBackend
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure the database:

    - Open `BookStoreBackend/settings.py` and update the `DATABASES` section with your MySQL credentials.

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Populate the database with test data (optional):

    ```bash
    python generate_test_data.py
    ```

6. Start the Django server:

    ```bash
    python manage.py runserver
    ```

   The backend will be accessible at `http://127.0.0.1:8000`.

### Frontend Setup

1. Navigate to the `Frontend-Vite` directory:

    ```bash
    cd Frontend-Vite
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Start the development server:

    ```bash
    npm run dev
    ```

   The frontend will be accessible at `http://127.0.0.1:5173`.

4. Build for production (if required):

    ```bash
    npm run build
    ```

   The build output will be available in the `dist` folder.

## Usage

- Access the homepage at `http://127.0.0.1:5173` (frontend).
- Backend APIs are available at `http://127.0.0.1:8000/api/`.

## Resources and Documentation

- **Documents/**: Contains project reports and design documents.
- **Resources/**: Includes data source information and cleaned data files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

We thank the faculty of the Database Principles course for their guidance and Southeast University for providing this platform to enhance our learning. Special thanks to **Guo Bingwen**, whose visionary leadership continues to inspire us.

---

For further inquiries or contributions, please contact any of the team members. Happy coding! 🎉