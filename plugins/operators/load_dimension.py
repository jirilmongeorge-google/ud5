from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    
    """
    Loads dimension table in Redshift from data in staging table(s)    
    @param redshift_conn_id: Redshift connection Id
    @param table: Target table in Redshift to load
    @param select_sql: SQL query for loading data into target table
    @param append_insert: append-insert or truncate-insert 
    @param primary key: using the append-insert method using primary key
    """
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 select_sql="",
                 append_insert=False,
                 primary_key="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql
        self.append_insert = append_insert
        self.primary_key = primary_key

    def execute(self, context):
        self.log.info('LoadDimensionOperator started')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.append_insert:
            table_insert_sql = f"""
                create temp table stage_{self.table} (like {self.table}); 
                
                insert into stage_{self.table}
                {self.select_sql};
                
                delete from {self.table}
                using stage_{self.table}
                where {self.table}.{self.primary_key} = stage_{self.table}.{self.primary_key};
                
                insert into {self.table}
                select * from stage_{self.table};
            """
        else:
            table_insert_sql = f"""
                insert into {self.table}
                {self.select_sql}
            """
            
            self.log.info("Clearing data from dimension table")
            redshift_hook.run(f"TRUNCATE TABLE {self.table};")
        
        self.log.info("Loading data to dimension tables")
        redshift_hook.run(table_insert_sql)
