def loadParentSet(loaded_dict,company='VTS'):
    groupKPISet = set()
    for oneKPI in loaded_dict['01/2020']['month'][company]:
        comp = loaded_dict['01/2020']['month'][company][oneKPI]['KPI MẸ']
        groupKPISet.add(comp)
    return groupKPISet

def listingGroupKPI(loaded_dict,company='VTPOST',kpi_mom='Tỷ lệ xử lý phản ánh của KH'):
    listOneKPI = []
    for oneKPI in loaded_dict['01/2020']['month'][company]:
        comp = loaded_dict['01/2020']['month'][company][oneKPI]['KPI MẸ']
        if comp == kpi_mom: 
            listOneKPI.append(oneKPI)
    return listOneKPI