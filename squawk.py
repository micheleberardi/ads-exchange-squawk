from datetime import datetime
import tweepy
import requests


def twitter(post):
    # all the keys we need for our twitter bot
    CONSUMER_KEY = '<CONSUMER_KEY>'
    CONSUMER_SECRET = '<CONSUMER_SECRET>'
    ACCESS_KEY = '<ACCESS_KEY>'
    ACCESS_SECRET = '<ACCESS_SECRET>'
    # talk to twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(post)

def adsbexchange(squawk):
    url = "https://adsbexchange-com1.p.rapidapi.com/v2/sqk/" + str(squawk) + "/"
    headers = {
        "X-RapidAPI-Key": "<X-RapidAPI-Key>",
        "X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    response = response.json()
    return response
    
def screenshot(url, icao24):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.headless = True
    options.add_argument('window-size=800,800')
    options.add_argument('ignore-certificate-errors')
    # Plane images issue loading when in headless setting agent fixes.
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
    # driver = webdriver.Chrome(DRIVER)
    driver.get(url)
    screenshot = driver.save_screenshot('/images/' + str(icao24) + '.png')
    driver.quit()


if __name__ == '__main__':

    #CODE 7700 = emergency
    #CODE 7600 = communicationfailure
    #CODE 7500 = hijacking

    list_code = ['7500', '7600','7700']
    for squawk in list_code:
        check_squawk = adsbexchange(squawk)
        if check_squawk:
            ac = check_squawk['ac']
            for a in ac:
                hex = a.get('hex', None)
                type = a.get('type', None)
                flight = a.get('flight', None)
                r = a.get('r', None)
                t = a.get('t', None)
                alt_baro = a.get('alt_baro', None)
                gs = a.get('gs', None)
                true_heading = a.get('true_heading', None)
                squawk = a.get('squawk', None)
                emergency = a.get('emergency', None)
                category = a.get('category', None)
                lat = a.get('lat', None)
                lon = a.get('lon', None)
                datenow = datetime.utcnow()
                datenow = datenow.strftime("%Y-%m-%d")
                dateunix = datetime.utcnow()
                unixtime = int(dateunix.timestamp())
                datenowutc = datetime.utcnow("%Y-%m-%d %H:%M:%S")
                url = "https://globe.adsbexchange.com/?icao="+str(hex)+"&lat="+str(lat)+"&lon="+str(lon)+"&zoom=5.0&showTrace="+str(datenow)+"&timestamp="+str(unixtime)
                # CHECK MD5

                if squawk == '7500':
                    tr = "🚨 ADS-B Exchange Emergency Alerts \n ✈️ SQUAWKING " + str(
                        squawk) + " (Communication Failure) \n 🌐 " + str(url) + "\n ⏰ " + str(datenowutc)
                    twitter(tr)
                    print(tr)
                    twitterpost = (str(tr))
                    twitterpost += "\n\n #ADSBExchange #DKAMC"
                    twitterpost = twitterpost
                    twitter(twitterpost)
                elif squawk == '7600':
                    tr = "🚨 ADS-B Exchange Emergency Alerts \n ✈️ SQUAWKING " + str(
                        squawk) + " (Hijacking Failure) \n 🌐 " + str(url) + "\n ⏰ " + str(datenowutc)
                    print(tr)
                    twitterpost = (str(tr))
                    twitterpost += "\n\n #ADSBExchange #DKAMC"
                    twitterpost = twitterpost
                    twitter(twitterpost)

                elif squawk == '7700':
                    tr = "🚨 ADS-B Exchange Emergency Alerts \n ✈️ SQUAWKING " + str(
                        squawk) + " (Emergency) \n 🌐 " + str(url) + "\n ⏰ " + str(datenowutc)
                    print(tr)
                    twitterpost = (str(tr))
                    twitterpost += "\n\n #ADSBExchange #DKAMC"
                    twitterpost = twitterpost
                    twitter(twitterpost)
                else:
                    print("no squawking")
                    pass


        else:
            print("no squawking")
            pass
