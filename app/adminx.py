from app import models
import xadmin


xadmin.site.register(models.domain)
xadmin.site.register(models.account)
xadmin.site.register(models.record)
xadmin.site.register(models.domainsite)