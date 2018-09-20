from django.db import models

# Create your models here.
class GoogleSheet(models.Model):
    id_str =  models.AutoField(primary_key=True)
    from_user = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField()
    created_at = models.CharField(max_length=200, blank=True, null=True)
    time = models.CharField(max_length=200, blank=True, null=True)
    geo_coordinates = models.CharField(max_length=200, blank=True, null=True)
    user_lang = models.CharField(max_length=200, blank=True, null=True)
    in_reply_to_user_id_str = models.CharField(max_length=200, blank=True, null=True)
    in_reply_to_screen_name = models.CharField(max_length=200, blank=True, null=True)
    from_user_id_str = models.CharField(max_length=200, blank=True, null=True)
    in_reply_to_status_id_str = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    profile_image_url = models.CharField(max_length=200, blank=True, null=True)
    user_followers_count = models.CharField(max_length=200, blank=True, null=True)
    user_friends_count = models.CharField(max_length=200, blank=True, null=True)
    user_location = models.CharField(max_length=200, blank=True, null=True)
    status_url = models.CharField(max_length=200, blank=True, null=True)
    entities_str = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return '%s - %s. %s. - %s' % (
        self.from_user, self.created_at, self.source, self.profile_image_url)

    class Meta:
        verbose_name_plural = 'GoogleSheets'
