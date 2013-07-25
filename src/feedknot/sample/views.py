# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from sample.models import Sample
from sample.forms import SampleForm

def index(request):
    data_list = Sample.objects.filter(del_flg=False)

    return render_to_response('sample/index.html',
                              {'data_list':data_list},
                              context_instance=RequestContext(request))

def detail(request, sample_id):
    data = get_object_or_404(Sample, pk=sample_id, del_flg=False)

    return render_to_response('sample/detail.html',
                              {'data':data},
                              context_instance=RequestContext(request))

def create(request):

    if request.method == "POST":
        form = SampleForm(request.POST)
        return_type = request.POST.get('return')
        if form.is_valid() and not return_type:
            is_comit = True if request.POST.get('comit') else False
            if is_comit:
                sample = form.instance
                sample.add_sample(request)
                return HttpResponseRedirect(reverse('complete'))
            else:
                return render_to_response('sample/confirm.html',
                            {'proc_title':'新規作成',
                             'form':form
                            },
                            context_instance=RequestContext(request))

    else:
        form = SampleForm()

    return render_to_response('sample/edit.html',
                  {'proc_title':'新規作成',
                   'form':form
                  },
                  context_instance=RequestContext(request))

def edit(request, sample_id):

    try:
        sample = Sample.objects.get(pk=sample_id, del_flg=False)
    except Sample.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = SampleForm(request.POST, instance=sample)
        return_type = request.POST.get('return')
        if form.is_valid() and not return_type:
            is_comit = True if request.POST.get('comit') else False
            if is_comit:
                editSample = form.instance
                editSample.edit_sample(request)
                return HttpResponseRedirect(reverse('complete'))
            else:
                return render_to_response('sample/confirm.html',
                              {'proc_title':'編集',
                               'form':form
                              },
                              context_instance=RequestContext(request))
    else:
        form = SampleForm(instance=sample)

    return render_to_response('sample/edit.html',
                  {'proc_title':'編集',
                   'form':form
                  },
                  context_instance=RequestContext(request))

def delete(request, sample_id):

    try:
        sample = Sample.objects.get(pk=sample_id, del_flg=False)
    except Sample.DoesNotExist:
        raise Http404

    sample.delete_sample(request)

    return HttpResponseRedirect(reverse('members-info-list'))

def complete(request):

    return render_to_response('sample/complete.html',
                              context_instance=RequestContext(request))
