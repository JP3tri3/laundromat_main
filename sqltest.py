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

# mycursor.execute("CREATE TABLE trades (id VARCHAR(50), symbol VARCHAR(50), symbol_pair VARCHAR(50), key_input INT UNSIGNED, limit_price_difference float UNSIGNED, leverage INT UNSIGNED, input_quantity INT UNSIGNED, data_name VARCHAR(50))")

# # describe table details:
# mycursor.execute("DESCRIBE Strategy")

# for x in mycursor:
#     print(x)

# # insert into table
# mycursor.execute("INSERT INTO Strategy () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("30_min", 0.0, 0.0, 0.0, 0.0, 0.0, "null", "null", "null", "null"))
# db.commit()

# mycursor.execute("INSERT INTO trades () VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ('main', 'empty', 'empty', 0, 0.0, 0, 0, 'empty'))
# db.commit()
# mycursor.execute("SELECT * FROM Strategy")

# Query
# mycursor.execute("SELECT * FROM trades WHERE id = 'main'")
# for x in mycursor:
#     print(x)

# # Query specific
# mycursor.execute("SELECT wt1, wt2 FROM Strategy WHERE id = '9_min'")

# # Alter / Add
# mycursor.execute("ALTER TABLE strategy ADD COLUMN test VARCHAR(50) NOT NULL")

# # Alter / Remove
# mycursor.execute("ALTER TABLE Strategy DROP test")

# # Alter / Change column name

# mycursor.execute("ALTER TABLE Strategy CHANGE name id VARCHAR(50)")

def updateTableValue(table_name, id_name, column_name, value):
    try:
        if (isinstance(value, str)):
            query = "UPDATE " +str(table_name)+ " SET " + str(column_name) + "='" + str(value) + "' WHERE id = '" + str(id_name) + "'"
        else:
            query = "UPDATE " +str(table_name)+ " SET " + str(column_name) + "=" + str(value) + " WHERE id = '" + str(id_name) + "'"
        print(query)
        mycursor.execute(query)
        db.commit()
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))


def updateStratValues(id_name, wt1, wt2, last_candle_high, last_candle_low, last_candle_vwap):
    try:
        query = "UPDATE strategy SET wt1=" +str(wt1)+ ", wt2=" +str(wt2)+ ", last_candle_low=" +str(last_candle_low)+ ", last_candle_high=" +str(last_candle_high)+ ", last_candle_vwap=" +str(last_candle_vwap)+ " WHERE id = '" +str(id_name)+ "'"
        print(query)
        mycursor.execute(query)
        db.commit()
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))  


def updateTradeValues(id_name, symbol, symbol_pair, key_input, limit_price_difference, leverage, input_quantity, data_name):
    try:
        query = "UPDATE trades SET symbol='" +str(symbol)+ "', symbol_pair='" +str(symbol_pair)+ "', key_input=" +str(key_input)+ ", limit_price_difference=" +str(limit_price_difference)+ ", leverage=" +str(leverage)+ ", input_quantity=" +str(input_quantity)+ ", data_name='" +str(data_name)+ "' WHERE id='" +str(id_name)+ "'" 
        print(query)
        mycursor.execute(query)
        db.commit
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))


def viewDbValue(id_name, column_name):
    try: 
        query = "SELECT " + str(column_name) + " FROM strategy WHERE id = '" + str(id_name) + "'"
        test = mycursor.execute(query)
        result = mycursor.fetchall()
        return result[0][0]
    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))


def clearAllTableValues():
    updateTradeValues('main', 'empty', 'empty', 0, 0, 0, 0, 'empty')
    updateStratValues('1_min', 0, 0, 0, 0, 0)
    updateStratValues('9_min', 0, 0, 0, 0, 0)
    updateStratValues('16_min', 0, 0, 0, 0, 0)
    updateStratValues('30_min', 0, 0, 0, 0, 0)

# updateTableValue('trades', 'main', 'leverage', 0)
# updateStratValues('9_min', 0, 0, 0, 0, 0)
# viewDbValues('9_min', 'wt1')
# mycursor.getUpdateCount()
# print(viewDbValues('9_min', 'wt1'))
# test1 = viewDbValues('9_min', 'wt1')
clearAllTableValues()

# updateTradeValues('main', 'BTC', 'BTCUSD', 0, 0.5, 5, 500, 'test')

# clearAllTableValues()

