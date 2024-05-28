# Telegram Bot for AutoService

## Introduction

This project is part of a comprehensive car service management system designed to optimize the process of managing car service records, customer interaction, and service analytics. The complete project consists of three main components:

1. **Website**: Allows customers to make service appointments, view available services, and receive information about the car service.
2. **Telegram Bot**: Provides customers with an alternative and convenient way to interact with the car service, offering the same features as the website.
3. **Main Application**: Used by car service center staff to book appointments, process customer information, and analyze car service data.

Each component is integrated with the MongoDB cloud database to ensure seamless data synchronization and availability.

## Telegram Bot Review

The Telegram Bot is an essential part of this system, designed to facilitate the process of signing up customers for service. It allows customers to:
- Sign up by entering their personal details and car information.
- Order a service by selecting the desired service, date, and time of visit.
- View the list of available car service services.
- Get contact information, address, and other useful information about the car service.

## Features

### Main Features:
- **Customer Registration**: Customers can register by entering their personal details and vehicle information.
- **Book a Service**: Customers can choose the desired service, date, and time of visit.
- **View Services**: Customers can view the list of available services offered by the car service center.
- **Get Information**: Customers can get contact information, address, and other useful information about the car service center.

### Additional Features:
- **Employee Workload Tracking**: Admins can monitor employee workload through the bot interface.
- **Analytics**: Administrators can receive reports on earnings, service popularity, and employee workload.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/boghtml/TelegramBot_AutoServiceProject_part_1.git
    ```

2. Navigate to the project directory:
    ```bash
    cd TelegramBot_AutoServiceProject_part_1
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables for the bot, such as the Telegram bot token and database connection string.

5. Run the bot:
    ```bash
    python main.py
    ```

## Usage

1. **Registration**: Customers can register by entering their details through the Telegram Bot.
2. **Booking**: Customers can book a service by selecting the desired service, date, and time.
3. **View Services**: Customers can view the list of available services at any time.
4. **Information**: Customers can get information about the car service, including contact details and address.

## Project Structure

- **main.py**: Entry point for the Telegram bot.
- **database/**: Contains scripts for database interactions.
- **services/**: Contains modules for different services provided by the bot.
- **utils/**: Utility functions used across the project.

## Advantages

- **Convenience**: Provides an easy and accessible way for customers to interact with the car service.
- **Efficiency**: Streamlines the booking and information retrieval process.
- **Integration**: Seamlessly integrates with the main application and website for data consistency.
- **Analytics**: Provides valuable insights and reports for administrators.

## Conclusion

The Telegram Bot for AutoService is a vital component of a larger system aimed at improving car service management. By leveraging the convenience of Telegram, the bot enhances customer interaction and streamlines service booking. Integrated with MongoDB, it ensures data consistency and availability, contributing to an efficient and comprehensive car service management system.
