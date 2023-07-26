## know the permissions in django

```py
from django.contrib.auth.models import Permission
default_permissions = Permission.objects.filter(content_type__app_label='auth') # related to auth
default_permissions = Permission.objects.all() # all
for permission in default_permissions:
    print(permission.codename, permission.name)


```

## different permissions

```txt
add_logentry Can add log entry      
change_logentry Can change log entry
delete_logentry Can delete log entry
view_logentry Can view log entry
add_group Can add group
change_group Can change group
delete_group Can delete group
view_group Can view group
add_permission Can add permission
change_permission Can change permission
delete_permission Can delete permission
view_permission Can view permission
add_user Can add user
change_user Can change user
delete_user Can delete user
view_user Can view user
add_contenttype Can add content type
change_contenttype Can change content type
delete_contenttype Can delete content type
view_contenttype Can view content type
add_med_test1_report Can add med_test1_report
change_med_test1_report Can change med_test1_report
delete_med_test1_report Can delete med_test1_report
view_med_test1_report Can view med_test1_report
add_constant Can add constant
add_constants Can add constants
change_constant Can change constant
change_constants Can change constants
delete_constant Can delete constant
delete_constants Can delete constants
view_constant Can view constant
view_constants Can view constants
add_patient Can add patient
change_patient Can change patient
delete_patient Can delete patient
view_patient Can view patient
add_receipt Can add receipt
change_receipt Can change receipt
delete_receipt Can delete receipt
view_receipt Can view receipt
add_session Can add session
change_session Can change session
delete_session Can delete session
view_session Can view session

```

```py
<p>Current Base URL: {{ request.scheme }}://{{ request.get_host }}/</p>
<p>Current URL: {{ request.build_absolute_uri }}</p>



```