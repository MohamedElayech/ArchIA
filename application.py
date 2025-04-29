from flask import Flask, request, jsonify, render_template, send_from_directory
from flask import send_file
from flask_cors import CORS
import os
from flask import Flask, jsonify, request
import json
import re
from openai import OpenAI
import os
from plantuml import PlantUML
client = OpenAI()
import subprocess
import zlib
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


relationships = {
    "composed of": "Composition",
    "composed in": "Composition",
    "composes": "Composition",  # added
    "composition": "Composition",  # added

    "aggregates": "Aggregation",
    "aggregated in": "Aggregation",
    "aggregated by": "Aggregation",  # added
    "aggregation": "Aggregation",  # added

    "assigned to": "Assignment",
    "has assigned": "Assignment",
    "assigns": "Assignment",
    "assignment": "Assignment",

    "realizes": "Realization",
    "realized by": "Realization",
    "realization": "Realization",  # added

    "serves": "Serving",
    "serving": "Serving",
    "served by": "Serving",
    "service": "Serving",  # optional alias

    "accesses": "Access",
    "accessed by": "Access",
    "access": "Access",

    "influences": "Influence",
    "influenced by": "Influence",
    "influence": "Influence",

    "associated with": "Association",
    "associated to": "Association",
    "associated from": "Association",
    "associates": "Association",  # added
    "association": "Association",  # added

    "triggers": "Triggering",
    "triggered by": "Triggering",
    "triggering": "Triggering",
    "trigger": "Triggering",  # added

    "flows to": "Flow",
    "flows from": "Flow",
    "flows": "Flow",  # added
    "flow": "Flow",  # added

    "specializes": "Specialization",
    "specialized by": "Specialization",
    "specialization": "Specialization",  # added
}



key_elements = {
    "Motivation": [
        "Stakeholder", "Driver", "Assessment", "Goal", "Outcome", "Principle",
        "Requirement", "Constraint", "Meaning", "Value"
    ],
    "Strategy": [
        "Resource", "Capability", "Value Stream", "Course of Action"
    ],
    "Business": [
        "Business Actor", "Business Role", "Business Collaboration", "Business Interface",
        "Business Process", "Business Function", "Business Interaction", "Business Event",
        "Business Service", "Business Object", "Contract", "Representation", "Product"
    ],
    "Application": [
        "Application Component", "Application Collaboration", "Application Interface",
        "Application Function", "Application Interaction", "Application Process",
        "Application Event", "Application Service", "Data Object"
    ],
    "Technology": [
        "Node", "Device", "System Software", "Technology Collaboration", "Technology Interface",
        "Path", "Communication Network", "Technology Function", "Technology Process",
        "Technology Interaction", "Technology Event", "Technology Service", "Artifact",
        "Equipment", "Facility", "Distribution Network", "Material"
    ]
}

def generate_json_text(test):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": "You are a specialized assistant for extracting layers and their key elements from enterprise architecture descriptions."},
            
            {
                "role": "user",
                "content": test
            },
            
            {
                "role": "assistant",
                "content": "Analyze the provided enterprise architecture description and identify which layer it describes (e.g., Business Layer, Application Layer, Motivation Layer, etc.). Extract only the key elements for that layer based on the description provided. Do not assume any elements are present unless explicitly mentioned in the description.The key element name shouldn't contain the name of the layer. the id of each element should containes only characters and numbers "
                "{\n"
                '    "architecture": "<project name>",\n'
                '    "layers": [\n'
                '        {\n'
                '            "layer": "<Identified Layer>",\n'
                '            "elements": [\n'
                '                {\n'
                '                    "type": "<Element Type>",\n'
                '                    "subElements": [\n'
                '                        {\n'
                '                            "id": "<Unique ID>",\n'
                '                            "name": "<Extracted Element Name>",\n'
                '                            "description": "<Description of the Element>"\n'
                '                        }\n'
                '                    ]\n'
                '                }\n'
                '            ],\n'
                '            "element-relationship": [\n'
                '                {\n'
                '                    "from": {\n'
                '                        "id": "<Source Element ID>",\n'
                '                        "type": "<Source Type>"\n'
                '                    },\n'
                '                    "to": {\n'
                '                        "id": "<Target Element ID>",\n'
                '                        "type": "<Target Type>"\n'
                '                    },\n'
                '                    "type": "<Original Relationship Phrase>"\n'
                '                }\n'
                '            ]\n'
                '        }\n'
                '    ]\n'
                "}"
            },
            
            
            {
                "role": "developer",
                "content": "Output only the JSON object .Output each layer with its elements and their relationships. Extract elements strictly from the following list:\n" + str(key_elements)+" and relationships between key elements in each layer. Extract only elements mentioned in the description along with their corresponding relationships. Ensure relationships are limited to the following:\n" + str(relationships)
                
            }

        ]
    )
    txt = completion.choices[0].message.content
    return txt


def generate_json_obj(response_content):

    # Remove markdown-style JSON code block markers
    cleaned_json = re.sub(r"```json\n|\n```", "", response_content).strip()

    try:
        json_obj = json.loads(cleaned_json)
        json.dumps(json_obj, indent=4)  # Pretty-print the JSON
    except json.JSONDecodeError as e:
        print("JSON decoding failed:", e)
        print("Raw response:", repr(response_content))
        
    return json_obj



def extract_elements(element,layer_name):
    k=element["type"].split()
    plantuml_cod=''
    element_type=''
    if(k[0]==layer_name and len(k)>1):
        element_type=k[1]
        # ch=layer_name+'_'+k[1]+'('
    else:
        # ch=layer_name+'_'+k[0]+'('   
        element_type=k[0]  
    for i in element["subElements"]:
        element_id=i['id']
        element_name=i['name']
        plantuml_cod += f"{layer_name}_{element_type}({element_id},{element_name})\n"
        
    return plantuml_cod


def define_layer_key_elements(struct,layer_name):
    # for lay in struct.keys():
    s=''
    elements=struct[layer_name]
    for element in elements:
        s+=extract_elements(element,layer_name)+'\n'
        # print(element)
        
    # print(s)
    return s
    
    
    
def define_relations_in_layer(relations,layer_name):
    plantuml_cod=''
    for lay in relations[layer_name]:
    #    print(lay)
        relation_type=relationships[lay['type'].lower()]
        from_ = lay['from']['id']
        to =lay['to']['id']
        ch = f"Rel_{relation_type}({from_},{to},{relation_type})\n"
        plantuml_cod+=ch
    # print(plantuml_code)
       
    
    return plantuml_cod
    
        # for relation in lay:
        #     print(relation)
        #     ch=''
        #     # ch ='Rel_'+relation["type"]+'('+ relation["from"]['id']+','+relation["to"]['id']+','+relation["type"]+')'+'\n'
        #     # ch ='Rel_'+relationships[relation["type"]]+'('+ relation["from"]['id']+','+relation["to"]['id']+','+relationships[relation["type"]]+')'+'\n'
        #     plantuml_code +=ch
        
        
def plantuml_for_one_layer(struct,relations,layer_name):
   
        # define_layer_key_elements(struct,layer_name,plantuml_code)
        tx1=define_layer_key_elements(struct,layer_name)
        
        # define_relations_in_layer(relations,plantuml_code,layer_name)
        tx2=define_relations_in_layer(relations,layer_name)
        # print(tx1+'\n'+tx2)
        return f"{tx1}\n{tx2}"
    
            
            
                        

            
def json_to_plantuml_archimate(json_obj):
    layers = json_obj["layers"]
    t=''
    struct={}
    relations = {}
    # print(len(layers))
    for layer in layers:
        
        layer_name = layer["layer"]
        struct[layer_name] = layer["elements"]
        relations[layer_name] = layer["element-relationship"]
        t+=plantuml_for_one_layer(struct,relations,layer_name)
        
        
                
                    
            
    
    
       
     
    return t

def generate_plantUML(json_obj):
    plantuml_code = "@startuml\n!include <archimate/Archimate>\n"
    plantuml_code += json_to_plantuml_archimate(json_obj)
    plantuml_code += "@enduml" 
    return plantuml_code
    

# txt=plantuml_+  json_to_plantuml_archimate(json_obj)
# txt+= "@enduml" 
# print(txt)

def export_plantuml_to_image(puml_file: str, output_format: str = "svg", jar_path: str = "plantuml.jar") -> str | None:
    """
    Export a .puml file to an image using PlantUML, and return the output image path.
    
    :param puml_file: The .puml file to process
    :param output_format: Output format: svg, png, eps, pdf, etc.
    :param jar_path: Path to the plantuml.jar file
    :return: The output image path, or None if an error occurred
    """
    try:
        subprocess.run([
            "java", "-jar", jar_path,
            f"-t{output_format}",
            puml_file
        ], check=True)

        # Construct the output file name
        base_name = os.path.splitext(puml_file)[0]
        output_path = f"{base_name}.{output_format}"
        print(f"✅ Diagram exported: {output_path}")
        return output_path

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to export diagram. Error: {e}")
    except FileNotFoundError:
        print("❌ Java not found or plantuml.jar missing.")
    
    return None


@app.route('/text', methods=['POST','GET'])
def generate_image():
    if request.method == 'POST':
        data = request.get_json()
        text = data['data']['desc']
        elements = data['data']['elements']

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Convert text to JSON object as text
        json_object_text = generate_json_text(text)
        
        # Convert JSON text to JSON object 
        json_object = generate_json_obj(json_object_text)
        # print(json_object)
        # Create PlantUML code from JSON object
        plantuml_code = generate_plantUML(json_object)
        print(plantuml_code)
        with open("code.puml", "w", encoding="utf-8") as f:
            f.write(plantuml_code)
        # Generate image from PlantUML code
        image_path=export_plantuml_to_image(puml_file="code.puml", output_format="svg")
        print(image_path)
        if not image_path:
            return jsonify({'error': 'Image generation failed'}), 500

        return jsonify({'image_path': image_path}), 200
    else : 
        image_path = os.path.join(os.getcwd(), 'code.svg')
        if os.path.exists(image_path):
            return send_file(image_path, mimetype='image/svg+xml')
        else:
            return jsonify({'error': 'Image not found'}), 404




if __name__ == "__main__":
    app.run(debug=True,port=8080)
    
    
# Set-ExecutionPolicy RemoteSigned -Scope Process
