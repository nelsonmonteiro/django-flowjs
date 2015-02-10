from django import http
from django import forms
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from models import FlowFile, FlowFileChunk


class FlowFileForm(forms.Form):
    file = forms.FileField()


class UploadView(View):
    def dispatch(self, request, *args, **kwargs):
        # get flow variables
        self.flowChunkNumber = int(request.REQUEST.get('flowChunkNumber'))
        self.flowChunckSize = int(request.REQUEST.get('flowChunkSize'))
        self.flowCurrentChunkSize = int(request.REQUEST.get('flowCurrentChunkSize'))
        self.flowTotalSize = int(request.REQUEST.get('flowTotalSize'))
        self.flowIdentifier = request.REQUEST.get('flowIdentifier')
        self.flowFilename = request.REQUEST.get('flowFilename')
        self.flowRelativePath = request.REQUEST.get('flowRelativePath')
        self.flowTotalChunks = int(request.REQUEST.get('flowTotalChunks'))

        # identifier is a combination of session key and flow identifier
        self.identifier = ('%s-%s' % (request.session.session_key, self.flowIdentifier))[:200]
        return super(UploadView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Flow.js test if chunk exist before upload it again.
        Return 200 if exist.
        """
        get_object_or_404(FlowFileChunk, number=self.flowChunkNumber, parent__identifier=self.identifier)
        return http.HttpResponse(self.identifier)

    def post(self, request, *args, **kwargs):
        """
        Upload the file by chunks
        """

        # get file or create if doesn't exist the identifier
        flow_file, created = FlowFile.objects.get_or_create(identifier=self.identifier, defaults={
            'original_filename': self.flowFilename,
            'total_size': self.flowTotalSize,
            'total_chunks': self.flowTotalChunks,
        })

        # validate the file form
        form = FlowFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return http.HttpResponseBadRequest(form.errors)

        # avoiding duplicated chucks
        chunk, created = flow_file.chunks.get_or_create(number=self.flowChunkNumber, defaults={
            'file': form.cleaned_data['file'],
        })
        if not created:
            chunk.file = form.file
            chunk.size = form.size
            chunk.save()

        return http.HttpResponse(flow_file.identifier)


class CheckStateView(View):
    def get(self, request, *args, **kwargs):
        """
        Return the status of the file uploaded. This is important for big files,
        because user don't need to wait for the file to be ready.
        """
        flow = get_object_or_404(FlowFile, identifier=request.GET.get('identifier', ''))
        return http.HttpResponse(flow.state)
