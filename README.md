django-flowjs
=============

This is an app for your Django project to enable large uploads using flow.js to
chunk the files client side and send chunks that are re-assembled on server side.

NOTE: I have done this just to help me on a project and I haven't been updating the code.
Feel free to take control of the project. This was working with ng-flow-standalone 2.5.1.
Celery isn't required but it is recommended.


Settings
========
*FLOWJS_PATH*: Media path where the files are saved. *Default: 'flowjs/'*

*FLOWJS_REMOVE_FILES_ON_DELETE*: Remove the upload files when the model is deleted. *Default: True*

*FLOWJS_AUTO_DELETE_CHUNKS*: Remove temporary chunks after file have been upload and created. *Default: True*

*FLOWJS_EXPIRATION_DAYS*: Time in days to remove non completed uploads. *Default: 1*

*FLOWJS_JOIN_CHUNKS_IN_BACKGROUND*: When flowjs should join files in background. Options: 'none', 'media' (audio and video), 'all' (all files). *Default: 'none'*


HTML
====
```
<span flow-init="initFlow()" flow-btn
      flow-file-progress="uploadProgress($flow, $file)"
      flow-files-submitted="openUploadProgressModal($flow)"
      flow-file-success="fileUploadedSuccessfully($flow, $message)">
</span>
```

Javascript
==========

The script is only working for 1 file and 1 simultaneousUpload.
```
function initFlow() {
    return {
        target: '/flowjs/upload/',
        singleFile: true,
        query: {'csrfmiddlewaretoken': $cookies.csrftoken},
        simultaneousUploads: 1
    }
}
```

This is an example of how to update a variable while the file is uploading
```
function uploadProgress($flow, $file) {
    $flow.item.progress = parseInt($file._prevUploadedSize / $file.size * 100);
    $flow.item.speed = $file.currentSpeed;
}

```

Open a modal or something to show the progress bar
```
function openUploadProgressModal($flow) {
    // Write something here
}
```

Function to handle the download
```
function fileUploadedSuccessfully($flow, $message) {
    $http.post("/some-url-to-handle-file/", {identifier: $message})
        .success(function () {});
}
```

Views
=====
```
def view_to_handle_download(request):
    # get and validate flow file to use as media file
    identifier = request.POST.get('identifier', '')
    try:
        flow_file = FlowFile.objects.get(identifier=identifier)
        if not flow_file.is_valid_session(request.session.session_key):
            return http.HttpResponseForbidden()
    except FlowFile.DoesNotExist:
        raise http.Http404()

    # Do something now with the flow_file.
    # If the file is being joined in background, there's no guarantee
    # the flow_file.file is ready at this moment. A signal is fired when is ready.
```


Signals
=======
There are 3 signals being fired: *file_is_ready*, *file_upload_failed* and *file_joining_failed*.
