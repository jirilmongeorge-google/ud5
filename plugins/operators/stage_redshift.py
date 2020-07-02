from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    """
    This custom operator Copies JSON data from S3 to Redshift staging tables    
    @param redshift_conn_id: Redshift connection  details
    @param aws_credentials_id: AWS credentials details
    @param table: Redshift staging table to copy data into
    @param s3_bucket: Source S3 bucket 
    @param s3_key: S3 bucket objevt prefix where JSON data files are stored
    @param copy_json_option: Either a JSONPaths file or 'auto'
    @param region: AWS Region
    """
    
    ui_color = '#358140'
    
    redshift_copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION AS '{}'
        FORMAT as json '{}'
    """

    @apply_defaults
    def __init__(self,
                self.redshift_conn_id = redshift_conn_id
                self.aws_credentials_id = aws_credentials_id
                self.table = table
                self.s3_bucket = s3_bucket
                self.s3_key = s3_key
                self.copy_json_option = copy_json_option
                self.region = region,
                *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.s3_bucket = s3_bucket
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.copy_json_option = copy_json_option
        self.region = region
        self.s3_key = s3_key
        self.table = table

    def execute(self, context):
        self.log.info('Starting S3ToRedshift Operator ')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Purge data from Redshift tables")
        redshift.run("DELETE FROM {}".format(self.table))
        
        self.log.info("Copying data from S3 to Redshift staging tables")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        formatted_sql = StageToRedshiftOperator.redshift_copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.copy_json_option
        )
        redshift.run(formatted_sql)
        





