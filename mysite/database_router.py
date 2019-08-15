from django.conf import settings


DATABASES_APPS_MAPPING = settings.DATABASES_APPS_MAPPING

class DatabaseAppsRouter(object):
	def db_for_read(self, model, **hints):
		if model._meta.app_label in DATABASES_APPS_MAPPING:
			return DATABASES_APPS_MAPPING[model._meta.app_label]
		return None

	def db_for_write(self, model, **hints):
		if model._meta.app_label in DATABASES_APPS_MAPPING:
			return DATABASES_APPS_MAPPING[model._meta.app_label]
		return None

	def allow_relation(self, obj1, obj2, **hints):
		db_obj1 = DATABASES_APPS_MAPPING.get(obj1._meta.app_label)
		db_obj2 = DATABASES_APPS_MAPPING.get(obj2._meta.app_label)

		if db_obj1 and db_obj2:
			if db_obj1 == db_obj2:
				return True
			else:
				return False
		return None

	def allow_syncdb(self, db, model):
		if db in DATABASES_APPS_MAPPING.values():
			return DATABASES_APPS_MAPPING.get(model._meta.app_label) == db
		elif model._meta.app_label in DATABASES_APPS_MAPPING:
			return False
		return None

	def allow_migrate(self, db, app_label, model=None, **hints):
		if db in DATABASES_APPS_MAPPING.values():
			return DATABASES_APPS_MAPPING.get(app_label) == db
		elif app_label in DATABASES_APPS_MAPPING
			return False
		return None
