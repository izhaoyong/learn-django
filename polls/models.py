# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BookInfo(models.Model):
	id = models.BigAutoField(primary_key=True)
	source_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
	create_time = models.DateTimeField()
	info = models.TextField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'book_info'


class BookInfoLocal(models.Model):
	id = models.BigAutoField(primary_key=True)
	source_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
	book_name = models.CharField(max_length=200, blank=True, null=True)
	book_orig_name = models.CharField(max_length=200, blank=True, null=True)
	book_subtitle = models.CharField(max_length=200, blank=True, null=True)
	book_poster_url = models.CharField(max_length=400, blank=True, null=True)
	book_poster_name = models.CharField(max_length=200, blank=True, null=True)
	publish_year = models.CharField(max_length=200, blank=True, null=True)
	author = models.CharField(max_length=200, blank=True, null=True)
	publisher = models.CharField(max_length=500, blank=True, null=True)
	isbn = models.CharField(max_length=50, blank=True, null=True)
	douban_average = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
	douban_rators = models.BigIntegerField(blank=True, null=True)
	create_time = models.DateTimeField()
	update_time = models.DateTimeField()
	hot = models.IntegerField(blank=True, null=True)
	deleted = models.IntegerField(blank=True, null=True)
	name_alias = models.CharField(max_length=1000, blank=True, null=True)
	relative_book_source_id = models.CharField(max_length=1000, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'book_info_local'


class MovieInfo(models.Model):
	id = models.BigAutoField(primary_key=True)
	source_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
	create_time = models.DateTimeField()
	info = models.TextField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'movie_info'


class MovieInfoLocal(models.Model):
	id = models.BigAutoField(primary_key=True)
	source_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
	movie_name = models.CharField(max_length=200, blank=True, null=True)
	movie_orig_name = models.CharField(max_length=200, blank=True, null=True)
	movie_poster_url = models.CharField(max_length=400, blank=True, null=True)
	movie_poster_name = models.CharField(max_length=200, blank=True, null=True)
	country = models.CharField(max_length=200, blank=True, null=True)
	release_time = models.CharField(max_length=200)
	director = models.CharField(max_length=200, blank=True, null=True)
	actors = models.CharField(max_length=2000, blank=True, null=True)
	tags = models.CharField(max_length=2000, blank=True, null=True)
	douban_average = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
	douban_rators = models.BigIntegerField(blank=True, null=True)
	update_time = models.DateTimeField()
	imdb = models.CharField(max_length=50, blank=True, null=True)
	be_on = models.IntegerField(blank=True, null=True)
	hot = models.IntegerField(blank=True, null=True)
	deleted = models.IntegerField(blank=True, null=True)
	genres = models.CharField(max_length=200, blank=True, null=True)
	director_show = models.CharField(max_length=500, blank=True, null=True)
	create_time = models.DateTimeField()
	name_alias = models.CharField(max_length=1000, blank=True, null=True)
	relative_movie_source_id = models.CharField(max_length=1000, blank=True, null=True)
	confirmed = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'movie_info_local'


class TvInfo(models.Model):
	id = models.BigAutoField(primary_key=True)
	source_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
	create_time = models.DateTimeField()
	info = models.TextField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'tv_info'


class TvInfoLocal(models.Model):
	id = models.BigAutoField(primary_key=True)
	source_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
	tv_name = models.CharField(max_length=200, blank=True, null=True)
	tv_orig_name = models.CharField(max_length=200, blank=True, null=True)
	tv_poster_url = models.CharField(max_length=400, blank=True, null=True)
	tv_poster_name = models.CharField(max_length=200, blank=True, null=True)
	country = models.CharField(max_length=200, blank=True, null=True)
	release_time = models.CharField(max_length=200)
	director = models.CharField(max_length=2000, blank=True, null=True)
	actors = models.CharField(max_length=4000, blank=True, null=True)
	tags = models.CharField(max_length=2000, blank=True, null=True)
	imdb = models.CharField(max_length=50, blank=True, null=True)
	douban_average = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
	douban_rators = models.BigIntegerField(blank=True, null=True)
	update_time = models.DateTimeField()
	hot = models.IntegerField(blank=True, null=True)
	category = models.CharField(max_length=50, blank=True, null=True)
	deleted = models.IntegerField(blank=True, null=True)
	season_id = models.TextField(blank=True, null=True)
	season_index = models.IntegerField(blank=True, null=True)
	genres = models.CharField(max_length=200, blank=True, null=True)
	create_time = models.DateTimeField()
	name_alias = models.CharField(max_length=1000, blank=True, null=True)
	relative_tv_source_id = models.CharField(max_length=1000, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'tv_info_local'


class User(models.Model):
	user_id = models.BigAutoField(primary_key=True)
	username = models.CharField(max_length=100, blank=True, null=True)
	email = models.CharField(max_length=100, blank=True, null=True)
	password = models.CharField(max_length=100, blank=True, null=True)
	permission = models.TextField(blank=True, null=True)
	role = models.PositiveIntegerField(blank=True, null=True)

	def __str__(self):
		return self.username

	class Meta:
		managed = False
		db_table = 'user'
