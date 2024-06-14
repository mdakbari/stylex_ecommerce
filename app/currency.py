import everapi

# akhu badu band  karvu padse ..
class Client(everapi.Client):
    def __init__(self, api_key, base='https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_YmDDOQ53V2ORAoTPnzY4M8vJOBhlmqbFi6NNmUBp'):
        super(Client, self).__init__(base, api_key)

    def status(self):
        return self._request('/status')

    def currencies(self, currencies=[]):
        if type(currencies) is not list:
            raise Exception("Currencies needs to be a list")

        return self._request('/currencies', params={
            'currencies': self._list_to_comma_seperated(currencies)
        })

    def latest(self, base_currency=None, currencies=[]):
        if type(currencies) is not list:
            raise Exception("Currencies needs to be a list")

        return self._request('/latest', params={
            'base_currency': base_currency,
            'currencies': self._list_to_comma_seperated(currencies)
        })

    def historical(self, date, base_currency=None, currencies=[]):
        if type(currencies) is not list:
            raise Exception("Currencies needs to be a list")

        return self._request('/historical', params={
            'date': date,
            'base_currency': base_currency,
            'currencies': self._list_to_comma_seperated(currencies)
        })

    def _list_to_comma_seperated(self, lst):
        return ','.join(lst)

class INRToUSDConverter:
    def __init__(self, api_key):
        # Instantiate the client with the provided API key
        self.client = Client(api_key)

    def convert_inr_to_usd(self, amount_inr):
        # Get the latest exchange rates for INR to USD
        response = self.client.latest(base_currency='INR', currencies=['USD'])
        
        # Print the entire response for inspection
        # print(respsonse)

        # Extract the exchange rate from the response
        # Modify this part based on the actual structure of the response
        data = response.get('data', {})
        exchange_rate = data.get('USD')
        # Check if exchange_rate is None or not before proceeding
        if exchange_rate is None:
            print("Error: Unable to retrieve exchange rate.")
            return None

        # Convert the amount from INR to USD
        amount_usd = amount_inr * exchange_rate
        return amount_usd
