# Copyright (c) 2024 Châu Bình Phương Tâm
# For details, please contact me via LinkedIn: https://www.linkedin.com/in/phuongtam1994/
# Or email me at cbptamdev@gmail.com
# 
# 詳細についてはLinkedInで私に連絡してください：https://www.linkedin.com/in/phuongtam1994/
# またはメールでcbptamdev@gmail.comに連絡してください。

import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import*
from Autodesk.Revit.UI.Selection import *


clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

    
def get_dependent_family_instances(element):
    filter = ElementClassFilter(FamilyInstance) # type: ignore
    dependent_ids = element.GetDependentElements(filter)
    return dependent_ids
    
def set_construction_phase(element, param, value):
    parameter = element.LookupParameter(param)
    if parameter and not parameter.IsReadOnly:
        TransactionManager.Instance.EnsureInTransaction(doc)
        parameter.Set(value)
        TransactionManager.Instance.TransactionTaskDone()
        return True
    return False


dependent_elements_list = []
result = []
generic_models = [
    element 
    for element in FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(FamilyInstance).ToElements() 
    if element.Category.Name == "Generic Models"
]

for generic_model in generic_models:
    if generic_model.Category.Name == "Generic Models":
        dependent_ids = get_dependent_family_instances(generic_model)
        for id in dependent_ids:
            dependent_element = doc.GetElement(id)
            success = set_construction_phase(dependent_element, IN[1], generic_model.LookupParameter(IN[1]).AsValueString())  # Replace "ParameterName" with your actual parameter name
            result.append(success)

count_successful_operations = result.count(True)

OUT = "Success"
