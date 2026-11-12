import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Forex API is live! Visit /rates to see MYR pairs."
    }

@app.get("/rates")
async def get_forex_rates():
    url = "https://frankfurter.dev"
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            response = await client.get(url)
            
        if response.status_code != 200:
            raise HTTPException(
                status_code=502, 
                detail=f"Frankfurter API error ({response.status_code}): {response.text}"
            )
            
        data = response.json()
        
        if not data or not isinstance(data, list):
            raise HTTPException(status_code=502, detail=f"Unexpected API response: {data}")
            
        # Map the list of quote objects into a dictionary
        rates = {item["quote"]: item["rate"] for item in data}
        
        # Grab the date from the first item in the list
        date = data[0].get("date", "unknown")
        
        return {
            "date": date,
            "base": "MYR",
            "pairs": {
                "USD/MYR": round(1 / rates["USD"], 4),
                "GBP/MYR": round(1 / rates["GBP"], 4),
                "JPY/MYR": round(1 / rates["JPY"], 6),
                "100_JPY/MYR": round((1 / rates["JPY"]) * 100, 4)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

