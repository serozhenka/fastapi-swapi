import datetime

from tortoise import models, fields


class CsvFile(models.Model):
    id = fields.IntField(pk=True)
    filename = fields.CharField(max_length=64)
    created = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"fetch {self.format_datetime(self.created)}"

    def format_datetime(self, date_time: datetime) -> str:
        return date_time.strftime('%d %b %Y %H:%M')

    class Meta:
        ordering = ['-created']


class LastFetch(models.Model):
    id = fields.IntField(pk=True)
    datetime = fields.DatetimeField()

    def __str__(self):
        return "last_fetch"