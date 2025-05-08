from openai import OpenAI
import json
import json
from toDrawio import json_to_drawio  # import the function
from jsonformat import formattt
user_prompt = """
    Domain: Manufacturing & Logistics
    In response to evolving market demands, Company Y aims to modernize its supply chain through an AI-driven Smart Supply Chain Optimization initiative. This project will harness predictive analytics, IoT, and machine learning to streamline production and distribution, increase transparency, and reduce operational costs. The primary goals include boosting supply chain resilience, enhancing product quality, and minimizing downtime.
    The initiative will establish an interconnected network of smart devices and sensors within production facilities to capture real-time data on inventory levels, equipment performance, and delivery schedules. A central analytics platform will then process this data to predict demand, optimize production schedules, and prevent bottlenecks. Additionally, IoT-enabled predictive maintenance will be used to minimize machinery breakdowns, reducing unplanned downtime.
    This transformation will help Company Y achieve faster turnaround times, lower production costs, and greater flexibility in responding to fluctuations in customer demand. Success will be measured by reduced lead times, increased production efficiency, and lower operating expenses, positioning the company as a leader in smart manufacturing."""




def text_to_json(user_prompt,selected_layers):

    
    # Define the system prompt
    system_prompt = "You are an archimate expert. Generate structured JSON output for an ArchiMate model, covering all existing layers. ONLY EXISTING LAYERS SHALL BE INCLUDED.  You will receive an enterprise description from the user and you should turn it into the json format given to you.The ids must be distinct between all elements event those of different layers"

    # Define the user prompt
    

    client = OpenAI()

    # Call OpenAI API with function calling
    completion = client.chat.completions.create(
        model="gpt-4.1",  # Use a valid model name
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        functions=formattt,
        function_call={"name": "generate_archimate_model"}  # Force the model to use the function
    )
    if selected_layers == "all":
        selected_layers = ["Motivation","Strategy","Business","Application","Technology"]

    if completion.choices[0].message.function_call:
        structured_json = completion.choices[0].message.function_call.arguments
        parsed_data = json.dumps(json.loads(structured_json), indent=4)
        filtered_layers = []
        data = json.loads(structured_json)
        for layer in data["layers"]:
            if layer["layer"] in selected_layers:
                filtered_layers.append(layer)
        print(json.dumps({"layers": filtered_layers}))
        return json.dumps({"layers": filtered_layers})


    else:
        print("No function call found in the response.")

