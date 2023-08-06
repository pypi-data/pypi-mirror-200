"""BEMServer API client resources

/sites/ endpoints
/buildings/ endpoints
/storeys/ endpoints
/spaces/ endpoints
/zones/ endpoints
/structural_element_properties/ endpoints
/site_properties/ endpoints
/building_properties/ endpoints
/storey_properties/ endpoints
/space_properties/ endpoints
/zone_properties/ endpoints
/site_property_data/ endpoints
/building_property_data/ endpoints
/storey_property_data/ endpoints
/space_property_data/ endpoints
/zone_property_data/ endpoints
"""
from .base import BaseResources


class SiteResources(BaseResources):
    endpoint_base_uri = "/sites/"
    client_entrypoint = "sites"


class BuildingResources(BaseResources):
    endpoint_base_uri = "/buildings/"
    client_entrypoint = "buildings"


class StoreyResources(BaseResources):
    endpoint_base_uri = "/storeys/"
    client_entrypoint = "storeys"


class SpaceResources(BaseResources):
    endpoint_base_uri = "/spaces/"
    client_entrypoint = "spaces"


class ZoneResources(BaseResources):
    endpoint_base_uri = "/zones/"
    client_entrypoint = "zones"


class StructuralElementPropertyResources(BaseResources):
    endpoint_base_uri = "/structural_element_properties/"
    client_entrypoint = "structural_element_properties"


class SitePropertyResources(BaseResources):
    endpoint_base_uri = "/site_properties/"
    disabled_endpoints = ["update"]
    client_entrypoint = "site_properties"


class BuildingPropertyResources(BaseResources):
    endpoint_base_uri = "/building_properties/"
    disabled_endpoints = ["update"]
    client_entrypoint = "building_properties"


class StoreyPropertyResources(BaseResources):
    endpoint_base_uri = "/storey_properties/"
    disabled_endpoints = ["update"]
    client_entrypoint = "storey_properties"


class SpacePropertyResources(BaseResources):
    endpoint_base_uri = "/space_properties/"
    disabled_endpoints = ["update"]
    client_entrypoint = "space_properties"


class ZonePropertyResources(BaseResources):
    endpoint_base_uri = "/zone_properties/"
    disabled_endpoints = ["update"]
    client_entrypoint = "zone_properties"


class SitePropertyDataResources(BaseResources):
    endpoint_base_uri = "/site_property_data/"
    client_entrypoint = "site_property_data"


class BuildingPropertyDataResources(BaseResources):
    endpoint_base_uri = "/building_property_data/"
    client_entrypoint = "building_property_data"


class StoreyPropertyDataResources(BaseResources):
    endpoint_base_uri = "/storey_property_data/"
    client_entrypoint = "storey_property_data"


class SpacePropertyDataResources(BaseResources):
    endpoint_base_uri = "/space_property_data/"
    client_entrypoint = "space_property_data"


class ZonePropertyDataResources(BaseResources):
    endpoint_base_uri = "/zone_property_data/"
    client_entrypoint = "zone_property_data"
