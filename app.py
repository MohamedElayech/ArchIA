"""
Flask backend for the entreprise architecture diagram generator

This backend uses the OpenAI API to generate PlantUML code for an Archimate diagram.
The generated PlantUML code is then used to generate an image using PlantUML.
The image is then returned to the frontend.
"""

import subprocess
import json
import re
import os
from openai import OpenAI
from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
# import zlib
# import base64

client = OpenAI()

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

    "serve": "Serving",
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
    """
    Generate JSON text based on the provided test string and using an OpenAI prompt.
    """
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system", 
                "content": """ You are a specialized assistant for extracting layers and their key elements from enterprise architecture descriptions."""
            },

            {
                "role": "user",
                "content": test
            },

            {
                "role": "assistant",
                "content": "Analyze the provided enterprise architecture description and identify all layers it describes (e.g., Business Layer, Application Layer, Motivation Layer, etc.). Extract only the key elements for these layers based on the description provided. Do not assume any elements are present unless explicitly mentioned in the description. The key element name shouldn't contain the name of the layer. The id of each element should containes only characters and numbers"
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
                "content": "Output only the JSON object. Output each layer with its elements and their relationships. Extract elements strictly from the following list:\n" + str(key_elements)+" and relationships between key elements in each layer. Extract only elements mentioned in the description along with their corresponding relationships. Ensure relationships are limited to the following:\n" + str(relationships)
            }

        ]
    )
    txt = completion.choices[0].message.content
    return txt


def generate_json_obj(response_content):
    """
    Generate a JSON object from the response content.
    
    :param response_content: The response content containing JSON data in text format.
    :return: The generated JSON object.
    """

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
    """
    Extract elements from an element dictionary and generate PlantUML code for this element.
    :param element: The element from dictionary
    :return: The generated PlantUML code
    """
    print(element["type"])
    k=''
    if element["type"].startswith(layer_name):
        k = element["type"][len(layer_name):].strip()
    else:
        k=element["type"]
    # print(k)
    # k=element["type"].split()
    plantuml_cod=''
    element_type= ''.join(word.capitalize() for word in k.split())

    for i in element["subElements"]:
        element_id=i['id']
        element_name='"'+i['name']+'"'
        if element_type == "Data":
            element_type="DataObject"
        plantuml_cod += f"{layer_name.split()[0]}_{element_type}({element_id},{element_name})\n"

    return plantuml_cod


def define_layer_key_elements(struct,layer_name):
    """
    Generate PlantUML code for the key elements in a layer.

    :param struct: The structure of the layer
    :param layer_name: The name of the layer
    :return: PlantUML code for the key elements
    """

    # for lay in struct.keys():
    s=''
    elements=struct[layer_name]
    for element in elements:
        s+=extract_elements(element,layer_name)+'\n'
    print(s)

    return s


def define_relations_in_layer(relations,layer_name):
    """
    Generate PlantUML code for the relationships in a layer.

    :param relations: The relationships of the layer
    :param layer_name: The name of the layer
    :return: PlantUML code for the relationships
    """
    plantuml_cod=''
    for lay in relations[layer_name]:
        # print(relations[layer_name])
        relation_type=relationships[lay['type'].lower()]
        from_ = lay['from']['id']
        to =lay['to']['id']
        ch = f"Rel_{relation_type}({from_},{to},{relation_type})\n"
        plantuml_cod+=ch
    # print(relation_type)

    return plantuml_cod

def plantuml_for_one_layer(struct,relations,layer_name):
    """
    Generate PlantUML code for a single layer.

    :param struct: The structure of the layer
    :param relations: The relationships of the layer
    :param layer_name: The name of the layer
    :return: The generated PlantUML code for the layer that contains elements and relationships
    """
    # print(f"[DEBUG] Entering plantuml_for_one_layer with layer: {layer_name}")
    # define_layer_key_elements(struct,layer_name,plantuml_code)
    tx1=define_layer_key_elements(struct,layer_name)

    # define_relations_in_layer(relations,plantuml_code,layer_name)
    tx2=define_relations_in_layer(relations,layer_name)
    # print(tx1+'\n'+tx2)
    return f"{tx1}\n{tx2}"





def json_to_plantuml_archimate(json_obj,elnts):
    """
    Generate PlantUML code from a JSON object.
    :param json_obj: The JSON object to process
    :return: The generated PlantUML code
    """
    layers = json_obj["layers"]
    t=''
    struct = {}
    relations = {}

    for layer in layers:
        layer_name = layer["layer"]
        layer_n = layer["layer"].split()[0]
        struct[layer_name] = layer["elements"]
        relations[layer_name] = layer["element-relationship"]
        if layer_n in elnts:
            t+=plantuml_for_one_layer(struct,relations,layer_name)
        print(layer_name)
    # print(relations)
    return t

def generate_plantuml_code(json_obj,elnts):
    """
    Generate PlantUML code from a JSON object.
    :param json_obj: The JSON object to process
    :return: The generated PlantUML code
    """
    plantuml_code = "@startuml\n!include <archimate/Archimate>\n"
    plantuml_code += json_to_plantuml_archimate(json_obj,elnts)
    plantuml_code += "@enduml"
    return plantuml_code




def export_plantuml_to_image(
    puml_file: str,
    output_format: str = "svg",
    jar_path: str = "plantuml.jar"
) -> str | None:
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
    """Handles POST and GET requests to generate or retrieve a PlantUML image.

    - On POST: expects JSON with 'desc' and 'elements', generates PlantUML code and image.
    - On GET: returns the previously generated image if available.
    """
    if request.method == 'POST':
        data = request.get_json()
        text = data['data']['desc']
        elnts = data['data']['elements']
        print(elnts)
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Convert text to JSON object as text
        json_object_text = generate_json_text(text)

        # Convert JSON text to JSON object
        json_object = generate_json_obj(json_object_text)
        # print(json_object)
        # Create PlantUML code from JSON object
        plantuml_code = generate_plantuml_code(json_object,elnts)
        print(plantuml_code)

        with open("code.puml", "w", encoding="utf-8") as f:
            f.write(plantuml_code)
        # Generate image from PlantUML code
        image_path=export_plantuml_to_image(puml_file="code.puml", output_format="svg")
        print(image_path)
        if not image_path:
            return jsonify({'error': 'Image generation failed'}), 500

        return jsonify({'image_path': image_path}), 200

    image_path = os.path.join(os.getcwd(), 'code.svg')
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/svg+xml')
    return jsonify({'error': 'Image not found'}), 404




if __name__ == "__main__":
    app.run(debug=True,port=8080)

# Set-ExecutionPolicy RemoteSigned -Scope Process
