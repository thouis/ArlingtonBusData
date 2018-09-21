import mbtaapi
import datetime
api_instance = mbtaapi.VehicleApi()
D = ([datetime.datetime.now().isoformat()] +
     api_instance.api_web_vehicle_controller_index(api_key='a274639d2cc74dbeace399a6250a67b1', filter_route="77").data +
     api_instance.api_web_vehicle_controller_index(api_key='a274639d2cc74dbeace399a6250a67b1', filter_route="79").data +
     api_instance.api_web_vehicle_controller_index(api_key='a274639d2cc74dbeace399a6250a67b1', filter_route="87").data)
print(D)
