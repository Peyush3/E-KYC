import mysql.connector
import pandas as pd
from utils import read_yaml

config_path = "config.yaml"
config = read_yaml(config_path)
secrets = config['secrets']

mydb = mysql.connector.connect(
    host=secrets['HOST'],
    user=secrets['USER'],
    password=secrets['PASSWORD'],
    database=secrets['DB'],
    auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()

def insert_records(text_info, conn):
    sql = "INSERT INTO users(id, name, father_name, dob, id_type, embedding) VALUES (%s, %s, %s, %s, %s, %s)"
    value = (text_info['ID'], text_info['Name'], text_info["Father's Name"], text_info['DOB'], text_info['ID Type'], str(text_info['Embedding']))
    mycursor.execute(sql, value)
    mydb.commit()

def fetch_records(conn):
    sql = "SELECT * FROM users;"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if result:
        df = pd.DataFrame(result, columns=[desc[0] for desc in mycursor.description])
        return df
    else:
        return pd.DataFrame()

def check_duplicacy(text_info, conn):
    is_duplicate = False
    df = fetch_records(conn)
    if df.empty:
        print("DataFrame is empty. No records found in the database.")
        return False
    df = df[df['id'] == text_info['ID']]
    if df.shape[0] > 0:
        is_duplicate = True
    return is_duplicate
