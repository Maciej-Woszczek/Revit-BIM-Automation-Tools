Electrical Design Automation Tools for Revit ⚡

A collection of python scripts created to automate repetitive tasks for Electrical Engineers. Written in Python using the pyRevit API.
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

🛠️ Technology Stack

    Language: Python 3 (IronPython via pyRevit)

    Library: Autodesk Revit API 2024

    Tool: pyRevit

📷 Demo

(To be added at a later date)

👤 Author

Maciej Woszczek - Electrical Engineer & BIM Developer
