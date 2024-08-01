import argparse
import os
import json


def main():
    parser = argparse.ArgumentParser(description='Parses Json and passes arguments to download-artifacts-sh')
    # parser.add_argument("-o", "--organization", default="StaticYolt",
    #                     help="The organization the repository is under")
    parser.add_argument("-a", "--action_run", help="The ID of the workflow that was run")
    parser.add_argument("-c", "--conda_name", help="Name of the packed Conda environment")
    parser.add_argument("-f", "--file_name", default="artifact_info",
                        help="jsonfile containg info about all artifacts created from some repository")
    # parser.add_argument("-r", "--repository", default="nsls2-collection-tiled")
    parser.add_argument("-n", "--org_and_repo_name", default="StaticYolt/nsls2-collection-tiled",
                        help="uses github contexts github.repository to  git info")
    args = parser.parse_args()

    name_info = args.org_and_repo_name.split("/")
    org, repo = name_info[0], name_info[1]

    # Docs: https://docs.github.com/en/rest/actions/artifacts?apiVersion=2022-11-28
    artifact_command = f'''
    gh api \\
            -H \"Accept: application/vnd.github+json\" \\
            -H \"X-GitHub-Api-Version: 2022-11-28\" \\
            /repos/{org}/{repo}/actions/artifacts > {args.file_name}.json
    '''
    os.system(artifact_command)
    with open(f"{args.file_name}.json") as f:
        data = json.load(f)
        for element in data['artifacts']:
            if element['workflow_run'].get('id') == int(args.action_run) and element['name'] == args.conda_name:
                os.system(f"echo \"link: {str(element['url'])}\"")
                os.system(f"GHA_TOKEN={os.environ['GHA_TOKEN']} bash {os.environ['ACTION_PATH']}/download_artifacts.sh {repo} {org} {str(element['id'])} {str(element['name'])}")

                print(repo)
                print(org)
                print(str(element['id']))
                print(str(element['name']))

if __name__ == "__main__":
    main()