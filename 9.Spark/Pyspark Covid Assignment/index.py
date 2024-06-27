from src.data_extraction.fetch_data import InputData
from src.data_analysis.analysis import Analysis
from src.server.http_server import run_server
from utilities.spark_session import get_spark_session

from pyspark.sql import SparkSession

if __name__ == "__main__":
    # Spark Session initiated:
    spark = get_spark_session()

    # Load Data:
    inputData = InputData(spark)
    covidDF = inputData.loadJSON()

    # Analysis:
    queryObj = Analysis(spark, covidDF)
    handlers = {
        "mostAffected": lambda: queryObj.deathsByCases("max"),
        "leastAffected": lambda: queryObj.deathsByCases("min"),
        "highestCases": lambda: queryObj.casesWise("max"),
        "lowestCases": lambda: queryObj.casesWise("min"),
        "totalCases": queryObj.totalCases,
        "efficientRecovery": lambda: queryObj.recoveryPerCase("max"),
        "leastEfficientRecovery": lambda: queryObj.recoveryPerCase("min"),
        "mostCriticalCases": lambda: queryObj.criticalWise("max"),
        "leastCriticalCases": lambda: queryObj.criticalWise("min"),
    }

    # Server initiation
    run_server(handlers)
