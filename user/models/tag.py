from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name="tags", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tags"
