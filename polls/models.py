# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customers(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customernumber = models.CharField(db_column='CustomerNumber', unique=True, max_length=10)  # Field name made lowercase.
    nationalid = models.IntegerField(db_column='NationalID')  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=100)  # Field name made lowercase.
    fathersname = models.CharField(db_column='FathersName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bankaccount = models.CharField(db_column='BankAccount', max_length=30, blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(blank=True, null=True)  # This field type is a guess.
    mobile = models.CharField(db_column='Mobile', max_length=15, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='Telephone', unique=True, max_length=15, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=50, blank=True, null=True)
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Customers'


class Loadtypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LoadTypes'


class Loadings(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    invoicenumber = models.CharField(db_column='InvoiceNumber', unique=True, max_length=10)  # Field name made lowercase.
    loaddate = models.DateTimeField(db_column='LoadDate')  # Field name made lowercase.
    loaddateshamsi = models.CharField(db_column='LoadDateShamsi', max_length=20)  # Field name made lowercase.
    driver = models.CharField(db_column='Driver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vehiclenumber = models.CharField(db_column='VehicleNumber', max_length=15, blank=True, null=True)  # Field name made lowercase.
    customerid = models.CharField(db_column='CustomerID', max_length=10)  # Field name made lowercase.
    waybill = models.CharField(db_column='Waybill', max_length=20, blank=True, null=True)  # Field name made lowercase.
    loadedweight = models.DecimalField(db_column='LoadedWeight', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    unloadedweight = models.DecimalField(db_column='UnloadedWeight', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pureweight = models.DecimalField(db_column='PureWeight', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    loadtype = models.ForeignKey(Loadtypes, models.DO_NOTHING, db_column='LoadType', blank=True, null=True)  # Field name made lowercase.
    vehicletype = models.ForeignKey('Vehiclestype', models.DO_NOTHING, db_column='VehicleType', blank=True, null=True)  # Field name made lowercase.
    invoicetype = models.CharField(db_column='InvoiceType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Loadings'


class Vehiclestype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehiclesType'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)


class TempLoadings(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    invoicenumber = models.CharField(db_column='InvoiceNumber', max_length=10)  # Field name made lowercase.
    loaddate = models.DateTimeField(db_column='LoadDate')  # Field name made lowercase.
    loaddateshamsi = models.CharField(db_column='LoadDateShamsi', max_length=20)  # Field name made lowercase.
    driver = models.CharField(db_column='Driver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vehiclenumber = models.CharField(db_column='VehicleNumber', max_length=15, blank=True, null=True)  # Field name made lowercase.
    customerid = models.CharField(db_column='CustomerID', max_length=10)  # Field name made lowercase.
    waybill = models.CharField(db_column='Waybill', max_length=20, blank=True, null=True)  # Field name made lowercase.
    loadedweight = models.DecimalField(db_column='LoadedWeight', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    unloadedweight = models.DecimalField(db_column='UnloadedWeight', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pureweight = models.DecimalField(db_column='PureWeight', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    loadtype = models.ForeignKey(Loadtypes, models.DO_NOTHING, db_column='LoadType', blank=True, null=True)  # Field name made lowercase.
    vehicletype = models.ForeignKey(Vehiclestype, models.DO_NOTHING, db_column='VehicleType', blank=True, null=True)  # Field name made lowercase.
    invoicetype = models.CharField(db_column='InvoiceType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'temp_loadings'
