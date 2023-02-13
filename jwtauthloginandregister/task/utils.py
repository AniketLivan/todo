def ConvertQuerysetToJson(qs):
    if qs == None:
        return "Please provide valid Django QuerySet"
    else:
        json_data = []
        for i in qs:
            i = i.__dict__
            i.pop("_state")
            json_data.append(i)
    return json_data
