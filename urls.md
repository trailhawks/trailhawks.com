/	lawrencetrailhawks.views.HomepageView	homepage
/404/	django.views.generic.base.TemplateView
/500/	django.views.generic.base.TemplateView

/<prefix><tiny>	shorturls.views.redirect

/about/	lawrencetrailhawks.views.AboutView	about

/blog/	blog.views.PostArchive	blog_archive_index
/blog/<year>/<month>/<day>/<slug>/	blog.views.PostDateDetail	blog_detail

/comments/approve/<var>/	django.contrib.comments.views.moderation.approve	comments-approve
/comments/approved/	django.contrib.comments.views.utils.confirmed	comments-approve-done
/comments/cr/<var>/<var>/	django.contrib.contenttypes.views.shortcut	comments-url-redirect
/comments/delete/<var>/	django.contrib.comments.views.moderation.delete	comments-delete
/comments/deleted/	django.contrib.comments.views.utils.confirmed	comments-delete-done
/comments/flag/<var>/	django.contrib.comments.views.moderation.flag	comments-flag
/comments/flagged/	django.contrib.comments.views.utils.confirmed	comments-flag-done
/comments/post/	django.contrib.comments.views.comments.post_comment	comments-post-comment
/comments/posted/	django.contrib.comments.views.utils.confirmed	comments-comment-done

/contact/	members.views.officer_list	contact

/events/	events.views.EventListView	event_list
/events/<slug>/	events.views.EventDetailView	event_detail

/faq/	faq.views.FaqListView	faq_list
/faq/<pk>/	faq.views.FaqDetailView	faq_detail

/links/	links.views.LinkListView	link_list
/links/<pk>/	links.views.LinkDetailView	link_detail

/member_list/	members.views.member_list	member_list
/members/	members.views.MemberListView	member_list
/members/<pk>/	members.views.MemberDetailView	member_detail

/news/	news.views.NewsList	news_list
/news/<pk>/	news.views.NewsDetail	news_detail

/photos/	photos.views.PhotoListView	photo_list
/photos/<slug>/	photos.views.PhotoDetailView	photo_detail

/races/	races.views.RaceIndex	race_index
/races/<year>/	races.views.RaceYear	race_archive_year
/races/<year>/<month>/	races.views.RaceMonth	race_archive_month
/races/<year>/<month>/<day>/	races.views.RaceDay	race_archive_day
/races/<year>/<month>/<day>/<slug>/	races.views.RaceDateDetail	race_detail
/races/<year>/<month>/<day>/<slug>/results/	races.views.RaceResultDetail	race_result_detail
/races/ical/	races.feeds.RaceFeed()	race_ical
/races/racers/<pk>/	races.views.RacerDetail	racer_detail
/races/upcoming/	races.views.RaceUpcomingList	race_upcoming

/runs/	runs.views.RunListView	run_list
/runs/<slug>/	runs.views.RunDetailView	run_detail

/site_media/<path>	django.contrib.staticfiles.views.serve

/sponsors/	sponsors.views.SponsorListView	sponsor_list
/sponsors/<pk>/	sponsors.views.SponsorDetailView	sponsor_detail

/thanks/	lawrencetrailhawks.views.ThanksView	thanks
