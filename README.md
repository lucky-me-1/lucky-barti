# **Appointment Scheduling API**

This project is a Flask-based API for managing appointments for doctors. The API allows users to create, retrieve, and search for available appointment slots for two doctors: **Doctor Strange** and **Doctor Who**. The API also allows you to check for available slots after a specific time and for specific doctors.

## **Table of Contents**

- [Database Initialization](#database-initialization)
- [API Endpoints](#api-endpoints)
  - [Initialize Database](#initialize-database)
  - [Create an Appointment](#create-an-appointment)
  - [Get Appointments Within a Time Window](#get-appointments-within-a-time-window)
  - [Get First Available Appointment](#get-first-available-appointment)
- [Running Tests](#running-tests)

---


## **Database Initialization**

You need to initialize the database with the doctors' schedules by calling the `/init_db` endpoint. This should be done once on startup.

1. **Run the Flask app:**
   ```bash
   flask run
   ```

2. **Initialize the database by calling the `/init_db` endpoint:**

   - **Endpoint**: `/init_db`
   - **Method**: `POST`

   **Example using `curl`:**
   ```bash
   curl -X POST http://127.0.0.1:5000/init_db
   ```

   If the database has already been initialized, this endpoint will return:
   ```json
   { "message": "Init already done." }
   ```

---

## **API Endpoints**

### **1. Initialize Database**

- **Endpoint**: `/init_db`
- **Method**: `POST`
- **Description**: Initializes the database with two doctors:
  - Doctor Strange: Working from 9 AM to 5 PM, Monday to Friday.
  - Doctor Who: Working from 8 AM to 4 PM, Monday to Friday.
  
- **Response**:
  - **Success**:
    ```json
    { "message": "Database initialized with doctors." }
    ```
  - **Failure** (if already initialized):
    ```json
    { "message": "Init already done." }
    ```

---

### **2. Create an Appointment**

- **Endpoint**: `/appointments`
- **Method**: `POST`
- **Description**: Creates an appointment for a doctor. The system checks the availability of the doctor and whether there are any conflicting appointments.

- **Request Body**:
  ```json
  {
    "doctor_id": 1,
    "start_time": "2024-09-12T09:00:00",
    "duration": 45
  }
  ```
  - `doctor_id`: The ID of the doctor.
  - `start_time`: The start time of the appointment in ISO 8601 format.
  - `duration`: The duration of the appointment in minutes.

- **Response**:
  - **Success**:
    ```json
    { "message": "Appointment created successfully." }
    ```
  - **Failure (doctor unavailable)**:
    ```json
    { "message": "Doctor not available at the specified time." }
    ```
  - **Failure (conflict)**:
    ```json
    { "message": "The time slot is already booked." }
    ```

---

### **3. Get Appointments Within a Time Window**

- **Endpoint**: `/appointments`
- **Method**: `GET`
- **Description**: Retrieves all appointments for a specific doctor within a given time window.

- **Query Parameters**:
  ```
  /appointments?doctor_id=1&start_time=2024-09-12T08:00:00&end_time=2024-09-12T17:00:00
  ```
  - `doctor_id`: The ID of the doctor.
  - `start_time`: The start time of the window in ISO 8601 format.
  - `end_time`: The end time of the window in ISO 8601 format.

- **Response**:
  - **Success**:
    ```json
    [
      {
        "id": 1,
        "doctor_id": 1,
        "start_time": "2024-09-12T09:00:00",
        "end_time": "2024-09-12T09:45:00"
      }
    ]
    ```
  - **Failure (validation error)**: Error message and HTTP `400 Bad Request`.

---

### **4. Get First Available Appointment**

- **Endpoint**: `/appointments/available`
- **Method**: `GET`
- **Description**: Returns the first available appointment after a specified time. Filters by doctor if `doctor_id` is provided. Defaults to the current time if `after_time` is not provided.

- **Query Parameters**:
  ```
  /appointments/available?doctor_id=1&after_time=2024-09-12T08:00:00
  ```
  - `doctor_id` (optional): The ID of the doctor. If not provided, all doctors are checked.
  - `after_time` (optional): The time after which to search for available slots. If not provided, the current time is used.

- **Response**:
  - **Success**:
    ```json
    {
      "doctor_id": 1,
      "doctor_name": "Strange",
      "start_time": "2024-09-12T11:00:00",
      "end_time": "2024-09-12T11:45:00"
    }
    ```
  - **Failure (no available slots)**:
    ```json
    { "message": "No available slots." }
    ```

---

## **Running Tests**

1. **Install `pytest`:**
   ```bash
   pip install pytest
   ```

2. **Run the tests:**
   ```bash
   pytest tests/test_schedule.py
   ```

The test cases ensure that all APIs are covered, and the behavior of the system is as expected.