import argument_parser
import myGit
import myInfo
import myTask
import myTest
import argparse
import subprocess as sp
import os

def arg_parser():
    parser = argparse.ArgumentParser(description = '   ')
    parser.add_argument('-p', '--project',  required = True, choices= argument_parser.get_projects(), help = '')
    parser.add_argument('-b', '--bug-ID',   required = True, help = '')

    param_dict = {}
    args = parser.parse_args()
    param_dict["project"] = args.project
    param_dict["bug-ID"] = args.bug_ID
    return param_dict

def main():
    param_dict = arg_parser()
    repository = myGit.get_project_repository(param_dict)
    dirname = str(param_dict["project"])+str(param_dict["bug-ID"])
    output =  "acr-input/"+dirname+"/"
    myGit.clone_repo(repository, output)
    bug_id = str(param_dict["bug-ID"])
    prjname = str(param_dict["project"])

    # Developer patch
    diff_cmd = f"git diff tags/Bug-{bug_id}^ tags/Bug-{bug_id}-full > ../developer_patch.diff"
    sp.call(diff_cmd, shell=True)

    # Gets Buggy version
    checkout_cmd = f"git checkout tags/Bug-{bug_id}^"
    sp.call(checkout_cmd, shell=True)

    # kya chal raha hai
    checkout_cmd = f"python3 ../../../main.py -p {str(param_dict['project'])} -b {bug_id} -t test -v buggy -o output/"
    sp.call(checkout_cmd, shell=True)
    
    sample_prompt = f"The following is the result of running the tests on the Javascript project {param_dict['project']}. \nLook carefully at the tests which are not passing and make required changes to the codebase. \nThe \"err\" field in a test case represents a non passing test. \n"
    
    # Append the contents of test_results.json to test_results.txt
    with open('test_results.json', 'r') as json_file:
        json_data = json_file.read()
    
    if json_data:
        print(f"Successfully ran tests on the project {prjname} with bug id {bug_id}. Prepraring the input")
        # Write the prompt to the file
        with open('../test_results.txt', 'w') as f:
            f.write(sample_prompt)

        with open('../test_results.txt', 'a') as f:
            f.write(json_data)
    
    else:
        checkout_cmd = f"rm -r ../../{dirname}"
        sp.call(checkout_cmd, shell=True)
        raise Exception(f"Cannot run tests on the project {prjname} with bug id {bug_id}. Input not prepared")

    return

if __name__ == "__main__":
    main()




