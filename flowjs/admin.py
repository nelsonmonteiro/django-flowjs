from django.contrib import admin
from models import FlowFile, FlowFileChunk


class FlowFileChunkInline(admin.TabularInline):
    model = FlowFileChunk


class FlowFileAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'state', 'total_size', 'total_chunks', 'total_chunks_uploaded']
    list_filter = ['state']
    inlines = [FlowFileChunkInline]
admin.site.register(FlowFile, FlowFileAdmin)
