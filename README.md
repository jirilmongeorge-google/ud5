# Project 5 - Data Pipelines - Purpose
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.


# ETL pipeline
The ETL pipeline should extract songs and user log data from S3, loads it into Redshift staging tables and then copy it to Redshift fact and dimension tables.To complete the project, we need to create custom Airflow operators to perform tasks such as staging the data, filling the data warehouse, and running checks on the data as the final step.

# Project Files
- udac_example_dag.py - The main DAG file
- plugins/operators/data_quality.py - Defines the DataQualityOperator
- plugins/operators/load_dimension.py -  Defines the LoadDimensionOperator
- plugins/operators/load_fact.py -  Defines the LoadFactOperator
- plugins/operators/stage_redshift.py -  Defines the StageToRedshiftOperator

# Execution Instructions
- After you have updated the DAG, you will need to run /opt/airflow/start.sh command to start the Airflow webserver. 
- Add the AWS connection 'aws_credentials' from the Admin->Connections menu
- Add the Redshift connection 'redshift' from the Admin->Connections menu
