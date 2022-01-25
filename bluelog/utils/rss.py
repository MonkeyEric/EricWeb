# coding:utf-8
import datetime
import dateutil
from feedgen.feed import FeedGenerator


def build_rss_atom(blog_10_items):
    fg = FeedGenerator()
    # 给atom用的，如果有一个长期使用的域名的话就填域名就好了
    fg.id('https://www.choumaomi.com')
    # 对应的也就是rss xml里channel中的title
    fg.title("Smelly Cat's Blog")
    fg.author({'name': 'Tuesday'})
    fg.link(href='https://www.chenlongyu.com/atom.xml', rel='self')
    fg.link(href='https://www.chenlongyu.com', rel='alternate')
    fg.logo('https://www.chenlongyu.com/static/ico.jpg')
    fg.subtitle('喜欢写代码，喜欢研究一切好玩的，喜欢记录，喜欢分享。')
    fg.language('zh-CN')

    blog_10_items.reverse()
    for item in blog_10_items:
        fe = fg.add_entry()

        fe.title('title')
        fe.description('body')
        fe.category({"term": 'category'})

        fe.id(url)
        fe.link(url)

        time_temp: datetime.datetime = item[3]['time']
        local_dt = time_temp.replace(tzinfo=dateutil.tz.tzutc())
        fe.pubDate(local_dt)


    # fg.atom_file('atom.xml')  # Write the ATOM feed to a file
    # fg.rss_file('rss.xml')  # Write the RSS feed to a file
    atom_feed = fg.atom_str(pretty=True,xml_declaration=False)
    atom_feed_str = str(atom_feed, encoding="utf-8")
    file_name = r"./path/atom.xml"
    with open(file_name, 'w') as f_object:
        f_object.write(atom_feed_str)
        f_object.close()

    rss_feed = fg.rss_str(pretty=True)
    rss_feed_str = str(rss_feed, encoding="utf-8")
    file_name = r"./path/rss.xml"
    with open(file_name, 'w') as f_object:
        f_object.write(rss_feed_str)
        f_object.close()