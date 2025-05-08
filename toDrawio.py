import json
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def safe_id(element_id):
    """Prefix user IDs to avoid conflicts with Draw.io's reserved IDs (0 and 1)."""
    return f"elem_{element_id}"





def get_style_for_element(element_type):
    """Map ArchiMate element types to proper Draw.io ArchiMate styles."""

    styles = {
        # Motivation Layer (purple)
        # "Stakeholder": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=stakeholder;archiType=rounded;",
        # "Driver": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=driver;archiType=oct;",
        # "Assessment": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=assessment;archiType=oct;",
        # "Goal": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=goal;archiType=oct;",
        # "Outcome": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=outcome;archiType=oct;",
        # "Principle": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=principle;archiType=oct;",
        # "Requirement": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=requirement;archiType=square;",
        # "Constraint": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=constraint;archiType=square;",
        # "Meaning": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=meaning;archiType=rounded;",
       
        # "Value": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.motivation;appType=value;archiType=square;",
        # Motivation Layer (purple with working icons)
        "Stakeholder": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=role;archiType=oct;",
        "Driver": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=driver;archiType=oct;",
        "Assessment": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=assess;archiType=oct;",
        "Goal": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=goal;archiType=oct;",
        "Outcome": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=outcome;archiType=oct;",
        "Principle": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=principle;archiType=oct;",
        "Requirement": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=requirement;archiType=oct;",
        "Constraint": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=constraint;archiType=oct;",
        "Meaning": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=meaning;archiType=oct;",
        "Value": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#CCCCFF;shape=mxgraph.archimate3.application;appType=amValue;archiType=oct;",

        # Business Layer (yellow)
        "Business Actor": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=actor;archiType=square;",
        "Business Role": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=role;archiType=square;",
        "Business Collaboration": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=collab;archiType=square;",
        "Business Interface": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=interface;archiType=square;",
        "Business Process": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=proc;archiType=rounded;",
        "Business Function": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=func;archiType=rounded;",
        "Business Interaction": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=interact;archiType=rounded;",
        "Business Event": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=event;archiType=circle;",
        "Business Service": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=serv;archiType=rounded;",
        "Business Object": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=passive;archiType=square;",
        "Contract": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=contract;archiType=square;",
        "Representation": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=repres;archiType=square;",
        "Product": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFF99;shape=mxgraph.archimate3.application;appType=product;archiType=square;",
        # Application Layer (cyan)
        "Application Component": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#99ffff;shape=mxgraph.archimate3.application;appType=comp;archiType=square;",
        "Application Collaboration": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#99ffff;shape=mxgraph.archimate3.application;appType=collab;archiType=square;",
        "Application Interface": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#99ffff;shape=mxgraph.archimate3.application;appType=interface;archiType=square;",
        "Application Function": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#99ffff;shape=mxgraph.archimate3.application;appType=func;archiType=rounded;",
        "Application Interaction": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#99ffff;shape=mxgraph.archimate3.application;appType=interact;archiType=rounded;",
        "Application Process": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#99ffff;shape=mxgraph.archimate3.application;appType=proc;archiType=rounded;",
        "Application Event": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#99ffff;shape=mxgraph.archimate3.application;appType=event;archiType=circle;",
        "Application Service": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#99ffff;shape=mxgraph.archimate3.application;appType=serv;archiType=rounded;",
        "Data Object": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#99ffff;shape=mxgraph.archimate3.application;appType=passive;archiType=square;",
        # Technology Layer (green)
        "Node": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=node;archiType=square;",
        "Device": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=device;archiType=square;",
        "System Software": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=sysSw;archiType=square;",
        "Technology Collaboration": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=collab;archiType=square;",
        "Technology Interface": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=interface;archiType=square;",
        "Path": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=path;archiType=rounded;",
        "Communication Network": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=netw;archiType=square;",
        "Technology Function": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=func;archiType=rounded;",
        "Technology Process": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=proc;archiType=rounded;",
        "Technology Interaction": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=interact;archiType=rounded;",
        "Technology Event": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=event;archiType=circle;",
        "Technology Service": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=serv;archiType=rounded;",
        "Artifact": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#AFFFAF;shape=mxgraph.archimate3.application;appType=artifact;archiType=square;",
        # strategy layer
        "Resource": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#F5DEAA;shape=mxgraph.archimate3.application;appType=resource;archiType=square;",
        "Capability": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#F5DEAA;shape=mxgraph.archimate3.application;appType=capability;archiType=square;",
        "Course of Action": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#F5DEAA;shape=mxgraph.archimate3.application;appType=course;archiType=rounded;",
        "Value": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#F5DEAA;shape=mxgraph.archimate3.application;appType=value;archiType=square;",
        # Default style
        "default": "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=#FFFFFF;shape=mxgraph.archimate3.rectangle;",
    }
    return styles.get(element_type, styles["default"])


def get_style_for_relationship(relationship_type):
    """Map ArchiMate relationship types to proper Draw.io ArchiMate arrow styles."""
    styles = {
        "Influence": "html=1;shape=mxgraph.archimate3.relationship;archiType=influence;",
        "Assignment": "html=1;shape=mxgraph.archimate3.relationship;archiType=assignment;",
        "Triggering": "html=1;shape=mxgraph.archimate3.relationship;archiType=triggering;",
        "Serving": "html=1;shape=mxgraph.archimate3.relationship;archiType=serving;",
        "Access": "html=1;shape=mxgraph.archimate3.relationship;archiType=access;",
        "default": "html=1;shape=mxgraph.archimate3.relationship;archiType=association;",
    }
    return styles.get(relationship_type, styles["default"])




def create_shape(parent, element_id, value, x, y, width=120, height=60, style=""):
    """Create a Draw.io shape element with proper geometry and parent."""
    shape = ET.SubElement(
        parent,
        "mxCell",
        {
            "id": element_id,
            "value": escape(value),
            "style": style,
            "vertex": "1",
            "parent": "1",  # Critical: Makes the shape visible
        },
    )
    ET.SubElement(
        shape,
        "mxGeometry",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "as": "geometry",
        },
    )
    return shape


def create_connection(parent, connection_id, source, target, style=""):
    """Create a Draw.io connection between elements."""
    connection = ET.SubElement(
        parent,
        "mxCell",
        {
            "id": connection_id,
            "style": style,
            "edge": "1",
            "source": source,
            "target": target,
            "parent": "1",  # Critical: Makes the connection visible
        },
    )
    ET.SubElement(connection, "mxGeometry", {"relative": "1", "as": "geometry"})
    return connection


# def calculate_layout(layers,dis="dot"):
#     """Calculate optimal positions for elements using pygraphviz for better layout"""
#     layout_config = {
#         "layer_spacing": 500,  # Increased from 400
#         "node_spacing": 1000,   # Increased from 200
#         "margin": 200,
#         "node_width": 150,
#         "node_height": 75,
#     }
#     try:
#         import pygraphviz
#         HAS_PYGRAPHVIZ = True
#     except (ImportError, AttributeError):
#         HAS_PYGRAPHVIZ = False
#     all_positions = {}
#     current_y = layout_config["margin"]

#     for layer_idx, layer in enumerate(layers):
#         G = nx.DiGraph()

#         # Add nodes
#         for element in layer["elements"]:
#             G.add_node(element["id"])

#         # Add edges
#         for rel in layer.get("element-relationship", []):
#             G.add_edge(rel["from"], rel["to"])

#         # Convert to pygraphviz for better layout
#         try:
#             A = nx.nx_agraph.to_agraph(G)
#             A.graph_attr.update(
#                 rankdir="TB", splines="true", nodesep="0.5", ranksep="1.0"
#             )
#             A.node_attr.update(shape="rectangle", fixedsize="false")

#             # Use dot layout (hierarchical)
#             A.layout(prog=dis)

#             # Extract positions
#             for node in G.nodes():
#                 pos = A.get_node(node).attr["pos"]
#                 if pos:
#                     x, y = map(float, pos.split(","))
#                     # Adjust coordinates to our system
#                     adjusted_x = x + layout_config["margin"]
#                     adjusted_y = current_y + y
#                     all_positions[(layer_idx, node)] = (adjusted_x, adjusted_y)

#         except Exception as e:
#             print(
#                 f"Warning: pygraphviz layout failed, falling back to spring layout. Error: {e}"
#             )
#             # Fallback to spring layout if pygraphviz fails
#             pos = nx.spring_layout(
#                 G, k=layout_config["node_spacing"] / 50, iterations=100
#             )

#             # Normalize and scale coordinates
#             if pos:
#                 min_x = min(v[0] for v in pos.values())
#                 max_x = max(v[0] for v in pos.values())
#                 min_y = min(v[1] for v in pos.values())
#                 max_y = max(v[1] for v in pos.values())

#                 x_range = max_x - min_x if (max_x - min_x) > 0 else 1
#                 y_range = max_y - min_y if (max_y - min_y) > 0 else 1

#                 for node in pos:
#                     x = ((pos[node][0] - min_x) / x_range) * layout_config[
#                         "node_spacing"
#                     ] * (len(pos) - 1) + layout_config["margin"]
#                     y = ((pos[node][1] - min_y) / y_range) * layout_config[
#                         "node_spacing"
#                     ] + current_y
#                     all_positions[(layer_idx, node)] = (x, y)

#         current_y += layout_config["node_spacing"] + layout_config["layer_spacing"]

#     return all_positions

# The prog='dot' argument tells it which Graphviz layout engine to use.

# Here are the main ones:

# Engine	Algorithm Type	Best For
# dot	Hierarchical layout	Directed graphs, trees, DAGs
# neato	Spring (force-directed)	Undirected graphs
# fdp	Force-directed	Undirected graphs (larger)
# sfdp	Scalable force-directed	Very large undirected graphs
# twopi	Radial layout	Graphs with a central node
# circo	Circular layout	Cyclic or circular structures
import networkx as nx

def calculate_layout(layers_data, engine="dot"):
    """
    Compute (x, y) positions for ArchiMate elements for draw.io visualization,
    using pygraphviz for layout.

    Args:
        layers_data: List of layer dicts with 'elements' and 'element-relationship'
        engine: Layout engine (e.g., 'dot', 'neato', etc.)

    Returns:
        Dict with keys (layer_idx, element_id) -> (x, y)
    """
    import pygraphviz
    from networkx.drawing.nx_agraph import to_agraph

    layout_config = {
        "horizontal_spacing": 120,
        "vertical_spacing": 120,
        "layer_spacing": 300,
        "margin": 50,
    }

    positions = {}
    current_y = layout_config["margin"]

    for layer_idx, layer in enumerate(layers_data):
        G = nx.DiGraph()

        # Add elements as nodes
        for element in layer.get("elements", []):
            G.add_node(element["id"])

        # Add relationships as edges
        for rel in layer.get("element-relationship", []):
            G.add_edge(rel["from"], rel["to"])

        try:
            A = to_agraph(G)

            A.graph_attr.update(rankdir="TB", splines="true", nodesep="1.0", ranksep="1.0")
            A.node_attr.update(shape="box", fixedsize="false")

            A.layout(prog=engine)

            for node in G.nodes():
                pos = A.get_node(node).attr["pos"]
                if pos:
                    x, y = map(float, pos.split(","))

                    # Convert to draw.io-style coordinates
                    adjusted_x = x + layout_config["margin"]
                    adjusted_y = -y + current_y  # Flip Y

                    positions[(layer_idx, node)] = (adjusted_x, adjusted_y)

        except Exception as e:
            print(f"[Warning] Layout failed for layer {layer_idx}: {e}")

        current_y += layout_config["vertical_spacing"] + layout_config["layer_spacing"]

    return positions

def json_to_drawio(json_data, output_file,display="dot"):
    """Convert ArchiMate JSON to a fully valid Draw.io XML file with proper positioning."""
    data = json.loads(json_data)

    # Calculate optimized positions
    all_positions = calculate_layout(data["layers"],display)

    # Initialize Draw.io XML structure
    mxfile = ET.Element("mxfile", {"version": "1.0", "encoding": "UTF-8"})
    diagram = ET.SubElement(
        mxfile, "diagram", {"name": "ArchiMate Model", "id": "archimate_diagram"}
    )
    mxGraphModel = ET.SubElement(
        diagram,
        "mxGraphModel",
        {"dx": "1050", "dy": "522", "grid": "1", "gridSize": "10"},
    )
    root = ET.SubElement(mxGraphModel, "root")

    # Mandatory root cells (Draw.io requirement)
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})  # Default layer

    # Track element IDs (no need for manual x/y tracking)
    element_map = {}

    # Process each layer
    for layer_idx, layer in enumerate(data["layers"]):
        # Add layer label (position at the top-center of the layer)
        layer_label_id = f"label_{layer['layer'].replace(' ', '_')}"
        layer_nodes = [elem["id"] for elem in layer["elements"]]
        
        # Calculate layer label position (center of the layer)
        if layer_nodes:
            x_positions = [all_positions[(layer_idx, node)][0] for node in layer_nodes]
            layer_center_x = (min(x_positions) + max(x_positions)) / 2
            layer_top_y = min([all_positions[(layer_idx, node)][1] for node in layer_nodes]) - 80
        else:
            layer_center_x, layer_top_y = 100, 100 + (400 * layer_idx)

        create_shape(
            parent=root,
            element_id=layer_label_id,
            value=layer["layer"],
            x=layer_center_x - 100,  # Center the label
            y=layer_top_y,
            width=200,
            height=30,
            style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];",
        )

        # Add elements using calculated positions
        for element in layer["elements"]:
            elem_id = safe_id(element["id"])
            style = get_style_for_element(element["type"])
            
            # Get pre-calculated position
            pos_x, pos_y = all_positions.get((layer_idx, element["id"]), (100, 100 + (400 * layer_idx)))
            
            create_shape(
                root, 
                elem_id, 
                element["name"], 
                x=pos_x, 
                y=pos_y, 
                style=style
            )
            element_map[element["id"]] = elem_id

        # Add relationships
        for rel in layer.get("element-relationship", []):
            source_id = element_map.get(rel["from"])
            target_id = element_map.get(rel["to"])
            
            if source_id and target_id:  # Only create if both elements exist
                style = get_style_for_relationship(rel["type"])
                create_connection(
                    root, 
                    f"conn_{source_id}_{target_id}", 
                    source_id, 
                    target_id, 
                    style=style
                )

    # Save to file
    tree = ET.ElementTree(mxfile)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)
    # print(f"Draw.io file successfully generated: '{output_file}'")
    return output_file
