# create table: #
mycursor.execute("CREATE TABLE Strategy (id VARCHAR(50), wt1 float UNSIGNED, wt2 float UNSIGNED, last_candle_high float UNSIGNED, last_candle_low float UNSIGNED, last_candle_vwap float UNSIGNED, active_position VARCHAR(50), new_trend VARCHAR(50), last_trend VARCHAR(50), active_trend VARCHAR(50))")

mycursor.execute("CREATE TABLE trade (id VARCHAR(50), symbol VARCHAR(50), symbol_pair VARCHAR(50), key_input INT UNSIGNED, limit_price_difference float UNSIGNED, leverage INT UNSIGNED, input_quantity INT UNSIGNED, data_name VARCHAR(50))")

mycursor.execute("CREATE TABLE trade_records (id VARCHAR(50), symbol_pair VARCHAR(50), entry_price FLOAT UNSIGNED, exit_price FLOAT UNSIGNED, stop_loss FLOAT UNSIGNED, percent_gain FLOAT UNSIGNED, dollar_gain FLOAT UNSIGNED, coin_gain FLOAT UNSIGNED, number_of_trades INT UNSIGNED, total_p_l FLOAT UNSIGNED)")

# describe table details: #
mycursor.execute("DESCRIBE Strategy")

for x in mycursor:
    print(x)

# insert into table #
mycursor.execute("INSERT INTO Strategy () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("30_min", 0.0, 0.0, 0.0, 0.0, 0.0, "null", "null", "null", "null"))
db.commit()

mycursor.execute("INSERT INTO trades () VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ('bybit_btcusd_auto_1', 'empty', 'empty', 0, 0.0, 0, 0, 'empty'))
db.commit()
mycursor.execute("SELECT * FROM Strategy")

# Select Query #
 mycursor.execute("SELECT * FROM trades WHERE id = 'main'")
for x in mycursor:
    print(x)

# Select Query specific #
mycursor.execute("SELECT wt1, wt2 FROM Strategy WHERE id = '9_min'")

# Alter / Add #
mycursor.execute("ALTER TABLE strategy ADD COLUMN test VARCHAR(50) NOT NULL")

# Alter / Remove #
mycursor.execute("ALTER TABLE Strategy DROP test")

# Alter / Change column name #
mycursor.execute("ALTER TABLE Strategy CHANGE name id VARCHAR(50)")




# # create table:
# mycursor.execute("CREATE TABLE Strategy (id VARCHAR(50), wt1 float UNSIGNED, wt2 float UNSIGNED, last_candle_high float UNSIGNED, last_candle_low float UNSIGNED, last_candle_vwap float UNSIGNED, active_position VARCHAR(50), new_trend VARCHAR(50), last_trend VARCHAR(50), active_trend VARCHAR(50))")
# mycursor.execute("CREATE TABLE trades (id VARCHAR(50),  strat_id VARCHAR(50), symbol VARCHAR(50), symbol_pair VARCHAR(50), key_input INT UNSIGNED, limit_price_difference FLOAT UNSIGNED, leverage INT UNSIGNED, input_quantity INT UNSIGNED, side VARCHAR(8), stop_loss FLOAT UNSIGNED, percent_gain FLOAT UNSIGNED, trade_record_id INT UNSIGNED)")
# mycursor.execute("CREATE TABLE trade_records (id INT UNSIGNED, symbol_pair VARCHAR(50), entry_price FLOAT UNSIGNED, exit_price FLOAT UNSIGNED, stop_loss FLOAT UNSIGNED, percent_gain FLOAT UNSIGNED, dollar_gain FLOAT UNSIGNED, coin_gain FLOAT UNSIGNED, number_of_trades INT UNSIGNED, side VARCHAR(8), total_p_l FLOAT UNSIGNED)")

# # describe table details:
# mycursor.execute("DESCRIBE Strategy")

# for x in mycursor:
#     print(x)

# # insert into table
# mycursor.execute("INSERT INTO Strategy () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("30_min", 0.0, 0.0, 0.0, 0.0, 0.0, "null", "null", "null", "null"))
# db.commit()

## Insert Column
# mycursor.execute("ALTER TABLE trade_records ADD time VARCHAR(50)")
# db.commit()

# mycursor.execute("INSERT INTO trades () VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ('bybit_auto_1', 'empty', 'empty', 0, 0.0, 0, 0, 'empty'))
# mycursor.execute("INSERT INTO trades () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ('bybit_manual', 'empty', 'empty', 'empty', 0, 0.0, 0, 0, 'empty', 0, 0, 0))
# mycursor.execute("INSERT INTO trades () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ('bybit_auto_1', 'empty', 'empty', 'empty', 0, 0.0, 0, 0, 'empty', 0, 0, 0))
# mycursor.execute("INSERT INTO trades () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ('bybit_auto_2', 'empty', 'empty', 'empty', 0, 0.0, 0, 0, 'empty', 0, 0, 0))
# mycursor.execute("INSERT INTO trades () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ('bybit_auto_3', 'empty', 'empty', 'empty', 0, 0.0, 0, 0, 'empty', 0, 0, 0))

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