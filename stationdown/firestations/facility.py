from django.contrib.gis.db import models

#
# FeedEntry is a container for the information stored in each Philly Fire News post
#
class Facility(models.Model):

    ogc_fid = models.AutoField(primary_key=True,db_column='ogc_fid')

    engineId = models.IntegerField(db_column='eng')
    ladderId = models.IntegerField(db_column='lad')
    medicId  = models.IntegerField(db_column='med')
    locationStr = models.CharField(max_length=36,db_column='location')
    point = models.GeometryField(db_column='wkb_geometry')

    def __str__(self):
        return "id:{id} location:{location} x={x} y={y} engine:{engine} ladder:{ladder}".format(
            id=self.ogc_fid,
            location=self.locationStr,
            x=self.point.x,
            y=self.point.y,
            engine=self.engineId,
            ladder=self.ladderId
            )

    class Meta:
        db_table = "fire_dept_facilities"

class FacilityManager(models.Manager):

    def create_feed_entry( self, dataList ):
        facility = FireIncident()
        feedEntry.postTitleStr = dataList.title.encode( 'utf-8','replace' )
        feedEntry.postLinkStr  = dataList.link.encode( 'utf-8','replace' )
        feedEntry.postDateStr  = dataList.published.encode( 'utf-8','replace' )
        
        contentObj = PostContentHtml( dataList.content )
        
        feedEntry.fireDateStr = contentObj.fireDate.encode( 'utf-8','replace' )
        feedEntry.fireTimeStr = contentObj.fireTime.encode( 'utf-8','replace' )
        feedEntry.fireAddressRaw = contentObj.fireAddress.encode( 'utf-8','replace' )
        feedEntry.fireAddressStr = self.scrubAddress( feedEntry.fireAddressRaw )
        feedEntry.fireTypeStr = contentObj.fireType.encode( 'utf-8','replace' )
        feedEntry.fireDetailsStr = contentObj.fireDetails.encode( 'utf-8','replace' )

        return feedEntry