import sys
sys.path.append("..")
# import asyncio
from model.orders import Orders
from model.stop_loss import Stop_Loss
from model.calc import Calc
from api.bybit_api import Bybit_Api
import controller.comms as comms
from database.database import Database
import time

class Strategy:

    def __init__(self, vwap_margin_neg_input, vwap_margin_pos_input):
        self.vwap_margin_neg = vwap_margin_neg_input
        self.vwap_margin_pos = vwap_margin_pos_input
        self.last_vwap = 0.0
        self.current_vwap = 0.0
        self.last_trend = ""
        self.last_candle_wt1 = 0.0
        self.last_candle_wt2 = 0.0
        
        self.orders = Orders()
        self.sl = Stop_Loss()
        self.calc = Calc()
        self.api = Bybit_Api()
        self.db = Database()
    
    #single
    def determineVwapTrend(self):
        global last_vwap
        global current_vwap
        global last_trend

        new_trend = ""
        
        last_Candle_vwap = self.db.get_last_vwap()
        active_trend = self.db.get_active_trend()

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
                    self.db.set_active_position('change')
                if ((last_trend == 'cross_up') and (new_trend == 'cross_down')) or ((last_trend == 'cross_down') and (new_trend == 'cross_up')):
                    self.db.set_new_trend(new_trend)

            self.db.set_new_trend(new_trend)
            last_trend = self.db.get_new_trend()
            self.db.set_last_trend(last_trend)

    def vwapCrossStrategy(self):
        self.determineVwapTrend()
        new_trend = self.db.get_new_trend()
        self.db.set_new_trend('null')
        last_candle_wt1 = self.db.get_wt1()
        last_candle_wt2 = self.db.get_wt2()
        active_trend = self.db.get_active_trend()

        if (new_trend != 'null') and (new_trend != active_trend):
            if (new_trend == 'cross_up') or (new_trend == 'cross_down'):
                if (self.orders.activePositionCheck() == 1):
                    print("closing active Position")
                    self.orders.closePositionMarket()
                    comms.logClosingDetails()

                if ((new_trend == 'cross_up') and (last_candle_wt1 < 5) and (last_candle_wt2 < 5)) or (new_trend == 'cross_down') and (last_candle_wt1 > -5) and (last_candle_wt2 > -5):
                    input_quantity = self.db.get_input_quantity()
                    if (new_trend == 'cross_up'):
                        print("Opening new Long:")
                        self.orders.createOrder(side='Buy', order_type='Market', inputQuantity=input_quantity)

                    elif (new_trend == 'cross_down'):
                        print("Opening new Short:")
                        self.orders.createOrder(side='Sell', order_type='Market', inputQuantity=input_quantity)

                    self.db.set_active_trend(new_trend)
                    self.db.set_active_position('null')
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
                        elif(self.db.get_active_position == 'change'):
                            flag = False

                        #process SL if position is active
                        else:
                            if(self.orders.activePositionCheck() == 1):
                                self.sl.updateStopLoss('candles')
                                time.sleep(1)
                            else:
                                print("Position Closed")
                                print("")
                                self.db.set_active_trend('null')
                                comms.logClosingDetails()
                                flag = False


#check for order of last_trend verse new_trend