import requests
import json
import urllib.parse

def whether_api(city_name):
    
    response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json')
    latitude = response.json()['results'][0]['latitude']
    longitude = response.json()['results'][0]['longitude']

    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true')
    
    return response.json()['current_weather']



def wikipedia_search(query):
    """
    Fetch a summary from Wikipedia for a given query.
    """

    # Format the query for URL and add User-Agent Header
    formatted_query = urllib.parse.quote(query.replace(" ", "_"))
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + formatted_query
    headers = {
        'User-Agent': 'TusharAI/1.0 (test@example.com) python-requests'
    }

    try:
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            return json.dumps({"error": f"Wikipedia returned status code {response.status_code}"})
            
        data = response.json()

        
        # print('data',data)
        if "extract" in data:
            return json.dumps({
                "title": data.get("title"),
                "summary": data.get("extract")
            })

        else:
            return json.dumps({
                "error": "No Wikipedia page found for this query"
            })

    except Exception as e:
        return json.dumps({
            "error": str(e)
        })    


tools = [
    {
        "whether_api":{
            'fn':whether_api,
            'description':'Get the current weather for a city',
            'parameters':{
                'city_name': 'string'
            }
        },
        "wiki_search": {
            "desc": "Search Wikipedia and return a short summary for a topic",
            "fn": wikipedia_search,
            "parameters":{  
                "query": "string"
            }
        }   
    }
]

# print(wikipedia_search("UFC"))

