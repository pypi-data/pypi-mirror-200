from __future__ import annotations

import copy
import datetime

from iambic.core.iambic_enum import IambicManaged


def test_update_access_attribute(mocker, mg):
  from iambic.core.template_generation import update_access_attributes
  from iambic.plugins.v0_1_0.aws.iam.policy.models import ManagedPolicyDocument
  from iambic.plugins.v0_1_0.aws.identity_center.permission_set.models import (
      AWSIdentityCenterPermissionSetProperties,
      AWSIdentityCenterPermissionSetTemplate,
      PermissionSetAccess,
  )

  existing_model = AWSIdentityCenterPermissionSetTemplate(
    metadata_commented_dict={},
    metadata_iambic_fields={
      'metadata_commented_dict',
      'expires_at',
      'access_rules', 'deleted', 'iambic_managed', 'file_path', 'owner'},
    expires_at=None, deleted=False, template_type='NOQ::AWS::IdentityCenter::PermissionSet',
    file_path='../iambic-templates/resources/aws/identity_center/permission_set/awsreadonlyaccess.yaml',
    owner=None, iambic_managed=IambicManaged.UNDEFINED, identifier='AWSReadOnlyAccess',
    properties=AWSIdentityCenterPermissionSetProperties(
      metadata_commented_dict={}, metadata_iambic_fields={'metadata_commented_dict'},
      name='AWSReadOnlyAccess',
      description='This policy grants permissions to view resources and basic metadata across all AWS services',
      relay_state=None, session_duration='PT1H', permissions_boundary=None, inline_policy=None,
      customer_managed_policy_references=[],
      managed_policies=[
        ManagedPolicyDocument(
          metadata_commented_dict={},
          metadata_iambic_fields={'deleted', 'expires_at', 'metadata_commented_dict'},
          expires_at=None, deleted=False, arn='arn:aws:iam::aws:policy/job-function/ViewOnlyAccess')],
      tags=[]), access_rules=[
      PermissionSetAccess(
        metadata_commented_dict={},
        metadata_iambic_fields={'deleted', 'expires_at', 'metadata_commented_dict'},
        expires_at=None, deleted=False,
        included_accounts=[
          'account1', 'account2', 'account3'
        ],
        excluded_accounts=[],
        included_orgs=['o-yfdp0r70sq'],
        excluded_orgs=[], users=[], groups=['AWSSecurityAuditors']
      ),
      PermissionSetAccess(
        metadata_commented_dict={},
        metadata_iambic_fields={'deleted', 'expires_at', 'metadata_commented_dict'},
        expires_at=None, deleted=False, included_accounts=['Noq Log Archive'],
        excluded_accounts=[], included_orgs=['o-yfdp0r70sq'], excluded_orgs=[],
        users=[], groups=['AWSLogArchiveViewers'])], included_orgs=['*'], excluded_orgs=[]
  )
  new_model = copy.deepcopy(existing_model)

  new_model.access_rules[0].included_accounts = ['account1', 'account2', 'account3', 'account4']

  from dateutil.tz import tzlocal

  from iambic.plugins.v0_1_0.aws.models import (
      AWSAccount,
      IdentityCenterDetails,
      Partition,
  )
  from iambic.plugins.v0_1_0.aws.utils import RegionName
  all_provider_children = [
    AWSAccount(
      default_region=RegionName.us_east_1,
      aws_profile=None,
      hub_role_arn=None, external_id=None,
      iambic_managed = IambicManaged.READ_AND_WRITE,
        account_id = '123456789012',
        org_id = 'o-123456',
        account_name = 'test', partition =Partition.AWS,
        variables = [],
        identity_center_details = IdentityCenterDetails(
    region=RegionName.us_east_1,
            instance_arn = 'arn:aws:sso:::instance/ssoins-123456',
            identity_store_id = 'd-123456',
            permission_set_map = {
    'AWSReadOnlyAccess': {'Name': 'AWSReadOnlyAccess',
                          'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223e919c6a1baec/ps-1f0281f0000336b3',
                          'Description': 'This policy grants permissions to view resources and basic metadata across all AWS services',
                          'CreatedDate': datetime.datetime(2021, 1, 1, 1, 1, 1, 700000, tzinfo=tzlocal()),
                          'SessionDuration': 'PT1H', 'AttachedManagedPolicies': [
        {'Name': 'ViewOnlyAccess', 'Arn': 'arn:aws:iam::aws:policy/job-function/ViewOnlyAccess'}],
                          'assignments': {'user': {}, 'group': {'1234567890-456af6fc-9047-47df-a394-3829d34b62d9': {
                            'accounts': ['123456789012', '223456789012', '323456789012'],
                              'GroupId': '1234567890-456af6fc-9047-47df-a394-3829d34b62d9',
                            'DisplayName': 'AWSSecurityAuditors',
                            'Description': 'Read-only access to all accounts for security audits',
                            'IdentityStoreId': 'd-1234567890'}, '1234567890-6b86f3fe-fc90-40dd-bdb4-c366b9af856b': {
                            'accounts': ['1234567890'], 'GroupId': '1234567890-6b86f3fe-fc90-40dd-bdb4-c366b9af856b',
                            'DisplayName': 'AWSLogArchiveViewers',
                            'Description': 'Read-only access to log archive account',
                            'IdentityStoreId': 'd-1234567890'}}}},
    'AWSServiceCatalogEndUserAccess': {'Name': 'AWSServiceCatalogEndUserAccess',
                                       'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223e919c6a1baec/ps-81538fa15c7d1e5f',
                                       'Description': 'Provides access to the AWS Service Catalog end user console',
                                       'CreatedDate': datetime.datetime(2022, 6, 14, 11, 14, 26, 722000,
                                                                        tzinfo=tzlocal()), 'SessionDuration': 'PT1H',
                                       'InlinePolicy': '{"Version": "2012-10-17","Statement": [{"Sid": "AWSControlTowerAccountFactoryAccess","Effect": "Allow","Action": ["sso:GetProfile","sso:CreateProfile", "sso:UpdateProfile","sso:AssociateProfile","sso:CreateApplicationInstance","sso:GetSSOStatus","sso:GetTrust","sso:CreateTrust","sso:UpdateTrust","sso:GetPeregrineStatus","sso:GetApplicationInstance","sso:ListDirectoryAssociations","sso:ListPermissionSets","sso:GetPermissionSet","sso:ProvisionApplicationInstanceForAWSAccount","sso:ProvisionApplicationProfileForAWSAccountInstance","sso:ProvisionSAMLProvider","sso:ListProfileAssociations","sso-directory:ListMembersInGroup","sso-directory:SearchGroups","sso-directory:SearchGroupsWithGroupName","sso-directory:SearchUsers","sso-directory:CreateUser","sso-directory:DescribeGroups","sso-directory:DescribeDirectory","sso-directory:GetUserPoolInfo","controltower:CreateManagedAccount","controltower:DescribeManagedAccount","controltower:DeregisterManagedAccount","s3:GetObject","organizations:describeOrganization","sso:DescribeRegisteredRegions"],"Resource": "*"}]}',
                                       'AttachedManagedPolicies': [{'Name': 'AWSServiceCatalogEndUserFullAccess',
                                                                    'Arn': 'arn:aws:iam::aws:policy/AWSServiceCatalogEndUserFullAccess'}],
                                       'assignments': {'user': {}, 'group': {
                                         '90676f6acb-626ce36d-859e-4197-8b51-6eebdd61c781': {
                                           'accounts': ['259868150464'],
                                           'GroupId': '90676f6acb-626ce36d-859e-4197-8b51-6eebdd61c781',
                                           'DisplayName': 'AWSAccountFactory',
                                           'Description': 'Read-only access to account factory in AWS Service Catalog for end users',
                                           'IdentityStoreId': 'd-90676f6acb'}}}},
    'AWSOrganizationsFullAccess': {'Name': 'AWSOrganizationsFullAccess',
                                   'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223e919c6a1baec/ps-bbca575b465bb10c',
                                   'Description': 'Provides full access to AWS Organizations',
                                   'CreatedDate': datetime.datetime(2022, 6, 14, 11, 14, 27, 985000, tzinfo=tzlocal()),
                                   'SessionDuration': 'PT1H', 'AttachedManagedPolicies': [
        {'Name': 'AWSOrganizationsFullAccess', 'Arn': 'arn:aws:iam::aws:policy/AWSOrganizationsFullAccess'}],
                                   'assignments': {'user': {}, 'group': {
                                     '90676f6acb-50074cf1-81e0-4a8e-9257-23678dcf73f8': {
                                       'accounts': ['350876197038', '518317429440', '694815895589', '759357822767',
                                                    '894599878328', '940552945933', '972417093400'],
                                       'GroupId': '90676f6acb-50074cf1-81e0-4a8e-9257-23678dcf73f8',
                                       'DisplayName': 'AWSControlTowerAdmins',
                                       'Description': 'Admin rights to AWS Control Tower core and provisioned accounts',
                                       'IdentityStoreId': 'd-90676f6acb'}}}},
    'ViewOnlyAccess': {'Name': 'ViewOnlyAccess',
                       'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223e919c6a1baec/ps-6486581c00275d6c',
                       'CreatedDate': datetime.datetime(2021, 9, 13, 22, 6, 34, 677000, tzinfo=tzlocal()),
                       'SessionDuration': 'PT1H', 'AttachedManagedPolicies': [
        {'Name': 'ViewOnlyAccess', 'Arn': 'arn:aws:iam::aws:policy/job-function/ViewOnlyAccess'}],
                       'assignments': {'user': {}, 'group': {}}}, 'AdministratorAccess': {'Name': 'AdministratorAccess',
                                                                                          'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223e919c6a1baec/ps-ff451eecbf6ca4f7',
                                                                                          'CreatedDate': datetime.datetime(
                                                                                            2021, 10, 18, 10, 9, 42,
                                                                                            88000, tzinfo=tzlocal()),
                                                                                          'SessionDuration': 'PT1H',
                                                                                          'AttachedManagedPolicies': [{
                                                                                                                        'Name': 'AdministratorAccess',
                                                                                                                        'Arn': 'arn:aws:iam::aws:policy/AdministratorAccess'}],
                                                                                          'assignments': {'user': {},
                                                                                                          'group': {
                                                                                                            '90676f6acb-aa3dd60b-2ec9-472f-8b20-b041c58e26c3': {
                                                                                                              'accounts': [
                                                                                                                '114567474685',
                                                                                                                '197024362139',
                                                                                                                '242350334841',
                                                                                                                '258300530029',
                                                                                                                '259868150464',
                                                                                                                '306086318698',
                                                                                                                '350876197038',
                                                                                                                '404594182786',
                                                                                                                '420317713496',
                                                                                                                '430422300865',
                                                                                                                '518317429440',
                                                                                                                '615395543222',
                                                                                                                '694815895589',
                                                                                                                '759357822767',
                                                                                                                '775726381634',
                                                                                                                '869532243584',
                                                                                                                '894599878328',
                                                                                                                '940552945933',
                                                                                                                '969947703986',
                                                                                                                '972417093400'],
                                                                                                              'GroupId': '90676f6acb-aa3dd60b-2ec9-472f-8b20-b041c58e26c3',
                                                                                                              'DisplayName': 'admins',
                                                                                                              'IdentityStoreId': 'd-90676f6acb'}}}},
    'AWSServiceCatalogAdminFullAccess': {'Name': 'AWSServiceCatalogAdminFullAccess',
                                         'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223e919c6a1baec/ps-c6448c8024d926d5',
                                         'Description': 'Provides full access to AWS Service Catalog admin capabilities',
                                         'CreatedDate': datetime.datetime(2022, 6, 14, 11, 14, 27, 137000,
                                                                          tzinfo=tzlocal()), 'SessionDuration': 'PT1H',
                                         'AttachedManagedPolicies': [{'Name': 'AWSServiceCatalogAdminFullAccess',
                                                                      'Arn': 'arn:aws:iam::aws:policy/AWSServiceCatalogAdminFullAccess'}],
                                         'assignments': {'user': {}, 'group': {
                                           '90676f6acb-154e6d05-a3db-4003-9c96-17d6d2932e80': {
                                             'accounts': ['259868150464'],
                                             'GroupId': '90676f6acb-154e6d05-a3db-4003-9c96-17d6d2932e80',
                                             'DisplayName': 'AWSServiceCatalogAdmins',
                                             'Description': 'Admin rights to account factory in AWS Service Catalog',
                                             'IdentityStoreId': 'd-90676f6acb'}}}},
    'AWSPowerUserAccess': {'Name': 'AWSPowerUserAccess',
                           'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223e919c6a1baec/ps-1c3875e1e53318de',
                           'Description': 'Provides full access to AWS services and resources, but does not allow management of Users and groups',
                           'CreatedDate': datetime.datetime(2022, 6, 14, 11, 14, 27, 413000, tzinfo=tzlocal()),
                           'SessionDuration': 'PT1H', 'AttachedManagedPolicies': [
        {'Name': 'PowerUserAccess', 'Arn': 'arn:aws:iam::aws:policy/PowerUserAccess'}], 'assignments': {'user': {},
                                                                                                        'group': {
                                                                                                          '90676f6acb-32f256f2-7e12-424e-ab3e-6bfcf6d3c076': {
                                                                                                            'accounts': [
                                                                                                              '259868150464',
                                                                                                              '350876197038',
                                                                                                              '420317713496',
                                                                                                              '430422300865',
                                                                                                              '518317429440',
                                                                                                              '694815895589',
                                                                                                              '759357822767',
                                                                                                              '894599878328',
                                                                                                              '940552945933',
                                                                                                              '972417093400'],
                                                                                                            'GroupId': '90676f6acb-32f256f2-7e12-424e-ab3e-6bfcf6d3c076',
                                                                                                            'DisplayName': 'AWSSecurityAuditPowerUsers',
                                                                                                            'Description': 'Power user access to all accounts for security audits',
                                                                                                            'IdentityStoreId': 'd-90676f6acb'}}}},
    'AWSAdministratorAccess': {'Name': 'AWSAdministratorAccess',
                               'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223e919c6a1baec/ps-9525fb1dcf7a9d34',
                               'Description': 'Provides full access to AWS services and resources',
                               'CreatedDate': datetime.datetime(2022, 6, 14, 11, 14, 26, 355000, tzinfo=tzlocal()),
                               'SessionDuration': 'PT1H', 'AttachedManagedPolicies': [
        {'Name': 'AdministratorAccess', 'Arn': 'arn:aws:iam::aws:policy/AdministratorAccess'}], 'assignments': {
        'user': {'90676f6acb-ba3a0faa-72ae-4cf6-ac73-6afdc9c406a6': {'accounts': ['894599878328'],
                                                                     'UserName': 'aws_zelkova_account@noq.dev',
                                                                     'UserId': '90676f6acb-ba3a0faa-72ae-4cf6-ac73-6afdc9c406a6',
                                                                     'Name': {'FamilyName': 'User',
                                                                              'GivenName': 'Admin'},
                                                                     'DisplayName': 'Admin User', 'Emails': [
            {'Value': 'aws_zelkova_account@noq.dev'}], 'IdentityStoreId': 'd-90676f6acb'},
                 '90676f6acb-ea281d52-f52a-4179-98a0-3b57a7fd1b82': {'accounts': ['350876197038', '759357822767'],
                                                                     'UserName': 'aws_development_account@noq.dev',
                                                                     'UserId': '90676f6acb-ea281d52-f52a-4179-98a0-3b57a7fd1b82',
                                                                     'Name': {'FamilyName': 'User',
                                                                              'GivenName': 'Admin'},
                                                                     'DisplayName': 'Admin User', 'Emails': [
                     {'Value': 'aws_development_account@noq.dev'}], 'IdentityStoreId': 'd-90676f6acb'},
                 '90676f6acb-e1bfc7b5-cefb-41b4-96cb-cde4708f40c0': {'accounts': ['940552945933'],
                                                                     'UserName': 'curtis@noq.dev',
                                                                     'UserId': '90676f6acb-e1bfc7b5-cefb-41b4-96cb-cde4708f40c0',
                                                                     'Name': {'FamilyName': 'User',
                                                                              'GivenName': 'Admin'},
                                                                     'DisplayName': 'Admin User',
                                                                     'Emails': [{'Value': 'curtis@noq.dev'}],
                                                                     'IdentityStoreId': 'd-90676f6acb'}}, 'group': {
          '90676f6acb-50074cf1-81e0-4a8e-9257-23678dcf73f8': {
            'accounts': ['259868150464', '420317713496', '430422300865'],
            'GroupId': '90676f6acb-50074cf1-81e0-4a8e-9257-23678dcf73f8', 'DisplayName': 'AWSControlTowerAdmins',
            'Description': 'Admin rights to AWS Control Tower core and provisioned accounts',
            'IdentityStoreId': 'd-90676f6acb'},
          '90676f6acb-33fd6c99-dd4d-4ad5-a438-a0278921dc4a': {'accounts': ['430422300865'],
                                                              'GroupId': '90676f6acb-33fd6c99-dd4d-4ad5-a438-a0278921dc4a',
                                                              'DisplayName': 'AWSLogArchiveAdmins',
                                                              'Description': 'Admin rights to log archive account',
                                                              'IdentityStoreId': 'd-90676f6acb'},
          '90676f6acb-782406d0-fe73-4c54-a3b8-6dd73d67736a': {'accounts': ['420317713496'],
                                                              'GroupId': '90676f6acb-782406d0-fe73-4c54-a3b8-6dd73d67736a',
                                                              'DisplayName': 'AWSAuditAccountAdmins',
                                                              'Description': 'Admin rights to cross-account audit account',
                                                              'IdentityStoreId': 'd-90676f6acb'}}}},
    'DataScientist': {'Name': 'DataScientist',
                      'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-7223e919c6a1baec/ps-0e02c2e21f3d096b',
                      'CreatedDate': datetime.datetime(2022, 12, 22, 13, 13, 2, 184000, tzinfo=tzlocal()),
                      'SessionDuration': 'PT1H', 'AttachedManagedPolicies': [
        {'Name': 'DataScientist', 'Arn': 'arn:aws:iam::aws:policy/job-function/DataScientist'}],
                      'assignments': {'user': {}, 'group': {}}}},
            user_map = {
    '90676f6acb-ba3a0faa-72ae-4cf6-ac73-6afdc9c406a6': {'UserName': 'aws_zelkova_account@noq.dev',
                                                        'UserId': '90676f6acb-ba3a0faa-72ae-4cf6-ac73-6afdc9c406a6',
                                                        'Name': {'FamilyName': 'User', 'GivenName': 'Admin'},
                                                        'DisplayName': 'Admin User',
                                                        'Emails': [{'Value': 'aws_zelkova_account@noq.dev'}],
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-1507af32-49ae-4d56-9864-2912a6c853b6': {'UserName': 'will@noq.dev',
                                                        'UserId': '90676f6acb-1507af32-49ae-4d56-9864-2912a6c853b6',
                                                        'Name': {'FamilyName': 'Beasley', 'GivenName': 'Will'},
                                                        'DisplayName': 'Will Beasley', 'Emails': [
        {'Value': 'will@noq.dev', 'Type': 'work', 'Primary': True}], 'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-ea281d52-f52a-4179-98a0-3b57a7fd1b82': {'UserName': 'aws_development_account@noq.dev',
                                                        'UserId': '90676f6acb-ea281d52-f52a-4179-98a0-3b57a7fd1b82',
                                                        'Name': {'FamilyName': 'User', 'GivenName': 'Admin'},
                                                        'DisplayName': 'Admin User',
                                                        'Emails': [{'Value': 'aws_development_account@noq.dev'}],
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-ecfdb7bf-8a3a-4af7-b33b-99f59f5a236f': {'UserName': 'ccastrapel',
                                                        'UserId': '90676f6acb-ecfdb7bf-8a3a-4af7-b33b-99f59f5a236f',
                                                        'Name': {'FamilyName': 'Curtis', 'GivenName': 'Curtis'},
                                                        'DisplayName': 'ccastrapel', 'Emails': [
        {'Value': 'ccastrapel@gmail.com', 'Type': 'work', 'Primary': True}], 'Addresses': [{'Type': 'work'}],
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-e1bfc7b5-cefb-41b4-96cb-cde4708f40c0': {'UserName': 'curtis@noq.dev',
                                                        'UserId': '90676f6acb-e1bfc7b5-cefb-41b4-96cb-cde4708f40c0',
                                                        'Name': {'FamilyName': 'User', 'GivenName': 'Admin'},
                                                        'DisplayName': 'Admin User',
                                                        'Emails': [{'Value': 'curtis@noq.dev'}],
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-617c7ced-6981-4e98-b39a-18d2724fdb0a': {'UserName': 'matt@noq.dev',
                                                        'UserId': '90676f6acb-617c7ced-6981-4e98-b39a-18d2724fdb0a',
                                                        'Name': {'FamilyName': 'Daue', 'GivenName': 'Matt'},
                                                        'DisplayName': 'Matt Daue', 'Emails': [
        {'Value': 'matt@noq.dev', 'Type': 'work', 'Primary': True}], 'IdentityStoreId': 'd-90676f6acb'}}, group_map = {
    '90676f6acb-456af6fc-9047-47df-a394-3829d34b62d9': {'GroupId': '90676f6acb-456af6fc-9047-47df-a394-3829d34b62d9',
                                                        'DisplayName': 'AWSSecurityAuditors',
                                                        'Description': 'Read-only access to all accounts for security audits',
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-32f256f2-7e12-424e-ab3e-6bfcf6d3c076': {'GroupId': '90676f6acb-32f256f2-7e12-424e-ab3e-6bfcf6d3c076',
                                                        'DisplayName': 'AWSSecurityAuditPowerUsers',
                                                        'Description': 'Power user access to all accounts for security audits',
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-50074cf1-81e0-4a8e-9257-23678dcf73f8': {'GroupId': '90676f6acb-50074cf1-81e0-4a8e-9257-23678dcf73f8',
                                                        'DisplayName': 'AWSControlTowerAdmins',
                                                        'Description': 'Admin rights to AWS Control Tower core and provisioned accounts',
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-154e6d05-a3db-4003-9c96-17d6d2932e80': {'GroupId': '90676f6acb-154e6d05-a3db-4003-9c96-17d6d2932e80',
                                                        'DisplayName': 'AWSServiceCatalogAdmins',
                                                        'Description': 'Admin rights to account factory in AWS Service Catalog',
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-33fd6c99-dd4d-4ad5-a438-a0278921dc4a': {'GroupId': '90676f6acb-33fd6c99-dd4d-4ad5-a438-a0278921dc4a',
                                                        'DisplayName': 'AWSLogArchiveAdmins',
                                                        'Description': 'Admin rights to log archive account',
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-626ce36d-859e-4197-8b51-6eebdd61c781': {'GroupId': '90676f6acb-626ce36d-859e-4197-8b51-6eebdd61c781',
                                                        'DisplayName': 'AWSAccountFactory',
                                                        'Description': 'Read-only access to account factory in AWS Service Catalog for end users',
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-be16557e-f573-4863-92ac-fba1063b45d5': {'GroupId': '90676f6acb-be16557e-f573-4863-92ac-fba1063b45d5',
                                                        'DisplayName': 'group1', 'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-aa3dd60b-2ec9-472f-8b20-b041c58e26c3': {'GroupId': '90676f6acb-aa3dd60b-2ec9-472f-8b20-b041c58e26c3',
                                                        'DisplayName': 'admins', 'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-782406d0-fe73-4c54-a3b8-6dd73d67736a': {'GroupId': '90676f6acb-782406d0-fe73-4c54-a3b8-6dd73d67736a',
                                                        'DisplayName': 'AWSAuditAccountAdmins',
                                                        'Description': 'Admin rights to cross-account audit account',
                                                        'IdentityStoreId': 'd-90676f6acb'},
    '90676f6acb-6b86f3fe-fc90-40dd-bdb4-c366b9af856b': {'GroupId': '90676f6acb-6b86f3fe-fc90-40dd-bdb4-c366b9af856b',
                                                        'DisplayName': 'AWSLogArchiveViewers',
                                                        'Description': 'Read-only access to log archive account',
                                                        'IdentityStoreId': 'd-90676f6acb'}}, org_account_map = {
    '420317713496': 'Noq Audit', '306086318698': 'global_tenant_data_prod', '894599878328': 'zelkova',
    '869532243584': 'nonstandard_org_role', '242350334841': 'test', '940552945933': 'production',
    '694815895589': 'demo-2', '242345320040': 'iambic_open_source', '969947703986': '@!#!@#)(%*#R)QWITFGO)FG+=0984',
    '972417093400': 'demo-1', '430422300865': 'Noq Log Archive', '404594182786': 'ses',
    '114567474685': 'space in account name', '258300530029': 'global_prod_tenant_data', '759357822767': 'development',
    '259868150464': 'staging', '518317429440': 'demo-3', '197024362139': 'unusual_demo',
    '775726381634': 'Cyberdyne Demo Org', '350876197038': 'development-2',
    '615395543222': 'global_tenant_data_staging'}), spoke_role_arn = 'arn:aws:iam::259868150464:role/IambicSpokeRole')]

  update_access_attributes(

  )
