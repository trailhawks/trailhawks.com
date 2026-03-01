from functools import reduce
from operator import or_

import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic import TemplateView
from neapolitan.views import CRUDView, Role

from races.models import Race
from runs.models import Run


class StaffDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Staff dashboard with nav cards linking to CRUD sections."""

    template_name = "neapolitan/staff_dashboard.html"

    def test_func(self):
        return self.request.user.is_staff


class StaffCRUDView(LoginRequiredMixin, UserPassesTestMixin, CRUDView):
    """Base CRUD view requiring staff access, with namespace-aware URLs."""

    search_fields = []
    filterset_fields = []

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        if self.role == Role.DELETE:
            return reverse(f"staff:{self.url_base}-list")
        url_kwarg = self.lookup_url_kwarg or self.lookup_field
        return reverse(
            f"staff:{self.url_base}-detail",
            kwargs={url_kwarg: getattr(self.object, self.lookup_field)},
        )

    def _reverse_role(self, role, obj=None):
        url_kwarg = self.lookup_url_kwarg or self.lookup_field
        url_name = f"staff:{self.url_base}-{role.url_name_component}"
        if role in (Role.LIST, Role.CREATE):
            return reverse(url_name)
        return reverse(url_name, kwargs={url_kwarg: getattr(obj, self.lookup_field)})

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q and self.search_fields:
            queries = [Q(**{f"{field}__icontains": q}) for field in self.search_fields]
            qs = qs.filter(reduce(or_, queries))
        return qs

    def get_extra_row_urls(self, obj):
        """Return extra URLs to include in each list row. Override in subclasses."""
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_view_url"] = self._reverse_role(Role.CREATE)
        context["list_view_url"] = self._reverse_role(Role.LIST)
        if hasattr(self, "object") and self.object is not None:
            context["detail_view_url"] = self._reverse_role(Role.DETAIL, self.object)
            context["update_view_url"] = self._reverse_role(Role.UPDATE, self.object)
            context["delete_view_url"] = self._reverse_role(Role.DELETE, self.object)
        return context

    def list(self, request, *args, **kwargs):
        """Override to inject namespaced per-object URLs, search, filters, and htmx support."""
        response = super().list(request, *args, **kwargs)

        object_list = response.context_data.get("object_list", [])
        fields = self.fields or []

        headers = []
        for f in fields:
            try:
                headers.append(self.model._meta.get_field(f).verbose_name)
            except Exception:
                headers.append(f)

        rows = []
        for obj in object_list:
            field_values = []
            for f in fields:
                display_method = getattr(obj, f"get_{f}_display", None)
                if display_method and callable(display_method):
                    field_values.append(display_method())
                else:
                    field_values.append(getattr(obj, f, ""))
            row = {
                "object": obj,
                "fields": field_values,
                "detail_url": self._reverse_role(Role.DETAIL, obj),
                "edit_url": self._reverse_role(Role.UPDATE, obj),
                "delete_url": self._reverse_role(Role.DELETE, obj),
            }
            row.update(self.get_extra_row_urls(obj))
            rows.append(row)

        response.context_data["list_headers"] = headers
        response.context_data["object_rows"] = rows
        response.context_data["search_query"] = request.GET.get("q", "")

        model_name = self.model._meta.model_name
        if request.headers.get("HX-Request"):
            response.template_name = f"neapolitan/{model_name}_list_partial.html"
        else:
            response.template_name = f"neapolitan/{model_name}_list.html"

        return response

    def detail(self, request, *args, **kwargs):
        """Override to inject namespaced URLs and field data into context."""
        response = super().detail(request, *args, **kwargs)
        obj = response.context_data["object"]
        fields = self.fields or []
        detail_fields = []
        for f in fields:
            try:
                verbose = self.model._meta.get_field(f).verbose_name
            except Exception:
                verbose = f
            detail_fields.append(
                {
                    "label": verbose,
                    "value": getattr(obj, f, ""),
                }
            )
        response.context_data["detail_fields"] = detail_fields
        response.context_data["update_view_url"] = self._reverse_role(Role.UPDATE, obj)
        response.context_data["delete_view_url"] = self._reverse_role(Role.DELETE, obj)
        response.context_data["list_view_url"] = self._reverse_role(Role.LIST)
        return response


class RaceFilterSet(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(
        field_name="start_datetime",
        lookup_expr="year",
        label="Year",
        empty_label="All Years",
    )

    class Meta:
        model = Race
        fields = ["active", "year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = Race.objects.exclude(start_datetime__isnull=True).dates("start_datetime", "year", order="DESC")
        self.filters["year"].extra["choices"] = [(y.year, y.year) for y in years]
        # Style all widgets
        select_classes = (
            "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
        )
        for f in self.filters.values():
            f.field.widget.attrs.setdefault("class", select_classes)


class RaceCRUDView(StaffCRUDView):
    model = Race
    filterset_class = RaceFilterSet
    search_fields = ["title", "slug", "distance"]

    def get_extra_row_urls(self, obj):
        return {
            "agent_url": reverse("race_agent_pk", kwargs={"pk": obj.pk}),
            "chat_url": reverse("race_chat", kwargs={"pk": obj.pk}),
        }

    _form_fields = [
        "title",
        "slug",
        "active",
        "number",
        "annual",
        "slogan",
        "race_type",
        "distance",
        "unit",
        "start_datetime",
        "location",
        "description",
        "course_map",
        "cut_off",
        "reg_url",
        "reg_description",
    ]

    @property
    def fields(self):
        match self.role:
            case Role.LIST:
                return ["title", "start_datetime", "active"]
            case Role.DETAIL:
                return [
                    "title",
                    "slug",
                    "active",
                    "number",
                    "annual",
                    "slogan",
                    "race_type",
                    "distance",
                    "unit",
                    "start_datetime",
                    "location",
                    "description",
                    "course_map",
                    "cut_off",
                    "reg_url",
                    "awards",
                ]
            case _:
                return self._form_fields


class RunFilterSet(django_filters.FilterSet):
    class Meta:
        model = Run
        fields = ["active", "day_of_week"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        select_classes = (
            "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
        )
        for f in self.filters.values():
            f.field.widget.attrs.setdefault("class", select_classes)


class RunCRUDView(StaffCRUDView):
    model = Run
    filterset_class = RunFilterSet
    search_fields = ["name"]
    _form_fields = [
        "name",
        "slug",
        "day_of_week",
        "run_time",
        "location",
        "details",
        "active",
    ]

    @property
    def fields(self):
        match self.role:
            case Role.LIST:
                return ["name", "day_of_week", "run_time", "active"]
            case Role.DETAIL:
                return [
                    "name",
                    "slug",
                    "day_of_week",
                    "run_time",
                    "location",
                    "details",
                    "active",
                ]
            case _:
                return self._form_fields
