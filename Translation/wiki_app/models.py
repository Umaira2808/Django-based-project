from django.db import models

# Create your models here.
class Project(models.Model):
    project_id = models.AutoField(primary_key=True, db_column='Project_id')
    wiki_article = models.CharField(max_length=500, null=True)
    tar_lang = models.CharField(max_length= 300, null=True)

class Sentence(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sentence_id = models.IntegerField()
    original_sentence = models.CharField(max_length= 2000, null=True)
    translated_sentence = models.CharField(max_length= 2000, null=True)

