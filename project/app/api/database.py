import logging
import json
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()

# Load environment variables from .env
load_dotenv()


class PostgreSQL:
    def __init__(self):
        "Add custom fields here"

    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                                  host=DB_HOST, port='5432')

    # methods can reference this variable
    columns = ['Bridge_Name',
               'Project_Code',
               'Needs_Assessment',
               'Bridge_Opportunity_Level1_Government',
               'Bridge_Opportunity_Level2_Government',
               'Stage',
               'GPS_Latitude',
               'GPS_Longitude',
               'Bridge_Type',
               'Bridge_Span_m',
               'Individuals_Directly_Served',
               'year_2013_2014_Data',
               'Form_Name',
               'Created_By',
               'Bridge_Location_GPS_Latitude',
               'Proposed_Bridge_Location_GPS_Longitude',
               'Current_crossing_method',
               'Nearest_all_weather_crossing_point',
               'Days_per_year_river_flooded',
               'Flood_duration_rainy_season',
               'Market_access_blocked_by_river',
               'Education_access_blocked_by_river',
               'Health_access_blocked_by_river',
               'Other_access_blocked_by_river',
               'Primary_occupations',
               'Primary_crops_grown',
               'River_crossing_deaths_last_3_years',
               'River_crossing_injuries_last_3_years',
               'Incident_descriptions',
               'Notes_social_information',
               'Cell_service_quality',
               'Accessibility',
               'Name_nearest_city',
               'Name_nearest_paved_or_sealed_road',
               'Bridge_classification',
               'Flag_for_Rejection',
               'Rejection_Reason',
               'Bridge_Types',
               'Estimated_span_m',
               'Height_differential_between_banks',
               'General_Project_Photos',
               'CaseSafeID',
               'Senior_Engineering_Review_Conducted']

    def conn_curs(self):
        """
        makes a connection to the database
        """
        # Establishes connection and cursor
        connection = self.connection
        cursor = self.connection.cursor()
        return connection, cursor

    def cursor(self):
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)

    def close(self):
        self.connection.close()

    def fetch_query_records(self, query: str):
        """This is a custom query, that returns all the records based on customed query"""
        # Establishes connection and cursor
        conn, cursor = self.conn_curs()
        cursor.execute(query)
        # fetches all records, we can limit # of records by put LIMIT statement in query
        result = cursor.fetchall()
        # closes connection, for now, closing causes a bug that prevents add post/get requests, but in the
        # future closing the connection may be a proper step to implement, at the moment it works find without it.
        # cursor.close()
        # conn.close()
        return result

    def fetch_all_records(self):
        """This is query returns all data/records in json format"""
        # Establishes connection and cursor
        conn = self.connection
        cursor = self.connection.cursor()
        query = """ SELECT * from public."B2P_oct_2018";"""
        cursor.execute(query)
        result = cursor.fetchall()
        # cursor.close()
        # conn.close()
        df = pd.DataFrame(result, columns=['index'] + self.columns)
        df = df.iloc[:, 1:]  # skip 1 column, as it corresponds to an index column
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        return parsed

    def fetch_query_given_project(self, project_code):
        # Establishes connection and cursor
        conn = self.connection
        cursor = self.connection.cursor()
        query = f"""SELECT * FROM public."B2P_oct_2018" where "Project_Code" = '{project_code}';"""
        cursor.execute(query)
        result = cursor.fetchall()
        # cursor.close()
        # conn.close()
        df = pd.DataFrame(result, columns=['index'] + self.columns)  #
        df = df.iloc[:, 1:]  # skip 1 column, as it corresponds to an index column
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        return parsed


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    Project_Code: str = Field(..., example='1007374')

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])


@router.post('/data_by_bridge_code')
async def get_record(item: Item):
    """
    # Returns all records, based on project_code

    # Request Body
    - `project_code`: string

    # Response All Records Based on Bridge Code in JSON FORMAT
   - 'Bridge_Name':str
   - 'Project_Code',:str
   - 'Needs_Assessment': str

    """

    PSQL = PostgreSQL()
    json_output = PSQL.fetch_query_given_project(item.Project_Code)
    return json_output


@router.post('/all_data')
async def get_all_record():
    """

    #Response All Data/Records in JSON FORMAT
    - 'Bridge_Name'
    - 'Project_Code',
    - 'Needs_Assessment',
    - 'Bridge_Opportunity_Level1_Government',
    - 'Bridge_Opportunity_Level2_Government',
    - 'Stage',
    - 'GPS_Latitude',
    - 'GPS_Longitude',
    - 'Bridge_Type',
    - 'Bridge_Span_m',
    - 'Individuals_Directly_Served',
    - 'year_2013_2014_Data',
    - 'Form_Name',
    - 'Created_By',
    - 'Bridge_Location_GPS_Latitude',
    - 'Proposed_Bridge_Location_GPS_Longitude',
    - 'Current_crossing_method',
    - 'Nearest_all_weather_crossing_point',
    - 'Days_per_year_river_flooded',
    - 'Flood_duration_rainy_season',
    - 'Market_access_blocked_by_river',
    - 'Education_access_blocked_by_river',
    - 'Health_access_blocked_by_river',
    - 'Other_access_blocked_by_river',
    - 'Primary_occupations',
    - 'Primary_crops_grown',
    - 'River_crossing_deaths_last_3_years',
    - 'River_crossing_injuries_last_3_years',
    - 'Incident_descriptions',
    - 'Notes_social_information',
    - 'Cell_service_quality',
    - 'Accessibility',
    - 'Name_nearest_city',
    - 'Name_nearest_paved_or_sealed_road',
    - 'Bridge_classification',
    - 'Flag_for_Rejection',
    - 'Rejection_Reason',
    - 'Bridge_Types',
    - 'Estimated_span_m',
    - 'Height_differential_between_banks',
    - 'General_Project_Photos',
    - 'CaseSafeID',
    - 'Senior_Engineering_Review_Conducted'


    """
    pg = PostgreSQL()
    return_json = pg.fetch_all_records()
    return return_json


class Item1(BaseModel):
    """Use this data model to parse the request body JSON."""

    input1: str = Field(..., example='output1')
    output2: str = Field(..., example='output2')

    # @validator('input1')
    # def title_must_be_a_string(cls, value):
    #     """Validate that Title is a string."""
    #     assert type(value) == str, f'Title == {value}, must be a string'
    #     return value
    #
    # @validator('output1')
    # def post_must_be_a_string(cls, value):
    #     """Validate that post is a string."""
    #     assert type(value) == str, f'Title == {value}, must be a string'
    #     return value


@router.post('/predict')
async def predict(item: Item1):
    """
    Returns Prediction 🔮

    ### Request Body

   - 'Bridge_Name':str
   - 'Project_Code',:str
   - 'Needs_Assessment': str
    """
    prediction = item.input1 + '+' + item.output2

    return {"prediction": prediction}
