import urllib.request, json
import requests
import pandas as pd

def npsApiResponse(parkCode):
    r = requests.get(f"https://developer.nps.gov/api/v1/parks?parkCode={parkCode}&api_key=2JOTJFJPkRmsZNcchvTe5h9U933hnE5mFAsGS8cm").json()
    return r

#print(json.dumps(npsApiResponse('bibe').json(),indent=4))

def processArgs():
    parks_df = pd.read_csv("./parks.csv")
    parks_dict = parks_df.to_dict("records")

    for parkD in parks_dict:
        npsResp = npsApiResponse(parkD["Park Code"])['data'][0]
        tempDict = dict()
        tempDict["Description"] = npsResp['description']
        tempDict["Activities"] = [a["name"] for a in npsResp["activities"]]
        #tempDict["Activities"] = ', '.join([a["name"] for a in npsResp["activities"]])
        tempDict["Topics"] = [a["name"] for a in npsResp["topics"]]
        #tempDict["Topics"] = ', '.join([a["name"] for a in npsResp["topics"]])
        tempDict["WeatherInfo"] = npsResp["weatherInfo"]
        parkD.update(tempDict)

    '''parksDf = pd.DataFrame(parks_dict)
    parksDf.assign(Activities=parksDf.Activities.str.split(",")).explode('Activities').to_csv("./parksData.csv",index=False,header=True)'''
    pd.DataFrame(parks_dict).to_csv("./parksData.csv",index=False,header=True)

if __name__ == "__main__":
    processArgs()



