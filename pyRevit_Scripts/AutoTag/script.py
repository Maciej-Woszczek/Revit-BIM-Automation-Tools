# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from pyrevit import revit, DB

# ==========================================
# SCRIPT CONFIGURATION (Edit this section)
# ==========================================

# 1. Elements to tag (Category)
# Examples: OST_ElectricalFixtures, OST_LightingFixtures, OST_CommunicationDevices
TARGET_CATEGORY = BuiltInCategory.OST_ElectricalFixtures

# 2. Tag to use (Tag Category)
# Examples: OST_ElectricalFixtureTags, OST_LightingFixtureTags
TAG_CATEGORY = BuiltInCategory.OST_ElectricalFixtureTags

# 3. Specific Tag Name (Optional)
# Set to None to use the first available tag found in the project.
# Set to a specific string (e.g. "E_Tag_Socket_Type1") if you need a specific family type.
SPECIFIC_TAG_NAME = None 

# ==========================================
# END OF CONFIGURATION - DO NOT EDIT BELOW
# ==========================================

doc = revit.doc
active_view = doc.ActiveView

# 1. Collect elements in the active view
collector = FilteredElementCollector(doc, active_view.Id)\
            .OfCategory(TARGET_CATEGORY)\
            .WhereElementIsNotElementType()\
            .ToElements()

# 2. Find the tag symbol
tag_collector = FilteredElementCollector(doc)\
                .OfClass(FamilySymbol)\
                .OfCategory(TAG_CATEGORY)

# Logic to select the specific tag or the first available one
tag_symbol = None

if SPECIFIC_TAG_NAME:
    # Look for the specific name provided in config
    for tag in tag_collector:
        if tag.FamilyName == SPECIFIC_TAG_NAME or tag.Name == SPECIFIC_TAG_NAME:
            tag_symbol = tag
            break
else:
    # Take the first one found
    tag_symbol = tag_collector.FirstElement()

# Safety check
if not tag_symbol:
    print("ERROR: No tag family found in category: {}".format(TAG_CATEGORY))
else:
    # 3. Create Tags
    count = 0
    
    # Transaction name defined internally
    transaction_name = "Auto-Tag Elements"
    
    with revit.Transaction(transaction_name):
        for element in collector:
            # Check if element has a point location
            if isinstance(element.Location, LocationPoint):
                location_pt = element.Location.Point
                
                # Create the tag
                IndependentTag.Create(
                    doc, 
                    tag_symbol.Id, 
                    active_view.Id, 
                    Reference(element), 
                    False, # Leader (False = no leader)
                    TagOrientation.Horizontal, 
                    location_pt
                )
                count += 1

    print("Done! Used tag: '{}'".format(tag_symbol.FamilyName))
    print("Tagged elements count: {}".format(count))
