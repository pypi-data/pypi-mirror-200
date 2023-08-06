from localstack.http import Request,route
from .manager import SnapshotManager
class StateResource:
	'\n    Internal endpoints to trigger state management operations.\n    ';service_state_manager:0
	def __init__(A,service_state_manager):A.service_state_manager=service_state_manager
	@route('/_localstack/state/<service>/load',methods=['POST'])
	def load_service_state(self,request,service):self.service_state_manager.load(service)
	@route('/_localstack/state/<service>/save',methods=['POST'])
	def save_service_state(self,request,service):self.service_state_manager.save(service)