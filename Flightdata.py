import requests
import smtplib

API_KEY = "Your tequlila api key"
END_POINT = "https://tequila-api.kiwi.com/"

endpoint = "add your sheety url here"
iata_code_api = "locations/query"

fly_to_var = "COK"  # Enter the iata code here to search flight from
my_email = "Your email"
password = "Authorized password for smtp-lib"

num = 0


def check_stop():
    global num
    check = int(input("How many stopover are you looking for ?"))
    num = check


class FlightData:
    def __init__(self):

        self.api_key = API_KEY
        self.fly_from = "LGA"
        self.fly_to = fly_to_var
        self.date_from = "01/08/2022"
        self.date_to = "01/10/2022"
        self.end_point = END_POINT
        self.query = {
            "fly_from": "LON",
            "fly_to": fly_to_var,
            "date_from": "16/08/2022",
            "date_to": "16/12/2022",
            "curr": "GBP",

        }
        self.header = {
            "apikey": "key for header"
        }

        self.params = {
            "Content-Type": "application/json",
        }

    def get_iata_code(self):

        res = requests.get(url=endpoint, headers=self.params)
        sheet_data = res.json()["prices"]

        for index in range(0, 1):
            low_actual = sheet_data[index]["lowest"]
            term = {
                "term": sheet_data[index]["city"]
            }
            responses = requests.get(url=END_POINT + iata_code_api, params=term, headers=self.header)
            city = responses.json()["locations"][0]["code"]

            print(city)

            data_2 = {
                "price": {
                    "name": "Nikhil PN",
                    "email": "your email",
                    "code": city,

                }
            }  # SHeety url for to recieve data from the api
            responses_put = requests.put(url=f"https://api.sheety.co/6313e2538879303457d1bd0393933722/"
                                             f"copyOfCopyOfFlightDeals/prices/{index + 2}", json=data_2,
                                         headers=self.params)

            query = {
                "fly_from": "LON",
                "fly_to": city,
                "date_from": "16/08/2022",
                "date_to": "16/12/2022",
                "curr": "GBP",
                "max_stopovers": num,
                "max_sector_stopovers": 1,

            }

            responses = requests.get(url="https://tequila-api.kiwi.com/v2/search?", params=query, headers=self.header)
            print(responses.status_code)
            try:
                lowest_price = responses.json()["data"][3]["price"]
            except IndexError:
                print("No flight")
                check_stop()

                self.get_iata_code()

            else:
                if lowest_price < low_actual:
                    print(f"low price on flight to,{city} for {lowest_price}")

                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(user=my_email, password=password)
                        connection.sendmail(from_addr=my_email,
                                            to_addrs="to the address to be sent",
                                            msg=f"Subject:Low price on flight to {city}\n\n There is a Low price on "
                                                f"flight to {city} for GBP {lowest_price}"
                                            )

                json_lowest = {
                    "price": {
                        "name": "Nikhil PN",
                        "email": "nikhilpn360@gmail.com",
                        "lowest": lowest_price,

                    }
                }

                responses_low_put = requests.put(url=f"https://api.sheety.co/6313e2538879303457d1bd0393933722/"
                                                     f"copyOfCopyOfFlightDeals/prices/{index + 2}", json=json_lowest,
                                                 headers=self.params)
                print(responses_low_put)

    def email_all(self):
        my_email = "your email"
        password = "your password"

        # add your details custom sheety chart here.
        respones = requests.get(url="https://api.sheety.co/6313e2538879303457d1bd0393933722/"
                                    "copyOfCopyOfFlightDeals/users", headers=self.params)
        # the collection of email data
        email_data = respones.json()["users"]

        respones = requests.get(url="https://api.sheety.co/6313e2538879303457d1bd0393933722/"
                                    "copyOfCopyOfFlightDeals/prices", headers=self.params)

        price_data = respones.json()["prices"]
        data = ""
        for index in range(0, len(price_data)):
            val = price_data[index]["city"] + " " + str(price_data[index]["lowest"])
            data += val + "\n"

        for index in range(0, len(email_data)):
            client_email = email_data[index]["emails"]
            with smtplib.SMTP("smtp.gmail.com") as connection:
                print("send")
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs=client_email,
                                    msg=f"Subject:Low price on flights list Updated \n\nCheck the"
                                        f" following lists{data}")
