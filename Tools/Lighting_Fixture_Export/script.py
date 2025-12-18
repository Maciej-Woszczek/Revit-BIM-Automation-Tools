# -*- coding: utf-8 -*-
"""
Export Lighting Schedule (Compact Version)
------------------------------------------
Exports fixtures by room to CSV with Subtotals & Grand Total.
"""
from Autodesk.Revit.DB import *
from pyrevit import revit, DB
import os

# ==============================================================================
#  USER CONFIGURATION
# ==============================================================================
# Parameters to export (must match Revit parameter names exactly)
EXPORT_PARAMS = ["Mark", "Type Mark", "Manufacturer", "Comments"] 

# Keyword to identify the Linked Architecture model (e.g., "Arch", "Link", "Housing")
ARCH_LINK_KEYWORD = "Arch"

# Output Filename
OUTPUT_NAME = "Lighting_Schedule_Export.csv"
# ==============================================================================
#  END OF CONFIGURATION - DO NOT EDIT BELOW
# ==============================================================================

doc = revit.doc
HEADERS = ["Room Number", "Room Name", "Family", "Type"] + EXPORT_PARAMS

def get_param(elem, name):
    """Compact parameter reader (Checks Instance -> Type)."""
    p = elem.LookupParameter(name)
    if not p: # Fallback to Type Parameter
        t_id = elem.GetTypeId()
        if t_id != ElementId.InvalidElementId:
            p = doc.GetElement(t_id).LookupParameter(name)
    if not p: return ""
    # Return formatted value (User readable) or raw string
    return p.AsValueString() or p.AsString() or ""

def get_room_from_link(element, link_inst):
    """Finds room in linked model at element location."""
    if not link_inst: return "No Room", "No Room"
    try:
        # Transform point to Link Coordinates
        pt = link_inst.GetTotalTransform().Inverse.OfPoint(element.Location.Point)
        room = link_inst.GetLinkDocument().GetRoomAtPoint(pt)
        if room:
            return room.Number, room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
    except: pass
    return "No Room", "No Room"

# --- 1. FIND ARCH LINK ---
arch_link = None
for link in FilteredElementCollector(doc).OfClass(RevitLinkInstance):
    try:
        # Get Link Name
        t = doc.GetElement(link.GetTypeId())
        p_name = t.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM)
        name = p_name.AsString() if p_name else t.Name
        if ARCH_LINK_KEYWORD.lower() in name.lower():
            arch_link = link
            break
    except: pass

# --- 2. COLLECT DATA ---
fixtures = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_LightingFixtures).WhereElementIsNotElementType().ToElements()
print("Processing {} fixtures...".format(len(fixtures)))

data = []
for f in fixtures:
    r_num, r_name = get_room_from_link(f, arch_link)
    row = {"Room Number": r_num, "Room Name": r_name, "Family": f.Symbol.FamilyName, "Type": f.Name}
    for p in EXPORT_PARAMS:
        row[p] = get_param(f, p)
    data.append(row)

# Sort: Room Number -> Type
data.sort(key=lambda x: (x["Room Number"], x["Type"]))

# --- 3. ADD SUBTOTALS ---
final_rows = []
prev_room = None
room_count = 0

for row in data:
    if prev_room and prev_room != row["Room Number"]:
        final_rows.append({"Room Number": "", "Room Name": "--- SUBTOTAL: {} ---".format(room_count)})
        final_rows.append({k:"" for k in HEADERS}) # Empty spacer row
        room_count = 0
    final_rows.append(row)
    prev_room = row["Room Number"]
    room_count += 1

# Final Subtotal & Grand Total
final_rows.append({"Room Number": "", "Room Name": "--- SUBTOTAL: {} ---".format(room_count)})
final_rows.append({k:"" for k in HEADERS})
final_rows.append({"Room Number": "GRAND TOTAL", "Room Name": "{} fixtures".format(len(data))})

# --- 4. EXPORT TO CSV ---
path = os.path.join(os.path.expanduser("~/Documents"), OUTPUT_NAME)
try:
    with open(path, 'wb') as f:
        f.write(b'\xEF\xBB\xBF') # UTF-8 BOM for Excel
        # Write Header
        f.write((",".join(['"{}"'.format(h) for h in HEADERS]) + "\r\n").encode('utf-8'))
        # Write Rows
        for r in final_rows:
            line = ",".join(['"{}"'.format(str(r.get(h,"")).replace('"', '""')) for h in HEADERS])
            f.write((line + "\r\n").encode('utf-8'))     
    print("SUCCESS! Exported {} fixtures to:\n{}".format(len(data), path))
    os.startfile(path)
except Exception as e:
    print("Error saving file (Close Excel if open!): {}".format(e))
