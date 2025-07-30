import json
from pathlib import Path 
import os 
import asyncio
import pandas as pd 

CONFIG = json.load(open("config.json","r", encoding='utf‑8'))


#Save to CSV
async def save_to_csv(list_df, filename):
    Path(CONFIG["OUTPUT_DIR"]).mkdir(exist_ok=True)
    filepath = os.path.join(CONFIG["OUTPUT_DIR"], filename)

    df = pd.DataFrame(list_df)
    #Save data
    df.to_csv(filepath)

async def get_page_url(page_num=None):
    if page_num and page_num < 10:
        return CONFIG['URL']+f"/page/{page_num}"+CONFIG['SEARCH_PAGE']
    else:
        return CONFIG['URL'] + CONFIG['SEARCH_PAGE']
