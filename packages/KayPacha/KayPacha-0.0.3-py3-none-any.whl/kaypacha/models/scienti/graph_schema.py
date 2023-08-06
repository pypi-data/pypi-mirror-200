# Scienti data model 2022
# SCHEMA version for modification on the relations, it is vertioned as well
from .graph_schema_product import graph_product
from .graph_schema_network import graph_network
from .graph_schema_project import graph_project
from .graph_schema_event import graph_event
from .graph_schema_patent import graph_patent
from .graph_schema_endorsement import graph_endorsement

graph_schema = {"SCIENTI_MODEL": 2022}
graph_schema["MODELS"] = {}


graph_schema["MODELS"]["network"] = graph_network
graph_schema["MODELS"]["product"] = graph_product
graph_schema["MODELS"]["project"] = graph_project
graph_schema["MODELS"]["event"] = graph_event
graph_schema["MODELS"]["patent"] = graph_patent
graph_schema["MODELS"]["endorsement"] = graph_endorsement
