Electrical Design Automation Tools for Revit ⚡

A collection of Revit C# Addins and python scripts created to automate repetitive tasks for Electrical Engineers. Scripts are using the pyRevit API.
🚀 Features
1. Auto-Tag Elements

Automatically places tags on selected electrical categories (e.g., Fixtures, Lighting) in the active view.

    Problem solved: Manual tagging of hundreds of sockets takes multiple hours for big projects.
    Solution: This script does it in <5 seconds.

    Key Features:

        Configurable target category (Socket, Light, Fire Alarm).
        Checks element location type to avoid errors.
        Transaction safety handling.

2. Auto-Create electrical fixtures for devices (BETA) 

Scans linked Revit models (HVAC, Plumbing, Medical) and automatically places electrical connection points based on the equipment's power data.

    Problem solved: Engineers spend hours manually checking mechanical drawings to place power outlets for pumps, VAVs, and fans.
    Solution: This script scans the link, reads the power parameter, and places the correct 1-Phase or 3-Phase connection family automatically.

    Key Features:

        Smart Filtering: Only connects devices that actually require power (filters out passive silencers, sinks, etc.).
        Type Mapping: Automatically selects between "Standard" and "Fire Safety" (FLS) connection types based on keywords.
        Duplicate Protection: Prevents placing a new connection if one already exists at that location.

    ⚠️ Note: This script requires configuration to match your company's specific parameter names (e.g., "Apparent Power" vs "Load").
        It has been tested on sample data but requires validation on a real-world project to ensure edge cases are handled.

3. Export Lighting Fixtures by Linked Room

Generates a comprehensive lighting fixture report grouped by Room, capable of resolving rooms inside Linked Models.

    Problem solved: Standard Revit schedules often struggle to group elements by "Linked Rooms" effectively for external reports, and exporting with custom subtotals usually requires manual Excel work.  
    Solution: This script geometrically maps every light to its architectural room (even in links), calculates counts, and exports a formatted report instantly.

    Key Features:
        Linked Room Resolution: Uses geometric transformation to accurately identify which room a fixture belongs to inside a linked Architecture file.
        Automated Reporting: Automatically inserts "Subtotal" rows for each room and a "Grand Total" at the end of the file.
        Excel-Ready: Exports to a specially formatted CSV (UTF-8 BOM) that opens perfectly in Excel with no manual formatting required.
        Zero Dependencies: Runs on pure Python/Revit API without requiring external libraries.

🛠️ Technology Stack

    Language: Python 3 (IronPython via pyRevit)
    Library: Autodesk Revit API 2024
    Tool: pyRevit

📷 Demo

(To be added at a later date)

👤 Author

Maciej Woszczek - Electrical Engineer & BIM Developer
