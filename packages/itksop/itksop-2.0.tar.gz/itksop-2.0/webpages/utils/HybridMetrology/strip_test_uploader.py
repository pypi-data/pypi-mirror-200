import os
import sys
import argparse
import json
from glob import glob
import mimetypes as mt

#import itkdb
import itkdb

def upload(input_name, project, upload_file = True):
    
    # Read test data from json
    with open (input_name) as f:
        data = json.load(f)
    
    # Get component
    comp = client.get('getComponent', json={"component" : data["component"]})#,"alternativeIdentifier" : data.get("alternativeIdentifier", True)})

#    # Check stage
#    if comp["currentStage"]["code"] != data["currentStage"]:
#        print("WARNING: Component stage in DB {} doesn't match that requested {}.  Skipping".format(comp["currentStage"]["code"], data["currentStage"]))
#        return None
#
#    # Check type
#    if comp["componentType"]["code"] != data["componentType"]:  
#        print("WARNING: Component type in DB {} doesn't match that requested {}.  Skipping".format(comp["componentType"]["code"], data["componentType"]))
#        return None
    
    # Get test template 
    test_template = client.get('generateTestTypeDtoSample', json={"project" : project, "componentType" : data["componentType"], 'code': data["testType"]}) #, 'requiredOnly' : True})


    # Get file name for separate upload, removing from result if an attachment
    attachment = "VISUAL_INSPECTION" in data["testType"] or ("METROLOGY" in data["testType"] and "S" in project)
    if attachment:
        file_name = data["results"].pop("FILE", "")
    else:
        file_name = data["results"].get("FILE", "")        
        
    # Upload test result
    new_test_result = client.post('uploadTestRunResults', json={**test_template, 'component': comp["code"], "institution" : data["institution"],
                                                                "passed" : data["passed"], "problems" : data["problems"], "date" : data["date"],
                                                                "properties" : data["properties"], "results" : data.get("results", {}), 'runNumber': str(data["runNumber"]),
                                                                "comments" : data.get("comments", []), "defects" : data.get("defects", [])})
    
    # Upload file 
    if upload_file and file_name:
        if attachment:
            if "P" in project:
                client.post('createBinaryTestRunParameter', data={"testRun" : new_test_result['testRun']['id'], "parameter" : "IMAGE"}, files={"data" : open(file_name, "rb")})
            else:
                client.post('createTestRunAttachment', data={ "testRun": new_test_result['testRun']['id'], "type" : "file", "title" : os.path.basename(file_name)},
                            files={"data" : (os.path.basename(file_name), open(file_name, "rb"), mt.guess_type(file_name)[0])})                
        else:
            client.post('createBinaryTestRunParameter', data={"testRun" : new_test_result['testRun']['id'], "parameter" : "FILE"}, files = {"data" : open(file_name, "rb")})
    
    # Print results link
    host = "https://uuappg01-eu-w-1.plus4u.net/ucl-itkpd-maing01/"
    link = "{}{}/testRunView?id={}".format(host, new_test_result["componentTestRun"]["awid"], new_test_result['testRun']['id'])
    print("{}\t{}".format(comp["code"], link))
    
    return new_test_result

if __name__ == "__main__":

    # Parse command line
    parser = argparse.ArgumentParser(description="Script for uploading strip hyrbid test results")
    parser.add_argument("json", help="Full name of json file containing test results or directory of json files")
    parser.add_argument("--accessCode1", default = None, help = "Access Code 1 (can also be specified via ITKDB_ACCESS_CODE1 env var)")
    parser.add_argument("--accessCode2", default = None, help = "Access Code 2 (can also be specified via ITKDB_ACCESS_CODE2 env var)")
    parser.add_argument("--project", "-p", default = "S", help = "Project code (S/P)")
    args = parser.parse_args()


    # Authenticate
    if args.accessCode1 and args.accessCode2:
        u = itkdb.core.User(accessCode1=args.accessCode1, accessCode2=args.accessCode2)
        #u = itkdb.core.User(accessCode1="LI.Zhan;2019", accessCode2="Lucule69")
        client = itkdb.Client(user = u)
    elif "ITKDB_ACCESS_CODE1" in os.environ and "ITKDB_ACCESS_CODE1" in os.environ:
        client = itkdb.Client()
    else:
        sys.exit("ERROR: Must provide access codes, either via arguments or environment variables")

    client.user.authenticate()
    user = client.get('getUser', json={'userIdentity': client.user.identity})
    print ('>>> Hello {} {}, welcome to the strip hybrid upload script'.format(user["firstName"], user["lastName"]))

    # Attempt to upload test result
    if args.json.endswith(".json"):
        print(f">>> Uploading {args.json} ...")
        upload(args.json, args.project)
    elif os.path.isdir(args.json):
        files = glob(f"{args.json}/*.json")
        if not files:
            sys.exit(f"ERROR: No json files found in dir {args.json}")
        for f in files:
            print(f">>> Uploading {f} ...")
            upload(args.json, args.project)
    else:
        sys.exit("ERROR: Unknown input format.  Plese provide a json file or directory path containing json files")
            
        
    
