import json
import urllib.error
import urllib.request

from django.shortcuts import render


def index(request):
    data = {}
    try:
        if request.method == "POST":
            city = request.POST["city"]

            # Using your OpenWeatherMap API key
            api_key = "292b0aaa2a69e046b2e7b78b52fb3fd1"

            # Remove spaces and encode city name
            city = urllib.parse.quote(city.strip())

            # Construct URL with your API key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

            try:
                source = urllib.request.urlopen(url).read()
                list_of_data = json.loads(source)

                data = {
                    "country_code": str(list_of_data["sys"]["country"]),
                    "coordinate": str(list_of_data["coord"]["lon"])
                    + " "
                    + str(list_of_data["coord"]["lat"]),
                    "temp": str(list_of_data["main"]["temp"]) + "k",
                    "pressure": str(list_of_data["main"]["pressure"]),
                    "humidity": str(list_of_data["main"]["humidity"]),
                    "error": False,
                }

            except urllib.error.HTTPError as e:
                if e.code == 401:
                    data["error"] = (
                        "Invalid API key. Please check your OpenWeatherMap API key."
                    )
                elif e.code == 404:
                    data["error"] = f"City '{request.POST['city']}' not found."
                else:
                    data["error"] = f"HTTP Error: {e.code}"

            except urllib.error.URLError as e:
                data["error"] = f"Failed to reach server. Error: {e.reason}"

            except json.JSONDecodeError:
                data["error"] = "Failed to parse weather data"

            except KeyError:
                data["error"] = "Unexpected response format from weather service"

    except Exception as e:
        data["error"] = f"An unexpected error occurred: {str(e)}"

    return render(request, "main/index.html", data)
