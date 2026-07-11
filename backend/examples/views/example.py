from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from examples.filters import ExampleFilter
from examples.models import Example
from examples.serializers import ExampleSerializer
from projects.models import Member, Project
from projects.permissions import IsProjectAdmin, IsProjectStaffAndReadOnly, IsProjectMember


class ExampleList(generics.ListCreateAPIView):
    serializer_class = ExampleSerializer
    #permission_classes = [IsAuthenticated & IsProjectMember]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ("created_at", "updated_at", "score")
    search_fields = ("text", "filename")
    model = Example
    filterset_class = ExampleFilter

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_queryset(self):
        member = get_object_or_404(Member, project=self.project, user=self.request.user)
        if member:
            return self.model.objects.filter(project=self.project)

        queryset = self.model.objects.filter(project=self.project, assignments__assignee=self.request.user)
        if self.project.random_order:
            queryset = queryset.order_by("assignments__id")
        return queryset

    def perform_create(self, serializer):
        serializer.save(project=self.project)

    def delete(self, request, *args, **kwargs):
        queryset = self.project.examples
        delete_ids = request.data["ids"]
        if delete_ids:
            queryset.filter(pk__in=delete_ids).delete()
        else:
            queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExampleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer
    lookup_url_kwarg = "example_id"
    permission_classes = [IsAuthenticated &  IsProjectMember]


class ExampleTextPage(APIView):
    permission_classes = [IsAuthenticated & IsProjectMember]
    default_limit = 8000
    max_limit = 50000

    @staticmethod
    def _previous_boundary(text, offset):
        if offset <= 0:
            return 0

        for index in range(min(offset, len(text)) - 1, 0, -1):
            if text[index].isspace():
                return index
        return 0

    def get(self, request, project_id, example_id):
        example = get_object_or_404(Example, pk=example_id, project_id=project_id)
        text = example.text or ""

        try:
            offset = max(int(request.query_params.get("offset", 0)), 0)
            limit = int(request.query_params.get("limit", self.default_limit))
        except ValueError:
            return Response({"detail": "offset and limit must be integers."}, status=status.HTTP_400_BAD_REQUEST)

        limit = min(max(limit, 1), self.max_limit)
        total = len(text)
        offset = min(offset, total)
        raw_page_end = min(offset + limit, total)
        page_end = raw_page_end
        if raw_page_end < total:
            boundary = self._previous_boundary(text, raw_page_end)
            if boundary > offset:
                page_end = boundary

        previous_offset = None
        if offset > 0:
            previous_offset = self._previous_boundary(text, max(offset - limit, 0))

        return Response(
            {
                "text": text[offset:page_end],
                "offset": offset,
                "limit": limit,
                "total": total,
                "next_offset": page_end if page_end < total else None,
                "previous_offset": previous_offset,
            }
        )
