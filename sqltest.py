import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    auth_plugin='mysql_native_password',
    database='laundrobase'
)

mycursor = db.cursor()

# # create table:
# mycursor.execute("CREATE TABLE Strategy (id VARCHAR(50), wt1 float UNSIGNED, wt2 float UNSIGNED, last_candle_high float UNSIGNED, last_candle_low float UNSIGNED, last_candle_vwap float UNSIGNED, active_position VARCHAR(50), new_trend VARCHAR(50), last_trend VARCHAR(50), active_trend VARCHAR(50))")

# # describe table details:
# mycursor.execute("DESCRIBE Strategy")

# for x in mycursor:
#     print(x)

# # insert into table
# mycursor.execute("INSERT INTO Strategy () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("30_min", 0.0, 0.0, 0.0, 0.0, 0.0, "null", "null", "null", "null"))
# db.commit()

# mycursor.execute("SELECT * FROM Strategy")

# Query
# mycursor.execute("SELECT * FROM Strategy WHERE id = '1_min'")
# for x in mycursor:
#     print(x)

# # Query specific
# mycursor.execute("SELECT wt1, wt2 FROM Strategy WHERE name = '9_min'")

# # Alter / Add
# mycursor.execute("ALTER TABLE strategy ADD COLUMN test VARCHAR(50) NOT NULL")

# # Alter / Remove
# mycursor.execute("ALTER TABLE Strategy DROP test")

# # Alter / Change column name

# mycursor.execute("ALTER TABLE Strategy CHANGE name id VARCHAR(50)")

def updateDbValue(id_name, column_name, value):
    try:
        query = "UPDATE strategy SET " + str(column_name) + "=" + str(value) + " WHERE id = '" + str(id_name) + "'" 
        print(query)
        mycursor.execute(query)
        db.commit()
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))


def updateMultipleDbValues(id_name, wt1_value, wt2_value, last_candle_high_value, last_candle_low_value, last_candle_vwap_value):
    try:
        query = "UPDATE strategy SET wt1=" + str(wt1_value) + ", wt2=" + str(wt2_value) + ", last_candle_low=" + str(last_candle_low_value) + ", last_candle_high=" + str(last_candle_high_value) + ", last_candle_vwap=" + str(last_candle_vwap_value) + " WHERE id = '" + str(id_name) + "'"
        print(query)
        mycursor.execute(query)
        db.commit()
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))



# updateDbValue('1_min', 'wt1', 0)
updateMultipleDbValues('9_min', 0, 0, 0, 0, 0)

# mycursor.getUpdateCount()