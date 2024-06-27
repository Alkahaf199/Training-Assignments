# COVID-19 Data Analysis and API Server

This project fetches COVID-19 statistics, processes the data using PySpark, and provides a simple HTTP server to serve various analytical endpoints. The project is organized into different modules for data fetching, analysis, and server handling.

## Project Structure

### config.yml

The `config.yml` file contains configuration details such as API credentials, CSV file names, and server settings.

### data_fetch/fetch_data.py

The `fetch_data.py` script fetches COVID-19 data from an external API, writes the data to a CSV file, and loads the data into a PySpark DataFrame.

### data_analysis/analysis.py

The `analysis.py` script contains methods to perform various analyses on the COVID-19 data, such as finding the most and least affected countries, calculating recovery rates, and analyzing critical cases.

### server/http_server.py

The `http_server.py` script defines a simple HTTP server that provides various endpoints for accessing the analysis results. It uses a custom request handler and server class.

### main.py

The `main.py` script is the entry point of the project. It initializes a Spark session, loads the data, performs the analysis, and starts the HTTP server.

## Prerequisites

- Python 3.7+
- PySpark
- PyYAML

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/covid-data-analysis.git
   cd covid-data-analysis
   ```
2. Create and activate a virtual environment (optional but recommended):
   
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Update the config.yml file with your API credentials and desired settings.

## Usage

1. Run the main.py script to start the data fetching, analysis, and server:

   ```sh
   python main.py
   ```

2. Open your browser and navigate to http://localhost:8000 (or the configured host and port) to see the available endpoints.

## Endpoints

The server provides the following endpoints:

* /mostAffected: Displays the most affected country by deaths.
* /leastAffected: Displays the least affected country by deaths.
* /highestCases: Displays the country with the highest number of cases.
* /lowestCases: Displays the country with the lowest number of cases.
* /totalCases: Displays the total number of cases.
* /efficientRecovery: Displays the country with the most efficient recovery rate.
* /leastEfficientRecovery: Displays the country with the least efficient recovery rate.
* /mostCriticalCases: Displays the country with the most critical cases.
* /leastCriticalCases: Displays the country with the least critical cases.

## Configuration

The config.yml file contains the following configuration options:

   ```python
   api:
     url: "covid-193.p.rapidapi.com"
     key: "your-api-key"
     host: "covid-193.p.rapidapi.com"

  csv:
     filename: "covid_data.csv"

  server:
     host: "localhost"
     port: 8000
  ```
* api: Contains the API URL, key, and host for fetching COVID-19 data.
* csv: Specifies the filename for storing the fetched data.
* server: Defines the host and port for the HTTP server.
