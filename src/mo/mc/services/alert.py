#####################################################
# Generated by generators/generator.py              #
# This file is generated. Do NOT edit it by hand.   #
#####################################################

"""The alert service defines the structures and patterns for the publishing and monitoring of alerts. The alert service uses COM event service to monitor and publish alert events.
The generation of alerts can be controlled using the enableGeneration operation, which supports the use of groups. Groups must reference either other groups or alerts only.
Alert definitions are maintained using the operations defined in this service but storage of definitions is delegated to the COM archive."""

from enum import IntEnum
from mo import mal
from mo import com
from mo.mc import *

number = 3

# CapabilitySet 1
class EnableGeneration(mal.RequestProviderHandler):
    pass


# CapabilitySet 2
class ListDefinition(mal.RequestProviderHandler):
    pass


# CapabilitySet 3
class AddAlert(mal.RequestProviderHandler):
    pass

class UpdateDefinition(mal.RequestProviderHandler):
    pass

class RemoveAlert(mal.SubmitProviderHandler):
    pass

# Composite
## AlertDefinitionDetails
## AlertEventDetails
## AlertCreationRequest


