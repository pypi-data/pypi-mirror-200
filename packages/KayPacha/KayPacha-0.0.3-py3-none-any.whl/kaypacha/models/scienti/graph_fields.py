from .graph_fields_product import product_fields
from .graph_fields_network import network_fields
from .graph_fields_project import project_fields
from .graph_fields_event import event_fields
from .graph_fields_patent import patent_fields
from .graph_fields_endorsement import endorsement_fields
graph_fields = {}

# adding fields for every main entity
graph_fields["EN_PRODUCTO"] = product_fields
graph_fields["EN_RED"] = network_fields
graph_fields["EN_PROYECTO"] = project_fields
graph_fields["EN_EVENTO"] = event_fields
graph_fields["EN_PATENTE"] = patent_fields
graph_fields["EN_AVAL_INSTITUCION"] = endorsement_fields
