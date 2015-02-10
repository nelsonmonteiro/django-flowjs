from __future__ import absolute_import
from celery import shared_task


@shared_task
def join_chunks_task(flow_file):
    print 'starting join task',
    return flow_file._join_chunks()


@shared_task
def delete_chunks_task(flow_file):
    print 'starting delete task',
    return flow_file._delete_chunks()