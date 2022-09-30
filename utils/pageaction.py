"""# 根据自己的情况去筛选数据
queryset = models.Admin.objects.all()
page_object=PageInaction(request, queryset)
 context = {
        "queryset":page_obj.page_queryset,
        "page_string":page_obj.html()
   }
return render(request, "admin_list.html", context)
在html 页面中，
{% for obj in queryset %}
 <tr>
<th scope="row">{{ obj.id }}</th>
<td>{{ obj.username }}</td>
</tr>
 {% endfor %}

 <ul class="pagination">
        {{ page_string }}
 </ul>
"""
from django.utils.safestring import mark_safe
class PageInaction(object):
    def __init__(self,request,queryset,page_size=10,page_param="page"):
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        print(type(query_dict))
        print(request.GET)
        self.query_dict=query_dict
        query_dict.setlist("page", [11])
        self.page_param=page_param
        print(query_dict.urlencode())

        page = request.GET.get(page_param,"1")
        print("pageGGG:",page)
        if page.isdecimal():
            page=int(page)
        else:
            page=1
        self.page=page
        self.page_size=page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset=queryset[self.start:self.end]

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count=total_page_count

    def html(self):
        page_str_list = []
        self.query_dict.setlist(self.page_param,[1])

        print(self.query_dict.urlencode())

        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page -1])
            page_str_list.append('<li><a href="?{}">Pre</a></li>'.format(self.query_dict.urlencode()))
        else:
            self.query_dict.setlist(self.page_param, [1])
            page_str_list.append('<li><a href="?{}">Pre</a></li>'.format(self.query_dict.urlencode()))
        for i in range(1, self.total_page_count + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                eli = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                eli = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(eli)
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page +1])
            page_str_list.append('<li><a href="?{}">Next</a></li>'.format(self.query_dict.urlencode()))
        else:
            self.query_dict.setlist(self.page_param, [self.page])
            page_str_list.append('<li><a href="?{}">Next</a></li>'.format(self.query_dict.urlencode()))

        page_string = mark_safe("".join(page_str_list))
        return page_string