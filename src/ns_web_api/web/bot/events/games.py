from models import Eprice,CountryCurrency
from rate import CurrencyRate

class GamesEvent(object):
    """ 遊戲事件
    """

    def __init__(self):
        pass

    def occurs(self, message):
        """遊戲事件觸發
        """
        print("parameter message is: {0}".format(message))

        if not message:
            return
            
        if "找" in message:
            idx = message.index('找')
            if len(message) > idx:
                game_name = "".join(message[idx+1:])
                items = Eprice.query.filter(Eprice.name == game_name)
                if items:
                    currency_rate = CurrencyRate()
                    reply_message = "{0}: 有以下價格\n".format(game_name)
                    for item in items:
                        currency = ""

                        if item.currency_specified:
                            currency = item.currency_specified
                        else:
                            country = CountryCurrency.query.filter(CountryCurrency.country == item.country).first()
                            if country:
                                currency = country.currency
                        
                        if currency:
                            item.eprice = item.eprice * currency_rate.caculate_rate(currency, 'TWD')
                        
                        reply_message += "[{country}: {eprice:.0f}]\n".format(country=item.country, eprice=item.eprice)

                    return reply_message
                    

            # 中了
            print("game-找")
            
        elif "玩" in message:
            print("game-玩")
        
        return
