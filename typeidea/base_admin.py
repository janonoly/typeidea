from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    '''
    1.用来自动补充文章、分类、标签、车边蓝、这些model的owner字段
    2.用来针对queryset过滤当前用户的数据
    '''
    exclude = ('owner', )
    
    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin,self).get_queryset(request)
        return qs.filter(owner=request.user)


    #obj是当前要保存的对象，form是页面提交过来的表单之后的对象
    #change用于标志本次保存的数据是新增的还是更新的
    #request当前请求
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)