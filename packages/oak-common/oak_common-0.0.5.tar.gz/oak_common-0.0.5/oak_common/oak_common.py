# -*- coding: utf-8 -*-
# from __future__ import annotations
import pymysql
import pandas as pd
import datetime
from sqlalchemy import create_engine
from pandas.core.api import DataFrame
from concurrent.futures import ProcessPoolExecutor, as_completed



class OakCommon():
    def __init__(self):
        self.host = "192.168.2.231"
        self.user = "oak_general"
        self.password = "Oak_12()"
        self.db = "oak_common"
        self.port = 3306
        self.charset = "utf8mb4"

    def get_db_connect(self, times=1):
        try:
            conn = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.db, port=self.port, charset=self.charset)
            return conn
        except Exception as e:
            print(f"Connect to the database({self.host}) failed, trying to connect {times} times")
            if times < 5:
                times += 1
                return self.get_db_connect(times)
        return None
    
    def get_db_engine(self):
        url_str = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"#?charset={self.charset}"
        engine = create_engine(url_str)

        return engine


    def __today(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')


    def get_tradingdays(self, start_day, end_day):
        """
        get trading day list.

        Parameters:
        start_day <str> yyyy-mm-dd 
        end_day <str> yyyy-mm-dd
        
        Returns:
            error <object>
            tradingday list <dateframe>
        """
        try:
            engine = self.get_db_engine()
            sql=(
                "select "
                "calendarday as tradingday, "
                "pre_tradingday "
                "from "
                "comm_calendar "
                "where "
                "calendarday >= %(start_day)s "
                "and calendarday <= %(end_day)s "
                "and iftrading=1 "
            )
            
            rts = pd.read_sql(sql,engine,params={"start_day": start_day,"end_day": end_day})

            return None,rts
        except Exception as e:
            return e,None

    def get_trading_win(self, tradingday, win=[-5,5]):
        """
        get before and after tradingdays on the entered tradingday.

        Parameters:
        tradingday <str> yyyy-mm-dd 
        win <lsit> [-5,5]
        
        Returns:
            error <object>
            tradingday list <dateframe>
        """
        try:
            start_sqe,end_seq = win
            engine = self.get_db_engine()
            sql=(
                "select "
                "calendarday as tradingday, "
                "tradingday_seq-pseq as seq, "
                "pre_tradingday "
                "from "
                "comm_calendar a, "
                "(select tradingday_seq pseq "
                "from comm_calendar "
                "where calendarday = %(tradingday)s "
                "and iftrading = 1) b "
                "where "
                "a.tradingday_seq >= b.pseq + %(start_sqe)s "
                "and a.tradingday_seq <= b.pseq + %(end_seq)s "

            )


            rts = pd.read_sql(sql,engine,params={"tradingday": tradingday,"start_sqe": start_sqe,"end_seq": end_seq})

            return None,rts
        except Exception as e:
            return e,None


    def get_pre_tradingday(self, day):
        """
        get previous tradingday.

        Parameters:
        day <str> yyyy-mm-dd 
        
        Returns:
            error <object>
            previous tradingday <str>
        """
        try:
            conn = self.get_db_connect()
            cursor = conn.cursor()
            sql=(
                "select "
                "pre_tradingday "
                "from "
                "comm_calendar "
                "where "
                "calendarday = %s "
            )
            row_count = cursor.execute(sql,day)
            rts = cursor.fetchall()
            pre_tradingday = datetime.date.strftime(rts[0][0], '%Y-%m-%d')

            cursor.close()
            conn.close()

            return None,pre_tradingday
            
        except Exception as e:
            # if conn:
            #     conn.close()
            return e,None

    # is_tradingday、is_weekend、is_monthend
    def is_tradingday(self, day,method = "is_tradingday"):
        """
        enter date is a [tradingday,weekend tradingday,monthend tradingday].

        Parameters:
        day <str> yyyy-mm-dd 
        method<str> is_tradingday、is_weekend、is_monthend
        
        Returns:
            error <object>
            flag <boole>
        """
        flag = False
        try:

            conn = self.get_db_connect()
            sql=(
                "select "
                "calendarday "
                "from "
                "comm_calendar "
                "where "
                "calendarday = %s "
            )
            if method == "is_tradingday":
                sql = sql + " and iftrading = 1 "
            elif method == "is_weekend":
                sql = sql + " and ifweekend = 1 "
            elif method == "is_monthend":
                sql = sql + " and ifmonthend = 1 "
            else:
                sql = sql + " and iftrading = 1 "

            cursor = conn.cursor()
            row_count = cursor.execute(sql,day)
            if row_count>0:
                flag = True

            cursor.close()
            conn.close()
            
            return None,flag
        except Exception as e:

            # if conn:
            #     conn.close()
            return e,None


    def comm_query_pd(self,sql):
        try:
            engine = self.get_db_engine()
            rts = pd.read_sql(sql,engine)

            return rts
        except Exception as e:
            raise e


    @staticmethod
    def get_periods_date(start_date, end_date, freq='15D'):
        """
        get periods dates between start_date and end_date

        Parameters
        ---------
        start_date: <str> yyyy-mm-dd 
        end_date: <str> yyyy-mm-dd 
        freq: <str> 

        Returns
        ------
        periods_dates: <list>
        
        """
        periods_dates = pd.period_range(start=start_date, end=end_date, freq=freq).map(
            lambda x: (x.start_time.strftime('%Y-%m-%d'), x.end_time.strftime('%Y-%m-%d'))).tolist()
        periods_dates[-1] = (periods_dates[-1][0], end_date)
        return periods_dates

    
    def _get_dailyquote_stock(self, start_date, end_date, stock_code=None, indexs=None, fields=('*',)):
        '''
        get the dailyquote between the start_date and end_date

        Parameters
        ----------
        start_date: <str> yyyy-mm-dd 
        end_date: <str> yyyy-mm-dd 
        stock_code: <str> or <tuple> 'SH600000' or ('SH600000', 'SH600007')
        indexs: <str> or <tuple> 'SH000300' or ('SH000300', 'SH000852')
        fields : <tuple> or <list> ['stock_code', 'tradingday'] or ('stock_code', 'tradingday')

        Returns
        -------
            error: <object>
            rts: <DataFrame>
        '''
        try:
            engine = self.get_db_engine()
            sql=(
                "select "
                f"{', '.join(fields)} "
                "from "
                "daily_quote_stock_rq "
                "where "
                "tradingday BETWEEN %(start_date)s "
                "and %(end_date)s "
            )

            if stock_code:
                if isinstance(stock_code, str):
                    stock_code = (stock_code, )
                sql += "and stock_code in %(stock_code)s "
            if indexs:
                if isinstance(indexs, (list, tuple)):
                    sql += 'and ('
                    sql += 'or '.join([f'{field}=1 '.upper().replace('SH', 'is_') for field in indexs])
                    sql += ')'
                else:
                    sql += f' and {indexs}=1'.upper().replace('SH', 'is_')
            rts = pd.read_sql(sql, engine, params={"start_date": start_date, "end_date": end_date, 'stock_code':stock_code})
            return None, rts
        except Exception as e:
            print(e)
            return e, None

    def get_dailyquote_stock(self, start_date, end_date=None, stock_code=None, indexs=None, fields=('*',), maxprocess=1):
        '''
        get the dailyquote by processpool 

        Parameters
        ----------
        start_date: <str> yyyy-mm-dd 
        end_date: <str> yyyy-mm-dd 
        stock_code: <str> or <tuple> 'SH600000' or ('SH600000', 'SH600007')
        indexs: <str> or <tuple> 'SH000300' or ('SH000300', 'SH000852')
        fields : <tuple> or <list> ['stock_code', 'tradingday'] or ('stock_code', 'tradingday')
        maxprocess: <int>

        Returns
        -------
            error : <object> or
            rts : <DataFrame>
        '''
        assert start_date, 'start_date is required'
        assert not (stock_code and indexs), "(stock_code, indexs) only one param is required"
        assert isinstance(maxprocess, int) and (maxprocess>0), 'maxprocess must be a positive int number'
        assert isinstance(fields, (tuple, list)), 'params fileds must be a tuple or a list'
        if not end_date: end_date = start_date
        if maxprocess != 1:
            try:
                dates = self.get_periods_date(start_date, end_date)
                with ProcessPoolExecutor(max_workers=maxprocess) as executor:
                    tasks = [executor.submit(self._get_dailyquote_stock, start_date, end_date, stock_code, indexs, fields) for start_date, end_date in dates]
                    datas = [ task.result()[1] for task in as_completed(tasks) if isinstance(task.result()[1], DataFrame)]
                    rts = pd.concat(datas)
                    rts.reset_index(drop=True, inplace=True)
                return None, rts
            except Exception as e:
                print(e)
                return e, None
        else:
            return self._get_dailyquote_stock(start_date, end_date, stock_code, indexs, fields)


    def get_dailyquote_index(self, start_date, end_date=None, stock_code=None):
        '''
        get the index dailyquote 

        Parameters
        ----------
        start_date: <str> yyyy-mm-dd 
        end_date: <str> yyyy-mm-dd 
        stock_code: <str> or <tuple> 'SH000300' or ('SH000300', 'SH000852')
        
        Returns
        -------
            error: <object>
            rts: <DataFrame>
        '''
        assert start_date, 'start_date is required'
        if not end_date: end_date = start_date
        try:
            engine = self.get_db_engine()
            sql=(
                "select "
                "* "
                "from "
                "daily_quote_index_rq "
                "where "
                "tradingday >= %(start_date)s "
                "and tradingday <= %(end_date)s "
            )

            if stock_code:
                if isinstance(stock_code, str):
                    stock_code = (stock_code, )
                sql += "and stock_code in %(stock_code)s "
            rts = pd.read_sql(sql, engine, params={"start_date": start_date, "end_date": end_date, 'stock_code':stock_code})
            return None, rts
        except Exception as e:
            return e, None

    
    def _get_risk_factor(self, start_date, end_date=None, stock_code=None):
        '''
        get the risk_factor 

        Parameters
        ----------
        start_date: <str> yyyy-mm-dd 
        end_date: <str> yyyy-mm-dd 
        stock_code: <str> or <tuple> 'SH000300' or ('SH000300', 'SH000852')
        
        Returns
        -------
            error: <object>
            rts: <DataFrame>
        '''
        try:
            engine = self.get_db_engine()
            sql=(
                "select "
                "* "
                "from "
                "risk_factor_exposure "
                "where "
                "tradingday >= %(start_date)s "
                "and tradingday <= %(end_date)s "
            )

            if stock_code:
                if isinstance(stock_code, str):
                    stock_code = (stock_code, )
                sql += "and stock_code in %(stock_code)s "
            rts = pd.read_sql(sql, engine, params={"start_date": start_date, "end_date": end_date, 'stock_code':stock_code})
            return None, rts
        except Exception as e:
            return e, None


    def get_risk_factor(self, start_date, end_date=None, stock_code=None, maxprocess=1):
        '''
        get the risk_factor processpool 

        Parameters
        ----------
        start_date: <str> yyyy-mm-dd 
        end_date: <str> yyyy-mm-dd 
        stock_code: <str> or <tuple> 'SH000300' or ('SH000300', 'SH000852')
        maxprocess: <int>
        Returns
        -------
            error: <object>
            rts: <DataFrame>
        '''
        assert start_date, 'start_date is required'
        assert isinstance(maxprocess, int) and (maxprocess>0), 'maxprocess must be a positive int number'
        if not end_date: end_date = start_date
        if maxprocess != 1:
            try:
                dates = self.get_periods_date(start_date, end_date)
                with ProcessPoolExecutor(max_workers=maxprocess) as executor:
                    tasks = [executor.submit(self._get_risk_factor, start_date, end_date, stock_code) for start_date, end_date in dates]
                    datas = [ task.result()[1] for task in as_completed(tasks) if isinstance(task.result()[1], DataFrame)]
                    rts = pd.concat(datas)
                    rts.reset_index(drop=True, inplace=True)
                return None, rts
            except Exception as e:
                return e, None
        else:
            return self._get_risk_factor(start_date, end_date, stock_code)

    
    def get_explicit_factor_return(self, start_date, end_date=None):
        '''
        获取显性因子收益率
        显性因子收益率-每个风格因子做完市值中性化之后，计算多空对冲收益

        Parameters
        ----------
        start_date: <str> yyyy-mm-dd 
        end_date: <str> yyyy-mm-dd default=today
        Returns
        -------
            error: <object> return error message
            rts: <DataFrame> return the result
        '''
        assert start_date, 'start_date is required'
        end_date = end_date or self.__today()
        try:
            engine = self.get_db_engine()
            sql=(
                "select "
                "* "
                "from "
                "factor_return_explicit "
                "where "
                "tradingday between %(start_date)s "
                "and %(end_date)s "
            )
            rts = pd.read_sql(sql, engine, params={"start_date": start_date, "end_date": end_date})
            return None, rts
        except Exception as e:
            return e, None

    
    def get_implicit_factor_return(self, start_date, end_date=None):
        '''
        获取隐性因子收益率
        隐性因子收益率-单日股票收益和多个风格因子多元回归，获得因子的回归系数即为隐性因子收益率

        Parameters
        ----------
        start_date: <str> yyyy-mm-dd 
        end_date: <str> yyyy-mm-dd default=today
        Returns
        -------
            error: <object> return error message
            rts: <DataFrame> return the result
        '''
        assert start_date, 'start_date is required'
        end_date = end_date or self.__today()
        try:
            engine = self.get_db_engine()
            sql=(
                "select "
                "* "
                "from "
                "factor_return_implicit "
                "where "
                "tradingday between %(start_date)s "
                "and %(end_date)s "
            )
            rts = pd.read_sql(sql, engine, params={"start_date": start_date, "end_date": end_date})
            return None, rts
        except Exception as e:
            return e, None


    def _get_special_return(self, start_date, end_date=None, stock_code=None):
        try:
            engine = self.get_db_engine()
            sql=(
                "select "
                "* "
                "from "
                "specific_return "
                "where "
                "tradingday between %(start_date)s "
                "and %(end_date)s "
            )

            if stock_code:
                if isinstance(stock_code, str):
                    stock_code = (stock_code, )
                sql += "and stock_code in %(stock_code)s "
            rts = pd.read_sql(sql, engine, params={"start_date": start_date, "end_date": end_date, 'stock_code':stock_code})
            return None, rts
        except Exception as e:
            return e, None


    def get_special_return(self, start_date, end_date=None, stock_code=None, maxprocess=1):
        '''
        获取特异收益率
        特异收益率-单日股票收益和多个风格因子多元回归，获得残差项（风格因子无法解释的收益）

        Parameters
        ----------
        start_date: <str> yyyy-mm-dd 
        end_date: <str> yyyy-mm-dd default=today
        Returns
        -------
            error: <object> return error message
            rts: <DataFrame> return the result
        '''
        assert start_date, 'start_date is required'
        assert not stock_code or (stock_code and isinstance(stock_code, (str, tuple, list))), 'stock_code must be string or tuple or list'
        assert isinstance(maxprocess, int) and (maxprocess>0), 'maxprocess must be a positive int number'
        end_date = end_date or self.__today()
        dates = self.get_periods_date(start_date, end_date)
        if maxprocess != 1:
            try:
                with ProcessPoolExecutor(max_workers=maxprocess) as executor:
                    tasks = [executor.submit(self._get_special_return, start_date, end_date, stock_code) for start_date, end_date in dates]
                    datas = [ task.result()[1] for task in as_completed(tasks) if isinstance(task.result()[1], DataFrame)]
                    rts = pd.concat(datas)
                    rts.reset_index(drop=True, inplace=True)
                return None, rts
            except Exception as e:
                return e, None
        else:
            return self._get_special_return(start_date, end_date, stock_code)


    def get_fut_daily_quote(self, start_date, end_date=None, fields=('*',)):
        '''
        获取期货行情数据
        Parameters
        ----------
        start_date: <str> yyyy-mm-dd 查询开始日期
        end_date: <str> yyyy-mm-dd 查询结束日期, 默认等于开始查询日期
        fields: <list> or <tuple> 查询返回字段, 默认返回所有
        Returns
        -------
            error: <object> return error message
            rts: <DataFrame> return the result
        '''
        assert start_date, 'start_date is required'
        assert isinstance(fields, (tuple, list)), 'params fileds must be a tuple or a list'
        end_date = end_date or start_date

        try:
            conn = self.get_db_connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql=(
                "select "
                f"{', '.join(fields)} "
                "from "
                "Fut_Daily_Quote_RQ "
                "where "
                "tradingday between %s "
                "and %s "
            )
            row_count = cursor.execute(sql, (start_date, end_date))
            rts = cursor.fetchall()
            cursor.close()
            conn.close()
            if row_count: 
                return None, DataFrame(rts)
            return None, DataFrame()
        except Exception as e:
            return e, None



if __name__ == "__main__":
    ocdb = OakCommon()
    # err,tmp = ocdb.get_tradingdays("2022-01-01","2022-05-05")
    # err,tmp = ocdb.is_tradingday("2022-01-28","is_monthend")
    # err,tmp = ocdb.get_trading_win("2022-01-28",[-20,-10])
    # print(tmp)
    # err,tmp = ocdb.get_pre_tradingday("2022-01-28")
    # print(tmp)

    import time

    t1 = time.perf_counter()
   
    #err, tmp = ocdb.get_dailyquote_stock("2022-01-01","2022-11-30", indexs=('SH000300', 'SH000852'), fields=('stock_code', 'tradingday'), maxprocess=10)
    # err, tmp = ocdb.get_risk_return("2014-01-01","2022-10-27", maxprocess=10)
    #err, tmp = ocdb.get_implicit_return("2014-01-01")
    # err, tmp = ocdb.get_special_return('2020-01-01', '2023-01-09', maxprocess=10)
    err, tmp = ocdb.get_fut_daily_quote('2023-03-20', '2023-03-30', fields=('order_book_id', 'end_delivery_date'))
    t2 = time.perf_counter()
    print(t2 - t1)
    print(err)
    print(tmp)

    # err, tmp = ocdb.get_dailyquote_index("2022-05-01","2022-07-06", ('SH000906', 'SH000852'))
    # print(tmp)