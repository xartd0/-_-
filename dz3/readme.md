
# XML to Configuration Language Converter

This project provides a command-line tool written in Python that converts XML files into a custom configuration language. The language supports various constructs such as comments, arrays, dictionaries, constants, and more. This tool identifies and handles syntax errors, providing meaningful error messages to the user.

## Features

- **Structs**: XML elements are converted to struct objects.
- **Lists**: Repeated XML elements with the same tag are converted to lists.
- **Constants**: Allows for constant declaration and computation at the translation stage.
- **Error Handling**: Proper error handling for missing attributes and unknown constants.
- **Testing**: Comprehensive tests using `pytest` to ensure all constructs and conversions are covered.

## Usage

### Installation

Make sure you have Python 3.7+ installed.

1. Clone this repository:

    ```bash
    git clone https://github.com/xartd0/conf_upravlenie
    cd conf_upravlenie
    ```

2. Install dependencies (if any):

    ```bash
    pip install -r requirements.txt
    ```

### Command-Line Usage

You can use the converter by providing the path to the XML file:

```bash
python converter.py -f input.xml
```

This will read the `input.xml` file and output the corresponding configuration language structure to the standard output.

#### Example

For an XML file like:

```xml
<server port="8080">
  <host>localhost</host>
  <routes>
    <route path="/home" handler="homeHandler"/>
    <route path="/login" handler="loginHandler"/>
  </routes>
  <const name="MAX_CONNECTIONS" value="100"/>
  <compute name="MAX_CONNECTIONS"/>
</server>
```

Running the command:

```bash
python converter.py -f server_config.xml
```

Will produce:

```plaintext
struct {
  port = 8080,
  host = "localhost",
  routes = struct {
    route = (list
      struct {
        path = "/home",
        handler = "homeHandler",
      }
      struct {
        path = "/login",
        handler = "loginHandler",
      }
    ),
  }
  100 -> maxconnections
  ![maxconnections]
}
```

### Error Handling

If an XML file contains invalid structures or references unknown constants, the tool will raise an error and provide a helpful message to identify the issue.

## Testing

This project uses `pytest` for testing. To run the tests:

1. Install `pytest` if you haven't already:

    ```bash
    pip install pytest
    ```

2. Run the tests:

    ```bash
    pytest test_converter.py
    ```

You should see an output like:

```bash
============================= test session starts =============================
collected 5 items

test_converter.py .....                                               [100%]

============================== 5 passed in 0.05s ==============================
```

## Example Configurations

Here are some example XML configurations from different domains that can be used with this tool.

### Web Server Configuration

**XML Input:**

```xml
<server port="8080">
  <host>localhost</host>
  <routes>
    <route path="/home" handler="homeHandler"/>
    <route path="/login" handler="loginHandler"/>
  </routes>
  <const name="MAX_CONNECTIONS" value="100"/>
  <compute name="MAX_CONNECTIONS"/>
</server>
```

**Converted Output:**

```plaintext
struct {
  port = 8080,
  host = "localhost",
  routes = struct {
    route = (list
      struct {
        path = "/home",
        handler = "homeHandler",
      }
      struct {
        path = "/login",
        handler = "loginHandler",
      }
    ),
  }
  100 -> maxconnections
  ![maxconnections]
}
```

### Database Configuration

**XML Input:**

```xml
<database>
  <host>db.example.com</host>
  <port>5432</port>
  <user>dbuser</user>
  <password>dbpass</password>
  <tables>
    <table name="users"/>
    <table name="orders"/>
  </tables>
  <const name="TIMEOUT" value="30"/>
  <compute name="TIMEOUT"/>
</database>
```

**Converted Output:**

```plaintext
struct {
  host = "db.example.com",
  port = 5432,
  user = "dbuser",
  password = "dbpass",
  tables = struct {
    table = (list
      struct {
        name = "users",
      }
      struct {
        name = "orders",
      }
    ),
  }
  30 -> timeout
  ![timeout]
}
```


