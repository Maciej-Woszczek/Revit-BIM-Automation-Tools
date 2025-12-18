Electrical Design Automation Tools for Revit ⚡

A collection of high-efficiency tools for Electrical Engineers, featuring rapid Python scripting (pyRevit) and robust C# plugins for Revit 2026.

🚀 Features

1. Total Length Calculator (C# Plugin)

A compiled Revit command written in C# (.NET 8) for rapid quantity checking.

    Problem Solved: Verifying the total length of specific cable tray or conduit runs requires creating temporary schedules or manual addition, which is slow and error-prone.
    Solution: A compiled plugin that instantly sums the length of any selected linear elements and displays the result in Meters, handling all unit conversions automatically.

    Key Features:
    Instant QTO: One-click calculation of total run lengths.
    Unit Safety: robust conversion from Revit internal units (Feet) to Metric (Meters).
    Future-Proof: Built on .NET 8, compatible with Revit 2026.
    Standalone: Runs natively without requiring pyRevit or Dynamo.

2. Auto-Tag Elements (pyRevit script)

Automatically places tags on selected electrical categories (e.g., Fixtures, Lighting) in the active view.

    Problem solved: Manual tagging of hundreds of sockets takes multiple hours for big projects.
    Solution: This script does it in <5 seconds.

    Key Features:

        Configurable target category (Socket, Light, Fire Alarm).
        Checks element location type to avoid errors.
        Transaction safety handling.

3. Auto-Create electrical fixtures for devices (pyRevit script) (BETA) 

Scans linked Revit models (HVAC, Plumbing, Medical) and automatically places electrical connection points based on the equipment's power data.

    Problem solved: Engineers spend hours manually checking mechanical drawings to place power outlets for pumps, VAVs, and fans.
    Solution: This script scans the link, reads the power parameter, and places the correct 1-Phase or 3-Phase connection family automatically.

    Key Features:

        Smart Filtering: Only connects devices that actually require power (filters out passive silencers, sinks, etc.).
        Type Mapping: Automatically selects between "Standard" and "Fire Safety" (FLS) connection types based on keywords.
        Duplicate Protection: Prevents placing a new connection if one already exists at that location.

    ⚠️ Note: This script requires configuration to match your company's specific parameter names (e.g., "Apparent Power" vs "Load").
        It has been tested on sample data but requires validation on a real-world project to ensure edge cases are handled.

4. Export Lighting Fixtures by Linked Room (pyRevit script)

Generates a comprehensive lighting fixture report grouped by Room, capable of resolving rooms inside Linked Models.

    Problem solved: Standard Revit schedules often struggle to group elements by "Linked Rooms" effectively for external reports, and exporting with custom subtotals usually requires manual Excel work.  
    Solution: This script geometrically maps every light to its architectural room (even in links), calculates counts, and exports a formatted report instantly.

    Key Features:
        Linked Room Resolution: Uses geometric transformation to accurately identify which room a fixture belongs to inside a linked Architecture file.
        Automated Reporting: Automatically inserts "Subtotal" rows for each room and a "Grand Total" at the end of the file.
        Excel-Ready: Exports to a specially formatted CSV (UTF-8 BOM) that opens perfectly in Excel with no manual formatting required.
        Zero Dependencies: Runs on pure Python/Revit API without requiring external libraries.

🛠️ Technology Stack

    🐍 Python / Scripting
        *   Language: Python 3 (IronPython)
        *   Tool: pyRevit
        *   Target: Revit 2024 Automation
    
    ⚙️ C# / .NET Plugin Development
        *   Language: C#
        *   Framework: .NET 8.0 (Targeting Revit 2026)
        *   IDE: Visual Studio 2022
        *   Competencies: Revit API (IExternalCommand), Plugin Compilation & Loading, UI Interaction (TaskDialog)

📷 Demo

TotalLengthCalculator:
![image](https://github.com/user-attachments/assets/9a8b0a6b-f69a-4ab2-a5ba-5d8cf27543f8)

(Demos for other tools to be added at a later date)

👤 Author

Maciej Woszczek - Electrical Engineer & BIM Developer
