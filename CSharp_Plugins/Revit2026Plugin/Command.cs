using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Autodesk.Revit.Attributes;

// 1. File-Scoped Namespace
namespace MyRevit2026Plugin;

[Transaction(TransactionMode.Manual)]
public class CalculateTotalLength : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        // Setup API Objects
        UIDocument uidoc = commandData.Application.ActiveUIDocument;
        Document doc = uidoc.Document;
        // 2. Get Selected Element IDs
        ICollection<ElementId> selectedIds = uidoc.Selection.GetElementIds();

        if (selectedIds.Count == 0)
        {
            TaskDialog.Show("Total Length", "Please select Conduits or Cable Trays first.");
            return Result.Cancelled;
        }
        double totalLengthFeet = 0.0;
        int count = 0;

        foreach (ElementId id in selectedIds)
        {
            Element? elem = doc.GetElement(id);
            if (elem == null) continue;

            // 3. Robust Parameter Retrieval
            Parameter? lenParam = elem.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH);

            // Checks if parameter exists and has a value
            if (lenParam is { HasValue: true })
            {
                totalLengthFeet += lenParam.AsDouble();
                count++;
            }
        }
        // 5. Unit Conversion (Feet -> Meters)
        double totalLengthMeters = totalLengthFeet * 0.3048;

        TaskDialog.Show("Total Length Calculation",
            $"Selected Items: {count}\n" +
            $"Total Length: {totalLengthMeters:F2} m\n" +
            $"(Raw Internal: {totalLengthFeet:F2} ft)");
        return Result.Succeeded;
    }
}
