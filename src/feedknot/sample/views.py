# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from sample.models import Sample
from sample.forms import SampleForm

def index(request):
    data_list = Sample.objects.filter(del_flg=False)

    return render(request,
                        'sample/index.html',
                        {'data_list':data_list})

def detail(request, sample_id):
    data = get_object_or_404(Sample, pk=sample_id, del_flg=False)

    return render(request,
                        'sample/detail.html',
                        {'data':data})

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
                return render(request,
                                'sample/confirm.html',
                                {'proc_title':'新規作成',
                                 'form':form
                                 })

    else:
        form = SampleForm()

    return render(request,
                    'sample/edit.html',
                    {'proc_title':'新規作成',
                     'form':form
                     })

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
                return render(request,
                                'sample/confirm.html',
                                {'proc_title':'編集',
                                 'form':form
                                })
    else:
        form = SampleForm(instance=sample)

    return render(request,
                  'sample/edit.html',
                  {'proc_title':'編集',
                   'form':form
                  })

def delete(request, sample_id):

    try:
        sample = Sample.objects.get(pk=sample_id, del_flg=False)
    except Sample.DoesNotExist:
        raise Http404

    sample.delete_sample(request)

    return HttpResponseRedirect(reverse('members-info-list'))

def complete(request):

    return render(request,
                  'sample/complete.html')
