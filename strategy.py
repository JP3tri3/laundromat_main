import sys
sys.path.append("..")
# import asyncio
from model.orders import Orders
from model.stop_loss import Stop_Loss
from model.calc import Calc
from api.bybit_api import Bybit_Api
import controller.comms as comms
import database.database as db
import time
import sql_connector as conn

class Strategy():

    orders = Orders()
    sl = Stop_Loss()
    calc = Calc()
    api = Bybit_Api()

    def __init__(self, vwap_margin_neg_input, vwap_margin_pos_input, strat_id_input, trade_id_input):
        global vwap_margin_neg
        global vwap_margin_pos
        global strat_id
        global trade_id
        global last_vwap
        global current_vwap
        global last_trend

        vwap_margin_neg = vwap_margin_neg_input
        vwap_margin_pos = vwap_margin_pos_input
        strat_id = strat_id_input
        trade_id = trade_id_input
        last_vwap = 0.0
        current_vwap = 0.0
        last_trend = ""
        last_candle_wt1 = 0.0
        last_candle_wt2 = 0.0

    #single
    def determineVwapTrend(self):
        global last_vwap
        global current_vwap
        global last_trend

        new_trend = ""
        
        last_Candle_vwap = conn.viewDbValue('strategy', strat_id, 'last_candle_vwap')
        active_trend = conn.viewDbValue('strategy', strat_id, 'active_trend')

        if (last_Candle_vwap != current_vwap):
            last_vwap = current_vwap
            print("")
            print("last_vwap: " + str(last_vwap))
            current_vwap = last_Candle_vwap
            print("current vwap: " + str(current_vwap))

            if(current_vwap >= vwap_margin_pos) and (last_vwap <= vwap_margin_pos):
                new_trend = 'cross_up'
            elif(current_vwap <= vwap_margin_neg) and (last_vwap >= vwap_margin_neg):
                new_trend = 'cross_down'
            elif(current_vwap > 0) and (last_vwap > 0):
                new_trend = 'positive_vwap'
            elif(current_vwap < 0) and (last_vwap < 0):
                new_trend = 'negative_vwap'
            else:
                new_trend = 'not_enough_information'
            
            if (new_trend == 'cross_up') or (new_trend == 'cross_down'):
                if (active_trend != 'null') and (active_trend != new_trend):
                    conn.updateTableValue('strategy', strat_id, 'active_position', 'change')
                if ((last_trend == 'cross_up') and (new_trend == 'cross_down')) or ((last_trend == 'cross_down') and (new_trend == 'cross_up')):
                    conn.updateTableValue('strategy', strat_id, 'new_trend', new_trend)

            print("last_trend: " + str(last_trend))
            print("new_trend: " + str(new_trend))
            conn.updateTableValue('strategy', strat_id, 'new_trend', new_trend)
            last_trend = comms.viewData(data_name, 'new_trend')
            conn.updateTableValue('strategy', strat_id, 'last_trend', last_trend)

    def vwapCrossStrategy(self):
        self.determineVwapTrend()
        new_trend = conn.viewDbValue('strategy', strat_id, 'new_trend')
        conn.updateTableValue('strategy', strat_idid, 'new_trend', 'null')
        last_candle_wt1 = conn.viewDbValue('strategy', strat_id, 'wt1')
        last_candle_wt1 = conn.viewDbValue('strategy', strat_id, 'wt2')
        active_trend = comms.viewData(data_name, 'active_trend')
        active_trend = conn.viewDbValue('strategy', strat_id, 'active_trend')

        if (new_trend != 'null') and (new_trend != active_trend):
            if (new_trend == 'cross_up') or (new_trend == 'cross_down'):
                if (self.orders.activePositionCheck() == 1):
                    print("closing active Position")
                    self.orders.closePositionMarket()
                    comms.logClosingDetails()

                if ((new_trend == 'cross_up') and (last_candle_wt1 < 5) and (last_candle_wt2 < 5)) or (new_trend == 'cross_down') and (last_candle_wt1 > -5) and (last_candle_wt2 > -5):
                    input_quantity = conn.viewDbValue('trades', trade_id, 'input_quantity')
                    if (new_trend == 'cross_up'):
                        print("Opening new Long:")
                        self.orders.createOrder(side='Buy', order_type='Market', input_quantity)

                    elif (new_trend == 'cross_down'):
                        print("Opening new Short:")
                        self.orders.createOrder(side='Sell', order_type='Market', input_quantity)

                    conn.updateTradeValues('strategy', strat_id, 'active_trend', new_trend)
                    conn.updateTradeValues('strategy', strat_id, 'active_position', 'null')
                    #process Stop Loss:
                    print("Checking for stop loss...")
                    flag = True
                    counter = 0
                    tempTime = 60

                    while (flag == True):
                        counter += 1
                        #display counter
                        if (counter == tempTime):
                            counter = 0
                            print("Waiting - Update SL")
                            print("Percent Gained: " + str(self.calc.calcPercentGained()))
                            print("")

                        elif(counter == tempTime/6):
                                print("Percent Gained: " +
                                            str(self.calc.calcPercentGained()))
                                print("Last Price: " + str(self.api.lastPrice()))
                        elif(conn.viewDbValue('strategy', strat_id, 'active_position') == 'change'):
                            flag = False

                        #process SL if position is active
                        else:
                            if(self.orders.activePositionCheck() == 1):
                                self.sl.updateStopLoss('candles')
                                time.sleep(1)
                            else:
                                print("Position Closed")
                                print("")
                                conn.updateTradeValues('strategy', strat_id, 'active_trend', 'null')
                                comms.logClosingDetails()
                                flag = False

                

#check for order of last_trend verse new_trend