# Drive-Through Application

## Overview
The Drive-Through Application is a web-based application that allows users to place and manage orders for food items. The backend is built using FastAPI, while the frontend is developed with Svelte. This application provides a seamless experience for users to create, view, and cancel orders.

## Features
- Create new orders for burgers, fries, and drinks.
- Cancel existing orders.
- View active and canceled orders.
- Integration with OpenAI for processing user input.

## Technologies Used
- **Backend**: FastAPI
- **Frontend**: Svelte
- **Database**: In-memory storage (for demonstration purposes)
- **OpenAI API**: For processing user input

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Node.js and npm (for Svelte)
- OpenAI API key (if using OpenAI features)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ilmaan/Drive_Through_app.git
   cd https://github.com/ilmaan/Drive_Through_app.git
   ```

2. **Set up the backend**:
   - Navigate to the backend directory and install the required packages:
     ```bash
     cd backend
     pip install -r requirements.txt
     ```

3. **Set up the frontend**:
   - Navigate to the frontend directory and install the required packages:
     ```bash
     cd frontend
     npm install
     ```

4. **Configure OpenAI credentials**:
   - Ensure you have your OpenAI API key set up in the environment or in the appropriate configuration file.

### Running the Application

1. **Start the backend server**:
   ```bash
   cd backend
   uvicorn main1:app --reload
   ```

2. **Start the frontend application**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the application**:
   - Open your web browser and navigate to `http://localhost:8080` (or the port specified by your Svelte app).

## API Endpoints

### Backend API Endpoints

- **GET /**: Returns the home page of the application.
- **POST /orders/**: Create a new order. Requires a JSON body with `order_text`.
- **DELETE /orders/cancel/**: Cancel an existing order. Requires a JSON body with `order_no` and `cancel_text`.
- **GET /orders/canceled/**: Retrieve a list of all canceled orders.
- **GET /orders/all/**: Retrieve a list of all active and canceled orders.
- **POST /process_input/**: Process input through OpenAI to determine the action. Requires a JSON body with `order_text`.

### API Documentation
- **Swagger UI**: Access the Swagger documentation at `http://localhost:8000/docs` to explore the API endpoints interactively.
- **Redoc**: Access the Redoc documentation at `http://localhost:8000/redoc` for a more detailed view of the API specifications.

### Frontend API Integration
The frontend communicates with the backend APIs to fetch and manage orders. The Svelte application handles user input and displays the order status in real-time.

## Usage
1. **Placing an Order**: Enter the order details in the input field and click "Submit Order". The order will be processed and added to the active orders list.
2. **Viewing Orders**: Active and canceled orders are displayed on the main page.
3. **Canceling an Order**: To cancel an order, use the cancellation functionality provided in the application (if implemented).

## NOTE
1. **The OPENAI key is incorrect have to change it**: Email me at ilmaanzia@gmail.com for further details.

