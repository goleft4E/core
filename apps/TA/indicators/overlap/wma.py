import math
from settings import LOAD_TALIB

if LOAD_TALIB:
    import talib

from apps.TA import HORIZONS
from apps.TA.storages.abstract.indicator import IndicatorStorage
from apps.TA.storages.abstract.indicator_subscriber import IndicatorSubscriber
from apps.TA.storages.data.price import PriceStorage
from settings import logger

WMA_LIST = [30, 50, 200,]


class WmaStorage(IndicatorStorage):

    # sorted_set_key = "BTC_USDT:poloniex:WmaStorage:30"

    def produce_signal(self):
        pass


class WmaSubscriber(IndicatorSubscriber):
    classes_subscribing_to = [
        PriceStorage
    ]

    def handle(self, channel, data, *args, **kwargs):

        self.index = self.key_suffix

        if self.index != 'close_price':
            logger.debug(f'index {self.index} is not close_price ...ignoring...')
            return

        periods_list = []
        for s in WMA_LIST:
            periods_list.extend([h * s for h in HORIZONS])

        for periods in set(periods_list):

            # todo: this can be refactored into only one query!
            # todo: after one query for all values, then cut to sizes for horizons and periods
            results_dict = PriceStorage.query(
                ticker=self.ticker,
                exchange=self.exchange,
                index=self.index,
                periods_range=periods
            )

            value_np_array = self.get_values_array_from_query(results_dict, limit=periods)
            if not len(value_np_array):
                return

            wma_value = talib.WMA(value_np_array, timeperiod=periods)[-1]
            if math.isnan(wma_value):
                return
            # logger.debug(f'savingWma value {wma_value}for {self.ticker} on {periods} periods')

            new_wma_storage = WmaStorage(ticker=self.ticker, exchange=self.exchange, timestamp=self.timestamp)
            new_wma_storage.periods = periods
            new_wma_storage.value = float(wma_value)
            new_wma_storage.save()
