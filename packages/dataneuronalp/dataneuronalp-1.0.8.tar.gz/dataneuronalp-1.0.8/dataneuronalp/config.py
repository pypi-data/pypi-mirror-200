import os
import requests

def config(API_Token):
    
    try:
        auth_status = (requests.get("http://20.212.37.37:4000/authorize", headers={"x-access-token": API_Token})).json()
        dir_path, _ = os.path.split(__file__)
        if auth_status['status'] == "SUCCESS":
            with open(dir_path + "/config_variables.py", "w") as config_file:
                config_file.write('API_TOKEN = "' + API_Token + '"\n')
        else:
            with open(dir_path + "/config_variables.py", "w") as config_file:
                config_file.write('API_TOKEN = None\n')
    
    except:
        auth_status = {}
        auth_status['status'] = "FAILURE"
        auth_status['response'] = "Failed to connect to the server"
            
    return auth_status


if __name__=='__main__':
    #Step 1 : Setting API Token
    
    API_Token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYzMmM0YTUwNDI0Zjg0OTVmMzJiMGNkZiIsImV4cCI6MTgzMDA3OTY2NH0.y87Yp8DgeS4dyYTTBHfV0fPDIlUWcll3xGutaM-WJx0'

    #Step 2 : Performing Prediction
    authentication_response = config(API_Token)
    print('authentication_response : ',authentication_response)
    from prediction import PredictIssue
    clf = PredictIssue()
    data =  ({'id1': 'Welcome to the DataNeuron Prediction API Documentation! This page will guide you through some general information about the terminology and about formatting and authenticating requests. You can use the menu on the left to jump to the documentation of the endpoints directly.'})
    task_response = clf.predict('tax1', data)
    print('task_response : ',task_response)

    #Step 3 : Fetch Result
    active_tasks = clf.get_active_tasks()
    prediction_result = clf.task_wait(active_tasks[0])
    print('prediction_result : ',prediction_result)