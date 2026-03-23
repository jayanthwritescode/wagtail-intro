from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index


class OpportunityIndexPage(Page):
    intro = RichTextField(blank=True)

    subpage_types = ["opportunities.OpportunityPage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["opportunities"] = (
            OpportunityPage.objects.descendant_of(self).live().public().order_by("deadline")
        )
        return context


class OpportunityPage(Page):
    OPPORTUNITY_TYPES = [
        ("internship", "Internship"),
        ("grant", "Grant"),
        ("event", "Event"),
    ]

    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPES)
    deadline = models.DateField()
    external_url = models.URLField(blank=True)
    summary = models.TextField(max_length=320)
    body = RichTextField(blank=True)

    parent_page_types = ["opportunities.OpportunityIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("opportunity_type"),
        FieldPanel("deadline"),
        FieldPanel("external_url"),
        FieldPanel("summary"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("summary"),
        index.SearchField("body"),
        index.FilterField("opportunity_type"),
        index.FilterField("deadline"),
    ]
