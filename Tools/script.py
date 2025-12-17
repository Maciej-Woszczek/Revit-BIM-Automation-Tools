# -*- coding: utf-8 -*-
"""
Auto-Connect Linked Devices Script (Production Ready)
-----------------------------------------------------
Scans linked models and places electrical connection points.
INCLUDES: Duplicate checking, Progress Bar, and FULL Keyword Filtering.
"""
from Autodesk.Revit.DB import *
from pyrevit import revit, DB, forms, script

# ==============================================================================
#   USER CONFIGURATION
# ==============================================================================

# --- 1. FILTERING & FAMILY ---
LINK_NAME_FILTER    = "HVAC"
SOURCE_CATEGORY     = BuiltInCategory.OST_MechanicalEquipment
CONNECTION_FAMILY   = "E_Connection_Point"

# Map: Logic -> Family Type
TYPE_NAMES_MAP = {
    "3PH_STD": "Connection 3-Phase",
    "1PH_STD": "Connection 1-Phase",
    "3PH_FLS": "Connection 3-Phase FLS",
    "1PH_FLS": "Connection 1-Phase FLS"
}

# --- 2. POWER DETECTION ---
# Parameters to check for power value
PARAM_POWER_CHECK   = "Apparent Power"
MIN_POWER_VAL       = 0.0

# --- 3. KEYWORD LOGIC (RESTORED) ---
# Comprehensive list to catch all variations of terms
KEYWORDS_FLS    = [
    "FLS", "FIRE", "SAFETY", "CRITICAL", "DAMP", "VALVE", 
    "SMOKE", "ALARM", "DETECTOR", "SPRINKLER", "EMERGENCY"
]

KEYWORDS_1PHASE = [
    "230", "1F", "1PH", "1-PH", "SINGLE", 
    "120V", "230V", "1-PHASE", "SINGLE-PHASE"
]

# Parameters to scan for the keywords above
SCAN_PARAMS     = [
    "Fire Rating", 
    "Comments", 
    "Description", 
    "Mark", 
    "Type Mark", 
    "Type Comments",
    "Model",
    "Family Name" 
]

# --- 4. DATA TRANSFER ---
PARAM_COPY_MAP  = {
    "Description":      "Mark", 
    "Comments":         "Type Mark", 
    "E_Device_Power":   "Apparent Power"
}

# ==============================================================================
#   END OF CONFIGURATION
# ==============================================================================

doc = revit.doc

# --- HELPER FUNCTIONS ---
def get_param_val(element, param_name):
    """Safely retrieves a parameter string."""
    if not element: return ""
    p = element.LookupParameter(param_name)
    if not p:
        elem_type = doc.GetElement(element.GetTypeId())
        p = elem_type.LookupParameter(param_name) if elem_type else None
    
    if p:
        return p.AsString() if p.StorageType == StorageType.String else p.AsValueString()
    return ""

def needs_power(element):
    """Checks for valid power requirements."""
    val = get_param_val(element, PARAM_POWER_CHECK)
    if not val: return False
    clean_val = val.upper().replace("VA", "").replace("W", "").replace(" ", "")
    if "NONE" in clean_val or "BRAK" in clean_val: return False
    try:
        return float(clean_val) > MIN_POWER_VAL
    except ValueError:
        return True # Assume text description implies power needed

def get_symbol_type(element, symbol_map):
    """Selects family symbol based on keywords."""
    # Combine all text into one uppercase string for efficient searching
    all_text = " ".join([get_param_val(element, p) or "" for p in SCAN_PARAMS]).upper()
    
    is_fls = any(k in all_text for k in KEYWORDS_FLS)
    is_1ph = any(k in all_text for k in KEYWORDS_1PHASE)
    
    # Logic Map
    key_map = {
        (False, False): "3PH_STD", 
        (False, True):  "1PH_STD",
        (True, False):  "3PH_FLS", 
        (True, True):   "1PH_FLS"
    }
    return symbol_map.get(TYPE_NAMES_MAP[key_map[(is_fls, is_1ph)]])

def is_duplicate(location_point):
    """Checks if a connection point already exists at this XYZ location."""
    delta = 0.5 # Tolerance in feet
    outline = BoundingBoxXYZ()
    outline.Min = location_point - XYZ(delta, delta, delta)
    outline.Max = location_point + XYZ(delta, delta, delta)
    
    filter_outline = BoundingBoxIsInsideFilter(outline)
    
    existing = FilteredElementCollector(doc)\
               .OfClass(FamilyInstance)\
               .WherePasses(filter_outline)\
               .ToElements()
               
    for e in existing:
        if e.Symbol.FamilyName == CONNECTION_FAMILY:
            return True
    return False

# --- MAIN EXECUTION ---
symbols = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
symbol_map = {DB.Element.Name.__get__(s): s for s in symbols if s.FamilyName == CONNECTION_FAMILY}

if not symbol_map:
    forms.alert("Family '{}' not found!".format(CONNECTION_FAMILY), exitscript=True)

# 1. Collect Valid Linked Elements
valid_elements = []
all_links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

for link in all_links:
    type_elem = doc.GetElement(link.GetTypeId())
    link_name = get_param_val(type_elem, "Type Name") or ""
    
    # Check link name filter
    if LINK_NAME_FILTER.upper() in link_name.upper():
        link_doc = link.GetLinkDocument()
        if not link_doc: continue
        
        transform = link.GetTotalTransform()
        
        # Collect items from link
        raw_elements = FilteredElementCollector(link_doc).OfCategory(SOURCE_CATEGORY)\
                       .WhereElementIsNotElementType().ToElements()
                       
        for el in raw_elements:
            if needs_power(el) and isinstance(el.Location, LocationPoint):
                valid_elements.append((el, transform))

# 2. Process with Progress Bar
if not valid_elements:
    forms.alert("No matching elements found in links.", exitscript=True)

count_placed = 0
count_exist = 0

with revit.Transaction("Auto-Connect Equipment"):
    [s.Activate() for s in symbol_map.values() if not s.IsActive]
    
    with forms.ProgressBar(title="Placing Connections... ({value}/{max_value})", cancellable=True) as pb:
        for i, (el, transform) in enumerate(valid_elements):
            if pb.cancelled: break
            pb.update_progress(i, len(valid_elements))
            
            # Calculate Point
            loc_pt = transform.OfPoint(el.Location.Point)
            
            # DUPLICATE CHECK
            if is_duplicate(loc_pt):
                count_exist += 1
                continue

            sym = get_symbol_type(el, symbol_map)
            if sym:
                try:
                    new_inst = doc.Create.NewFamilyInstance(loc_pt, sym, Structure.StructuralType.NonStructural)
                    
                    # Copy Params
                    for tgt, src in PARAM_COPY_MAP.items():
                        val = get_param_val(el, src)
                        if val and not new_inst.LookupParameter(tgt).IsReadOnly:
                            new_inst.LookupParameter(tgt).Set(val)
                    
                    count_placed += 1
                except Exception:
                    pass

# 3. Final Report
print("--------------------------------")
print("SUMMARY:")
print("Found Potential Targets: {}".format(len(valid_elements)))
print("Skipped (Already Exists): {}".format(count_exist))
print("Successfully Placed:      {}".format(count_placed))
