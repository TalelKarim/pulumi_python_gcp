import pulumi 
import pulumi_gcp as gcp
from pulumi_gcp.serviceaccount import IAMBinding, IAMBindingArgs, IAMBindingConditionArgs
import os
from google.cloud.devtools import containeranalysis_v1

registry = gcp.container.Registry("my-registry",
    location="EU",
    project="comworkio")


sa = gcp.serviceaccount.Account("sa",
    account_id="my-service-account-talel2",
    display_name="A service account for testing purpose!")

# Create a key for the service account
key = gcp.serviceaccount.Key("sa-key",
    service_account_id=sa.name,
    private_key_type="TYPE_GOOGLE_CREDENTIALS_FILE",
)

# Export the key value as an output
pulumi.export("service_account_key", key)




#Get the IAM policy for the organization
admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
    role="roles/iam.serviceAccountUser",
    members=["serviceAccount:my-service-account-talel"],
)])


# Define a custom role with necessary permissions and condition
custom_role = gcp.projects.IAMCustomRole("custom-role",
    title="Custom Role Talel",
    description="Custom role with access to the registry and a condition",
    permissions=[
       "artifactregistry.repositories.uploadArtifacts"
    ],
    role_id="myCustomRole2",
)


#Modify the IAM policy for the service account using the custom role
admin_account_iam = IAMBinding("admin-account-iam",
    resource=sa.name,
    args=IAMBindingArgs(
        service_account_id=sa.name,
        condition=IAMBindingConditionArgs(
            expression=registry.id.apply(lambda id: f'resource.name == "{id}"'),
            title="Match registry name"
        ),
        members=[sa.email.apply(lambda email: f"serviceAccount:{email}")],
        role=custom_role.id,
    ),
    opts=pulumi.ResourceOptions(parent=sa)
)

pulumi.export("endpoint", registry.id)



# def get_registry(registry_name, region):
#         registry = gcp.container.get_registry(
#             registry_id=registry_name,
#             location=region
#         )
#         return registry.name


# # Usage example
# hashed_name = "my-registry"
# region = "europe-west9"

# registry_name = get_registry(hashed_name, region)
# if registry_name:
#     pulumi.export("registry_exists", True)
#     pulumi.export("registry_name", registry_name)
# else:
#     pulumi.export("registry_exists", False)


# exists = check_registry_exists(hashed_name, region)
# pulumi.export("registry_exists", exists)