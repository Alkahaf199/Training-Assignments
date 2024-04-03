from fetch_data import InputData
from spark_analysis import Analysis

from pyspark.sql import SparkSession
import http.server
import socketserver

if __name__ == "__main__":
    # Spark Session initiated:
    spark = SparkSession.builder.master("local[*]").appName("covidAnalysis").getOrCreate()

    # Load Data:
    inputData = InputData(spark)
    covidDF = inputData.loadJSON()

    # Analysis:
    queryObj = Analysis(spark,covidDF)
    handlers = {
        "mostAffected": lambda : queryObj.deathsByCases("max"),
        "leastAffected": lambda : queryObj.deathsByCases("min"),
        "highestCases": lambda : queryObj.casesWise("max"),
        "lowestCases": lambda : queryObj.casesWise("min"),
        "totalCases": lambda : queryObj.totalCases(),
        "mostRecovered": lambda : queryObj.recoveryPerCase("max"),
        "eastRecovered": lambda : queryObj.recoveryPerCase("min"),
        "mostCritical": lambda : queryObj.criticalWise("max"),
        "leastCritical": lambda : queryObj.criticalWise("min")
    }

    class service(http.server.BaseHTTPRequestHandler):

        def do_GET(self):
            # Extract request path and query parameters
            request_path = self.path.split("/")[-1]

            # Check if a handler exists for the request path
            if request_path in handlers:
                response = handlers[request_path]()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                # Generate HTML content for the landing page with links
                html_content = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>COVID Analysis API</title>
                </head>
                <body>
                    <h1>COVID-19 Analysis API Endpoints</h1>
                    <hr>
                    <p>Available analysis options:</p>
                    <ul>
                """

                # Create links for each handler
                for key, value in handlers.items():
                    html_content += f'<li><a href="/{key}">{key.replace("_", " ")}</a></li>'

                html_content += """
                    </ul>
                </body>
                </html>
                """
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode())

                table = queryObj.showData()
                self.wfile.write(table.encode())

    class MyTCPServer(socketserver.TCPServer):
        def server_close(self):
            super().server_close()
            print("Socket released.")

    HOST = 'localhost'
    PORT = 8000
    with socketserver.TCPServer((HOST, PORT), service) as httpd:
        print(f"Serving at http://{HOST}:{PORT}")
        httpd.serve_forever()



    