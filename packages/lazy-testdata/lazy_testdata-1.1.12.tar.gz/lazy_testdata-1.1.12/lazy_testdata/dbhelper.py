'''
Author: yuweipeng
Date: 2023-01-17 09:58:17
LastEditors: yuweipeng
LastEditTime: 2023-04-01 11:13:05
Description: file content
'''
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import records


def connet_db(conn_str):
    engine = create_engine(conn_str, encoding='utf-8')
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


def only_query(conn, sql):
    db = records.Database(conn)
    rows = db.query(sql)  # or db.query_file('sqls/active-users.sql')
    return rows


def exec_sql(conn, sql):
    session = connet_db(conn)
    tmp_list = session.execute(sql)
    session.commit()
    return tmp_list


def write_csv_insert_db(conn, table_name, fieldnames, data, csv_file=None):
    if data:
        if not csv_file:
            csv_file = f'{table_name}.csv'
        with open(csv_file,'w',newline='',encoding='utf-8') as file:
            fieldnames = fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)    
        engine = create_engine(conn)
        rows = pd.read_csv(csv_file)
        rows.to_sql(table_name, con=engine, if_exists='append',index=False)
