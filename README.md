# LeakpeekController

An asynchrious Python tool to query Leakpeek for user data like emails, usernames, and more.

## Features

- **Automated Data Lookup**: Fetch information based on various query types using asynchrious requests.
- **Supports**: multiple search types (username, email, password, etc.)
- **Queue Management**: Handles requests efficiently with a queue.

  
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

1. Replace `self.cookie` in `LeakpeekController` with your session cookie once you have logged in.

## Usage

Run the bot and use `GetRequest("email", "test@gmail.com")` to query data, having the first parameter as the endpoint modification and the last parameter as the query you want to search within the category endpoint.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](LICENSE) file for details.
