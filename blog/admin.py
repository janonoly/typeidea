from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from blog.adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from .models import Post, Category, Tag


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    inlines = [PostInline, ]
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    #obj是当前要保存的对象，form是页面提交过来的表单之后的对象
    #change用于标志本次保存的数据是新增的还是更新的
    #request当前请求
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户的分类'''
    title = '分类过滤器'  #用于展示标题
    parameter_name = 'owner_category'  #查询时URL参数的名字

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


# list_display ：上面已经介绍过，它用来配置列表页面展示哪些字段
# list_display_links ：用来配置哪些字段可以作为链接，点击它们，可以进入编辑页面。
# list_filter ：配置页面过滤器，需要通过哪些字段来过滤列表页 上面我们配置了
# category ，这意味着可以通过 category 中的值来对数据进行过滤
# search_fields ：配置搜索字段
# actions一。n_t句：动作相关的配置，是否展示在顶部
# actions on_bottom 动作相关的配置，是否展示在底部
# save_on_top ：保存、编辑、编辑并新建按钮是否在顶部展示
@admin.register(Post,site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


    list_display = [
        'title', 'category', 'status',
        'owner', 'created_time', 'operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True

    exclude = ('owner',)
    fieldsets = (
        ('基础设置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            )
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    filter_horizontal = ('tag',)
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )


    # 自定义函数的参数是固定的，就是当前行的对象 列表页中的每一行数据都对应数据表中的
    # 一条数据，也对应 Mode 个实例自定义函数可以返回 HTML ，但是需要通过 forrnat_htrnl 函数处理， reverse 是根据名称
    # 解析出 URL 地址，这个后面会介绍到 最后的 operator short description 的作用就是指
    # 定表头的展示文案
    def operator(self, obj):
        return  format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return  super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/"
    #                 "bootstrap.min.css", ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


