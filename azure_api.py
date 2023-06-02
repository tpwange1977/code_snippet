from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import urllib.request

# Azure DevOps 的個人存取權限(PAT) 
personal_access_token = 'vaoysyweyaahcuvyv6gnupirkklbxvxgksbdojuena6n63oo77ka'
organization_url = 'https://dev.azure.com/tpwange'

# 建立連接
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# 選擇組織和項目
client = connection.clients.get_build_client()
project = 'poc'

# 獲取並列印所有構建
builds = client.get_builds(project)
for build in builds:
    print(f'Build ID: {build.id}, Build Number: {build.build_number}, Status: {build.status}')

    
build_id = 96

# 獲取工件詳情
artifacts = client.get_artifacts(project, build_id)

# 下載每個工件
for artifact in artifacts:
    if artifact.resource.download_url:
        filename = artifact.name + '.zip'
        urllib.request.urlretrieve(artifact.resource.download_url, filename)
        print(f'Downloaded artifact {artifact.name} to {filename}')




#token = "vaoysyweyaahcuvyv6gnupirkklbxvxgksbdojuena6n63oo77ka"


