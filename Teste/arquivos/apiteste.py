import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"

querystring = {"region":"US","symbols":"AMD,IBM,AAPL"}

headers = {
	"x-rapidapi-key": "", #TODO Substitua pela sua chave
	"x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring, verify=False)

print(response.json())