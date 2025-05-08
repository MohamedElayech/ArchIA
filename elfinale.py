from toDrawio import json_to_drawio
from prompt import text_to_json
from beded2 import drawio_to_url


user_prompt="Company Y is launching an AI-driven Smart Supply Chain Optimization initiative leveraging predictive analytics, IoT, and machine learning to create a connected network of smart devices for real-time data analysis, predictive maintenance, and optimized production, aiming to boost resilience, enhance quality, reduce downtime and costs, and position itself as a smart manufacturing leader."

def gbt(user_prompt,layers,display):
    parsed_data=text_to_json(user_prompt,layers)

    output_file="jolie.drawio"
    json_to_drawio(parsed_data,output_file,display)
    url=drawio_to_url(output_file)
    return url
# print(gbt(user_prompt,["Application","Business","Strategy"],"dot"))