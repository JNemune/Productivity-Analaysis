# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from jdatetime import datetime


class Label(models.Model):
    title = models.TextField(
        primary_key=True
    )  # The composite primary key (title, archived) found, that is not supported. The first column is selected.
    colorid = models.IntegerField(db_column="colorId")  # Field name made lowercase.
    order = models.IntegerField()
    archived = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = "Label"

    def __str__(self):
        return self.title


class Profile(models.Model):
    name = models.TextField(primary_key=True)
    durationwork = models.IntegerField(
        db_column="durationWork"
    )  # Field name made lowercase.
    durationbreak = models.IntegerField(
        db_column="durationBreak"
    )  # Field name made lowercase.
    enablelongbreak = models.IntegerField(
        db_column="enableLongBreak"
    )  # Field name made lowercase.
    durationlongbreak = models.IntegerField(
        db_column="durationLongBreak"
    )  # Field name made lowercase.
    sessionsbeforelongbreak = models.IntegerField(
        db_column="sessionsBeforeLongBreak"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Profile"


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.IntegerField()
    duration = models.IntegerField()
    label = models.ForeignKey(
        Label, models.DO_NOTHING, db_column="label", blank=True, null=True
    )
    archived = models.ForeignKey(
        Label,
        models.DO_NOTHING,
        db_column="archived",
        to_field="archived",
        related_name="session_archived_set",
    )

    class Meta:
        managed = False
        db_table = "Session"

    def __str__(self):
        duration = f"{self.duration//60:02}:{self.duration%60:02}"
        timestamp = datetime.fromtimestamp(self.timestamp / 1000).isoformat(sep=" ")
        return f"{self.id} | {self.label} {duration} {timestamp}"


class AndroidMetadata(models.Model):
    id = models.AutoField(primary_key=True)
    locale = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "android_metadata"


class RoomMasterTable(models.Model):
    id = models.AutoField(primary_key=True)
    identity_hash = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "room_master_table"
