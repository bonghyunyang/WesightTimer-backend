from django.db      import models

class User(models.Model):
    payment            = models.ForeignKey('Payment', on_delete = models.SET_NULL, null = True)
    payment_status     = models.ForeignKey('PaymentStatus', on_delete = models.SET_NULL, null = True)
    user_introduction  = models.ForeignKey('UserIntroduction', on_delete = models.SET_NULL, null = True)
    email              = models.CharField(max_length = 200)
    full_name          = models.CharField(max_length = 100)
    password           = models.CharField(max_length = 200)

    class Meta:
        db_table = 'users'

class UserIntroduction(models.Model):
    location           = models.ForeignKey('Location', on_delete = models.SET_NULL, null = True)
    time_zone          = models.ForeignKey('TimeZone', on_delete = models.SET_NULL, null = True)
    website            = models.CharField(max_length = 1000, null = True)
    tagline            = models.CharField(max_length = 200, null = True)
    introduction       = models.CharField(max_length = 2000, null = True)
    profile_image      = models.CharField(max_length = 200, null = True)

    class Meta:
        db_table = 'user_introductions'

class PlayHistory(models.Model):
    user               = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    content            = models.ForeignKey('content.Content', on_delete = models.SET_NULL, null = True)
    play_count         = models.IntegerField()

    class Meta:
        db_table = 'play_histories'

class Location(models.Model):
    location           = models.CharField(max_length = 50, null = True)

    class Meta:
        db_table = 'locations'

class MyCourseGroup(models.Model):
    user               = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    course             = models.ForeignKey('content.Course', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'my_course_groups'

class TimeZone(models.Model):
    time               = models.CharField(max_length = 100)

    class Meta:
        db_table = 'time_zones'

class PaymentStatus(models.Model):
    status             = models.SmallIntegerField(blank = True, null = True)

    class Meta:
        db_table = 'payment_status'

class Subscription(models.Model):
    subscribe_type     = models.ForeignKey('SubscriptionType', on_delete = models.SET_NULL, null = True)
    status_comment     = models.CharField(max_length = 100, null = True)
    status_date        = models.DateTimeField(auto_now_add = True)
    cycle              = models.CharField(max_length = 50)
    started            = models.DateTimeField(auto_now_add = True, null = True)
    next_bill          = models.DateTimeField(auto_now = True, null = True)
    biling             = models.CharField(max_length = 50, null = True)
    next_cycle         = models.CharField(max_length = 50, null = True)

    class Meta:
        db_table = 'subscriptions'

class Payment(models.Model):
    card               = models.CharField(max_length = 50, null = True)
    number             = models.CharField(max_length = 50, null = True)
    expire_date        = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'payments'

class CampaignCourse(models.Model):
    user               = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    campaign           = models.CharField(max_length = 50, null = True)
    subscription_type  = models.ForeignKey('Subscription', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'campaign_courses'

class SubscriptionType(models.Model):
    subscribe          = models.CharField(max_length = 50, null = True)

    class Meta:
        db_table = 'subscription_types'

class Teacher(models.Model):
    user                 = models.ForeignKey('User', on_delete=models.SET_NULL,null = True)
    gender               = models.ForeignKey('GenderType', on_delete=models.SET_NULL, null  = True)
    location             = models.ForeignKey('Location', on_delete=models.SET_NULL, null = True)
    name                 = models.CharField(max_length = 50)
    unique_name          = models.CharField(max_length = 50, null = True)
    teacher_bio          = models.TextField()
    signup_date          = models.DateTimeField(auto_now_add = True)
    facebook             = models.CharField(max_length = 200, null = True)
    twitter              = models.CharField(max_length = 200, null = True)
    linked_in            = models.CharField(max_length = 200, null = True)
    email                = models.CharField(max_length = 200, null = True)
    facebook_messenger   = models.CharField(max_length = 200, null = True)
    teacher_img          = models.URLField(max_length = 200, null = True)

    class Meta:
        db_table = 'teachers'

class GenderType(models.Model):
    name                 = models.CharField(max_length = 50, null = True)

    class Meta:
        db_table = 'gender_types'

class ReviewGroup(models.Model):
    target_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null =True)
    teacher_review = models.ForeignKey('TeacherReview', on_delete=models.SET_NULL, null=True)

    class Meat:
        db_table = 'review_groups'

class TeacherReview(models.Model):
    user                 = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    review               = models.CharField(max_length = 200)
    write_date           = models.DateTimeField(auto_now_add = True)
    teacher_rating       = models.IntegerField()

    class Meta:
        db_table = 'teacher_reviews'

class TeacherFollow(models.Model):
    user                 = models.ForeignKey('User', on_delete=models.SET_NULL, null = True)
    teacher              = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null = True)

    class Meta:
        db_table = 'teacher_follows'

class Gender(models.Model):
    name                 = models.CharField(max_length = 50, null = True)

    class Meta:
        db_table = 'gender'
