# LeakpeekController

An async Python tool to query the Leakpeek API for user data like emails, usernames, and more.

## Features

- **Automated Data Lookup**: Fetch information based on various query types.
- **Queue Management**: Handles requests efficiently with a queue.
- **Custom Headers**: Personalize request headers easily.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/leakpeekcontroller.git
    cd leakpeekcontroller
    ```
2. Install dependencies:
    ```sh
    pip install aiohttp faker
    ```

## Setup

1. Replace `self.cookie` in `LeakpeekController` with your session cookie.
2. Customize request headers in `self.headers` as needed.

## Usage

Run the bot and use `GetRequest("email", "test@gmail.com")` to query data.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](LICENSE) file for details.
