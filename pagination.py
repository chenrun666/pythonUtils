"""
分页组件
"""
from django.utils.html import mark_safe


class Pagination(object):

    def __init__(self, request, all_count, base_url, query_params, per_num=10, max_show=11):
        try:
            current_page = int(request.GET.get('page'))
            if current_page <= 0:
                raise Exception()
        except Exception as e:
            current_page = 1
        self.base_url = base_url
        self.current_page = current_page
        self.query_params = query_params
        self.max_show = max_show
        self.half_show = max_show // 2
        self.all_count = all_count
        self.per_num = per_num
        self.total_page, more = divmod(self.all_count, self.per_num)
        if more:
            self.total_page += 1

    @property
    def start(self):
        return (self.current_page - 1) * self.per_num

    @property
    def end(self):
        return self.current_page * self.per_num

    @property
    def html_str(self):
        # 计算起始页码数和终止页码数
        # 总页码数小于最大显示的页码数
        if self.total_page < self.max_show:
            page_start = 1
            page_end = self.total_page
        else:
            if self.current_page <= self.half_show:
                # 总页码数大于最大显示页码数
                page_start = 1
                page_end = self.max_show
            elif self.current_page + self.half_show > self.total_page:
                page_start = self.total_page - self.max_show + 1
                page_end = self.total_page
            else:
                page_start = self.current_page - self.half_show
                page_end = self.current_page + self.half_show
        html_list = []
        if self.current_page <= 1:
            prev_li = '<li class="disabled"><a><上一页></a></li>'
        else:
            self.query_params['page'] = self.current_page - 1
            prev_li = '<li><a href="{0}?{1}"><上一页></a></li>'.format(self.base_url, self.query_params.urlencode())
        html_list.append(prev_li)
        for i in range(page_start, page_end + 1):
            self.query_params['page'] = i
            if i == self.current_page:
                li_html = '<li class="active"><a href="{0}?{1}">{2}</a></li>'.format(self.base_url,
                                                                                     self.query_params.urlencode(), i)
            else:
                li_html = '<li><a href="{0}?{1}">{2}</a></li>'.format(self.base_url, self.query_params.urlencode(), i)

            html_list.append(li_html)

        if self.current_page >= self.total_page:
            next_li = '<li class="disabled"><a>< 下一页 ></a></li>'
        else:
            self.query_params['page'] = self.current_page + 1
            next_li = '<li><a href="{0}?{1}">< 下一页 ></a></li>'.format(self.base_url, self.query_params.urlencode())
        html_list.append(next_li)

        return mark_safe("".join(html_list))
