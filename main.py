import os

import requests
import tkinter
import tkinter as tk
from dotenv import load_dotenv

load_dotenv()

# You need to set YOUR_API_KEY=api_key to .env file

#https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
selection = ""
users = list()
window = tk.Tk()
cityLabel = tk.Label(window)
weatherLabel = tk.Label(window)
humidityLabel = tk.Label(window)




def get_users():
    req = requests.get("https://jsonplaceholder.typicode.com/users")
    return req.json()
# User Datas

def select_listbox(event):
    global selection
    selection = event.widget.get(event.widget.curselection())
    print(selection)

def get_weather():
    global selection, users
    ix = int(selection.split(",")[0])
    geo = users[ix]["address"]["geo"]
    city = users[ix]["address"]["city"]
    cityLabel.config(text=city)
    api_key = os.getenv("YOUR_API_KEY").strip()
    lat = geo["lat"]
    lon = geo["lng"]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    print(url)
    request = requests.get(url)
    if request.status_code == 200:
        json = request.json()
        print(json)
        weather = str(json["weather"][0]["main"]) + ", " + str("{:.2f}".format(json["main"]["temp"] - 273.15)) + " C"
        weatherLabel.config(text=weather)
        humidityLabel.config(text=str("{:.2f}".format(json["main"]["humidity"])) + " %")
    else:
        weatherLabel.config(text="N/A")
        humidityLabel.config(text="N/A")


def main():
    global window, cityLabel, weatherLabel, users, humidityLabel
    window = tk.Tk()

    window.title("Weather App")

    window.wm_minsize(width=400, height=400)

    list_box = tk.Listbox(window)
    for (ix, user) in enumerate(users):
        list_box.insert(ix, str(ix)+", "+user["name"])

    list_box.bind("<<ListboxSelect>>",select_listbox)
    list_box.pack()

    button = tk.Button(window, text="Get Weather", command=get_weather, font=("Arial", 21))
    button.pack()
    cityLabel = tk.Label(window, text="City Text",font=("Arial", 21))
    cityLabel.pack()
    weatherLabel = tk.Label(window, text ="Weather Text", font=("Arial", 21))
    weatherLabel.pack()
    humidityLabel = tk.Label(window, text ="Humidity Text", font=("Arial", 21))
    humidityLabel.pack()




    window.mainloop()



if __name__ == "__main__":
    users = get_users()
    main()