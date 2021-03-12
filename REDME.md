# No Staff Flag

As default django user model have `is_staff` flag. is flag used by default django admin to give user permission ot login.

So, in some business case we have different user types, and it's a good idea to have `role` field instead of having separate flag for each role.

But, to delete `is_staff` flag we need to update all default places django auth app use that flag.

**IMPORTANT**
this step need to take on start of project

## required Packages

- Django
