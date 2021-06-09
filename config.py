import json
#ces-soledad.pih-emr.org

#db user #password stored in json file
dwh_user = "mex-dwh-u1"
with open("user_details.json") as f:
    user_dict = json.load(f)
password = user_dict[dwh_user][user_dict[dwh_user]['type']]

#location and ip dictionary
location_ip_dict = {"Soledad": "10.160.10.16:3306",
                    "Reforma":""
                    }

schema = "openmrs"
#list of tables to be extracted
table_list = ["location","obs"]
#["concept","concept_description",""concept_name"","drug","encounter","location","obs"]
#["patient","person","program", "provider", "relationship", "visit"]

#Azure config file
container_token = "sp=rwleo&st=2021-05-18T00:00:00Z&se=2021-05-22T00:22:37Z&sv=2020-02-10&sr=c&sig=UH5%2FwoheNGRwVChX0Tr0PB%2FNYyroSqV86KH8uCD2M5I%3D"
container_url = ""
blob_token = ""
blob_url = ""
