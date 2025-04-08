from rest_framework import viewsets, permissions
from .models import MarkdownDocument, Tag
from .serializers import MarkdownDocumentSerializer, TagSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkdownDocumentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, request):
        queryset = MarkdownDocument.objects.filter(owner=request.user)

        tag_id = request.query_params.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        ordering = request.query_params.get('ordering')
        if ordering in ['created_at', '-created_at', 'updated_at', '-updated_at']:
            queryset = queryset.order_by(ordering)

        return queryset

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = MarkdownDocumentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MarkdownDocumentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            document = MarkdownDocument.objects.get(pk=pk, owner=request.user)
        except MarkdownDocument.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MarkdownDocumentSerializer(document)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            document = MarkdownDocument.objects.get(pk=pk, owner=request.user)
        except MarkdownDocument.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MarkdownDocumentSerializer(document, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            document = MarkdownDocument.objects.get(pk=pk, owner=request.user)
            document.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MarkdownDocument.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
