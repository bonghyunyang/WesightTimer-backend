from django.db         import models

class RootCategory(models.Model):
    name  = models.CharField(max_length = 50)

    class Meta:
        db_table = 'root_categories'

class MiddleCategory(models.Model):
    root_category = models.ForeignKey('RootCategory', on_delete=models.SET_NULL, null=True)
    name          = models.CharField(max_length = 50)

    class Meta:
        db_table = 'middle_categories'

class EndCategory(models.Model):
    middle_category = models.ForeignKey('MiddleCategory', on_delete=models.SET_NULL, null=True)
    name            = models.CharField(max_length = 50)


    class Meta:
        db_table = 'end_categories'

class MiddleContentTag(models.Model):
    middle_category  = models.ForeignKey('MiddleCategory', on_delete=models.SET_NULL, null=True)
    content          = models.ForeignKey('Content', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'middle_content_tags'

class EndContentTag(models.Model):
    end_categorry  = models.ForeignKey('EndCategory', on_delete=models.SET_NULL, null=True)
    content        = models.ForeignKey('content', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'end_content_tags'

class Content(models.Model):
    teacher          = models.ForeignKey('user.Teacher', on_delete=models.SET_NULL, null=True)
    content_type     = models.ForeignKey('ContentType', on_delete=models.SET_NULL, null=True)
    activity_type    = models.ForeignKey('ActivityType', on_delete=models.SET_NULL, null=True)
    target           = models.ForeignKey('Target', on_delete=models.SET_NULL, null=True)
    title            = models.CharField(max_length = 100)
    description      = models.CharField(max_length = 2000)
    image_url        = models.URLField(max_length = 2000)
    running_time     = models.CharField(max_length = 50)
    file_source      = models.CharField(max_length = 2000)
    course_img       = models.CharField(max_length = 300)

    class Meta:
        db_table = 'contents'

class ContentType(models.Model):
    name   = models.CharField(max_length = 50)

    class Meta:
        db_table = 'content_types'

class ActivityType(models.Model):
    name   = models.CharField(max_length = 50)

    class Meta:
        db_table = 'activity_types'

class Target(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'targets'

class ContentReview(models.Model):
    content         = models.ForeignKey('Content', on_delete=models.SET_NULL, null=True)
    user            = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    content_rating  = models.ForeignKey('ContentRating', on_delete=models.SET_NULL, null=True)
    review          = models.CharField(max_length = 2000)
    write_date      = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'content_reviews'

class ContentRating(models.Model):
    rating = models.IntegerField(default = 0)

    class Meta:
        db_table = 'content_ratings'

class Course(models.Model):
    payment_status  = models.ForeignKey('user.PaymentStatus', on_delete=models.SET_NULL, null=True)
    teacher         = models.ForeignKey('user.Teacher', on_delete=models.SET_NULL, null=True)
    course_name     = models.CharField(max_length =50)
    course_info     = models.CharField(max_length = 2000)

    class Meta:
        db_table = 'courses'

class CourseContent(models.Model):
    course           = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)
    lesson_title     = models.CharField(max_length = 100)
    lesson_describe  = models.CharField(max_length = 2000)

    class Meta:
        db_table = 'course_contents'

class CourseReview(models.Model):
    user          = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    course        = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)
    course_rating = models.ForeignKey('CourseRating', on_delete=models.SET_NULL, null=True)
    review        = models.CharField(max_length = 2000)
    write_date    = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'course_reviews'

class CourseRating(models.Model):
    rating  = models.IntegerField(default = 0)

    class Meta:
        db_table = 'course_ratings'

class PlayList(models.Model):
    teacher   = models.ForeignKey('user.Teacher', on_delete=models.SET_NULL, null=True)
    title     = models.CharField(max_length = 100)
    describe  = models.CharField(max_length = 2000)
    pick      = models.BooleanField()

    class Meta:
        db_table = 'play_lists'

class TagGroup(models.Model):
    play_list = models.ForeignKey('PlayList', on_delete=models.SET_NULL, null=True)
    tag_list  = models.ForeignKey('TagList', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'tag_groups'

class TagList(models.Model):
    tag  = models.CharField(max_length = 50)

    class Meta:
        db_table = 'tag_lists'

class PlayListGroup(models.Model):
    play_list  = models.ForeignKey('PlayList', on_delete=models.SET_NULL, null=True)
    content    = models.ForeignKey('Content', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'play_list_groups'

class PlayListFollower(models.Model):
    user      = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    play_list = models.ForeignKey('PlayList', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'play_list_followers'
