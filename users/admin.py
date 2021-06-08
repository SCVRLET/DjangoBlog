from django.contrib import admin

from .models import User, Post

from .admin_forms import UserForm, PostForm

from django.utils.safestring import mark_safe


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    actions = ['make_admin', 'make_common_user']
    search_fields = ('login',)

    list_display = ['id', 'login', 'email', 'is_email_verified', 'is_admin', 'get_avatar']    

    form = UserForm

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" style="width:70px; height:60px">')
        
        else:
            return mark_safe(f'<img width=75>')

    get_avatar.short_description = 'avatar'

    readonly_fields = (
            'id',
            'login',
            'email',
            'is_email_verified',
            'get_avatar'
    )

    def make_admin(self, request, queryset):
        row_update = queryset.update(is_admin=True)

        message_bit = f'{row_update} new admin(s) added'

        self.message_user(request, f'message_bit')

    
    def make_common_user(self, request, queryset):
        row_update = queryset.update(is_admin=False)

        message_bit = f'{row_update} admin(s) deleted'

        self.message_user(request, f'message_bit')


    make_admin.allowed_permissions = ('change',)
    make_common_user.allowed_permissions = ('change',)


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_filter = ('created_at', )
    list_display = ['id', 'text', 'total_likes']    
    search_fields = ('user_id__id',)

    form = PostForm

    def get_login(self, obj):
        return obj.user_id.login

    def get_id(self, obj):
        return obj.user_id.id

    def get_users_who_liked_post(self, obj):
        ret = ''
        for login in list(list(obj.liked.all().values_list('login'))):
            ret += f'{list(login)[0]}, ' 
        
        return ret

    get_login.short_description = 'login of creator'
    get_id.short_description = 'id of creator'
    get_users_who_liked_post.short_description = 'logins of users, who liked post'
    
    readonly_fields = (
            'get_id',
            'get_login',
            'text',
            'created_at',
            'get_users_who_liked_post',
            'total_likes'
    )

    get_id.admin_order_field = 'Make order by id'
