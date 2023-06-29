import pulumi
import pulumi_gcp as gcp
from pulumi_gcp.serviceaccount import IAMBinding, IAMBindingArgs, IAMBindingConditionArgs
import os
from google.cloud.devtools import containeranalysis_v1
import json


my_repo = gcp.artifactregistry.Repository("my-repo",
    description="example docker repository",
    format="DOCKER",
    location="us-central1",
    repository_id="my-repository")

sa = gcp.serviceaccount.Account("sa",
    account_id="my-service-account",
    display_name="A service account that has access to the artifact repository") 



custom_binding = gcp.artifactregistry.RepositoryIamBinding("custom-binding",
    project=my_repo.project,
    location=my_repo.location,
    repository=my_repo.repository_id,
    role="roles/artifactregistry.reader",
    members=[f"serviceAccount:my-service-account-talel2@comworkio.iam.gserviceaccount.com"],
)

key = gcp.serviceaccount.Key("sa-key",
    service_account_id=sa.name,
    private_key_type="TYPE_GOOGLE_CREDENTIALS_FILE",
)


pulumi.export("service_account_key", key)
pulumi.export("repository_name", my_repo.name)



# admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
#     role="roles/artifactregistry.reader",
#     members=[f"serviceAccount:my-service-account-talel2@comworkio.iam.gserviceaccount.com"],
# )])


# policy = gcp.artifactregistry.RepositoryIamPolicy("policy",
#     project=my_repo.project,
#     location=my_repo.location,
#     repository=my_repo.repository_id,
#     policy_data = admin.policy_data)