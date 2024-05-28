# Telegram Bot for AutoService

## Introduction

This project is part of a comprehensive car service management system designed to optimize the process of managing car service records, customer interaction, and service analytics. The complete project consists of three main components:

1. **Website**: Allows customers to make service appointments, view available services, and receive information about the car service.
2. **Telegram Bot**: Provides customers with an alternative and convenient way to interact with the car service, offering the same features as the website.
3. **Main Application**: Used by car service center staff to book appointments, process customer information, and analyze car service data.

Each component is integrated with the MongoDB cloud database to ensure seamless data synchronization and availability.

![Структура проекту](https://github.com/boghtml/TelegramBot_AutoServiceProject_part_1/assets/119760440/f30720c6-70fe-47de-a98a-502ae62bf98f)

## Telegram Bot Review

The Telegram Bot is an essential part of this system, designed to facilitate the process of signing up customers for service. It allows customers to:
- Sign up by entering their personal details and car information.
- Order a service by selecting the desired service, date, and time of visit.
- View the list of available car service services.
- Get contact information, address, and other useful information about the car service.

## Features

### Main Features:
- **Sign up for service**: The client can sign up for service at a car service by entering his First Name, Last Name, Family name, information about the car, add a personal comment with wishes for the services and choose the desired date of visit.
- **View Services**: Customers can view the list of available services offered by the car service center.
- **Get Information**: Customers can get contact information, address, and other useful information about the car service center.

### Possible future bot improvements:
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

## Project Structure

- **main.py**: Entry point for the Telegram bot.
- **database/**: Contains scripts for database interactions.
- **services/**: Contains modules for different services provided by the bot.
- **utils/**: Utility functions used across the project.

## Advantages

- **Convenience**: provides customers with a simple and affordable way to interact with the car service.
- **Efficiency**: simplifies the process of booking and obtaining information.
- **Integration**: Seamlessly integrates with the main application and website for data consistency.
- **Cloudiness**: since the project works with the MongoDB temple database, it ensures the use of the bot, just with the presence of Telegrem and the Internet.

## Functionality

In order to view the functionality of the bot, open the file: "Explanatory note.docs" and go to page 56

## Conclusion

Telegram Bot for AutoService is a vital component of a larger system aimed at improving auto service management. Using the convenience of Telegram, the bot improves interaction with customers and simplifies service registration. Integrated with MongoDB, it ensures data consistency and availability, facilitating an efficient and comprehensive car service management system.
