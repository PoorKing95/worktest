import json
import re

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .forms import AuthorForm, PaperStep1Form, AuthorForm2
from .models import Author, Company
from .models import AuthorCompany
from .models import Paper, PaperAuthor
from . import util
from .data import provinces
from .country_map import all_map as country_map


# Create your views here.


def add_step1(request):
    if request.method == 'POST':
        form = PaperStep1Form(request.POST)
        if form.is_valid():
            values = form.cleaned_data
            request.session['paper'] = values
            flag = True

            if values['pifpub'] == 'true':
                try:
                    if re.match(r'^\s+$', values['pplace']):
                        flag = False
                    if re.match(r'^\s+$', values['ppub']):
                        flag = False
                    if re.match(r'^\s+$', str(values['pyear'])):
                        flag = False
                    if re.match(r'^\s+$', str(values['ppage'])):
                        flag = False
                    if re.match(r'^\s+$', values['ppath']):
                        flag = False
                except:
                    flag = False

            if flag:
                return HttpResponseRedirect(reverse('polls:add_step2'))
    else:
        paper = request.session.get('paper', {})
        form = PaperStep1Form(initial={
            'pname': paper.get('pname', ''),
            'ptype': paper.get('ptype', ''),
            'pplace': paper.get('pplace', ''),
            'ppub': paper.get('ppub', ''),
            'pyear': paper.get('pyear', ''),
            'ppage': paper.get('ppage', ''),
            'ppath': paper.get('ppath', ''),
        })
    return render(request, 'polls/add-step1.html', {'form': form})


def add_step2(request):
    if request.session.get('paper', None) is None:
        raise Http404()

    authors = request.session.get('authors', [])

    return render(request, 'polls/add-step2.html', {'authors': json.dumps(authors)})


def add_step3(request):
    s = {"计算机程序[CP]", "电子公告[EB]", "数据库[DB]"}
    request.session['paper']['showPath'] = request.session['paper']['ptype'] in s
    return render(request, 'polls/add-step3.html', {
        'paper': request.session['paper'],
        'authors': request.session['authors']
    })


def save_paper(request, conti=False):
    _paper = request.session['paper']
    _paper['pifpub'] = (_paper['pifpub'] == 'true')
    authors = request.session['authors']
    if _paper['pyear'] is None:
        _paper['pyear'] = 0
    if _paper['ppage'] is None:
        _paper['ppage'] = 0
    paper = Paper(**_paper)
    paper.save()

    for i, a in enumerate(authors):
        author = Author.objects.get(amail=a['amail'])
        company = Company.objects.filter(cnamech1=a['cnamech1'], cnamech2=a['cnamech2'])[0]
        pa = PaperAuthor(
            author=author,
            company=company,
            paper=paper,
            paorder=i+1,
            pacommunication=a.get('isComm', False),
            pacorder=a.get('commOrder', 0)
        )
        pa.save()
    del request.session['paper']
    del request.session['authors']
    if not conti:
        return HttpResponseRedirect(reverse('login:tables'))
    else:
        return HttpResponseRedirect(reverse('polls:add_step1'))


def get_author(request):
    if request.method != 'GET':
        raise Http404()
    name = request.GET.get('name', '')
    if re.match(r'^\s*$', name):
        return JsonResponse({
            'success': False,
            'message': '名字不能为空',
        })
    try:
        author = Author.objects.get(anamech=name)
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '不存在该作者，请添加'
        })

    try:
        ac = AuthorCompany.objects.get(author=author)
        return JsonResponse({
            'success': True,
            'val': {
                'anamech': author.anamech,
                'anameen': author.anameen,
                'amail': author.amail,
                'cnamech1': ac.company.cnamech1,
                'cnamech2': ac.company.cnamech2,
            }
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': True,
            'val': {
                'anamech': author.anamech,
                'anameen': author.anameen,
                'amail': author.amail,
            }
        })


def author_list(request):
    if request.method != 'GET':
        raise Http404()
    prefix = request.GET.get('prefix', '')
    if prefix == '':
        raise Http404()
    authors = Author.objects.filter(Q(anamech__startswith=prefix) | Q(anameen__startswith=prefix))[:10]
    result = []
    for author in authors:
        try:
            ac = AuthorCompany.objects.get(author_id=author.aid)
            result.append({
                'anamech': author.anamech,
                'anameen': author.anameen,
                'amail': author.amail,
                'cnamech1': ac.company.cnamech1,
                'cnamech2': ac.company.cnamech2,
                'cnameeg1': ac.company.cnameeg1,
                'cnameeg2': ac.company.cnameeg2
            })
        except:
            result.append({
                'anamech': author.anamech,
                'anameen': author.anameen,
                'amail': author.amail,
            })
    return HttpResponse(json.dumps(list(result)), content_type="application/json")


@csrf_exempt
def add_authors(request):
    authors = json.loads(request.body.decode('utf-8'))
    if len(authors) == 0:
        return HttpResponse(json.dumps({'success': False, 'message': '至少添加一位作者'}), content_type="application/json")
    tmp = {}
    for a in authors:
        tmp[a['amail']] = a
    if len(tmp) != len(authors):
        return HttpResponse(json.dumps({'success': False, 'message': '添加了重复的作者'}), content_type="application/json")
    if not util.check_comm(authors):
        return HttpResponse(json.dumps({'success': False, 'message': '通信作者顺序有误'}), content_type="application/json")
    request.session['authors'] = authors
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def new_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            values = form.cleaned_data
            try:
                author = Author(
                    anamech=values['anamech'],
                    anameen=values['anameen'],
                    amail=values['amail'],
                )
                author.save()
            except:
                return render(request, 'polls/new-author.html', {
                    'form': form, 'err_msg': '%s已被其他作者占用' % values['amail']})

            try:
                company = Company.objects.get(
                    cnamech1=values['cnamech1'], cnamech2=values['cnamech2']
                )
            except Company.DoesNotExist:
                company = Company(
                    cnamech1=values['cnamech1'],
                    cnameeg1=values['cnameeg1'],
                    cnamech2=values['cnamech2'],
                    cnameeg2=values['cnameeg2'],
                    czipcode=values['czipcode'],
                    addressch=values['addressch'],
                    addressen=values['addressen'],
                )
                company.save()
            ac = AuthorCompany(
                author=author,
                company=company,
                acorder=1,
                accurrent=True,
            )
            ac.save()
            return HttpResponseRedirect(reverse('polls:add_step2'))
    else:
        form = AuthorForm()

    return render(request, 'polls/new-author.html', {'form': form})


def new_author_2(request):
    if request.method == 'POST':
        form = AuthorForm2(request.POST)
        if form.is_valid():
            values = form.cleaned_data
            try:
                author = Author(
                    anamech=values['alnamech'] + values['afnamech'],
                    anameen=values['afnameen'] + ' ' + values['alnameen'],
                    alnamech=values['alnamech'],
                    afnamech=values['afnamech'],
                    alnameen=values['alnameen'],
                    afnameen=values['afnameen'],
                    amail=values['amail'],
                )
                author.save()
            except:
                return render(request, 'polls/new-author.html', {
                    'data': values, 'err_msg': '%s已被其他作者占用' % values['amail']})

            if values['country'] == '中国':
                province_no = values['province']
                city_no = values['city']
                area_no = values['area']

                if province_no < 0 or province_no >= len(provinces):
                    err_msg = '不合法的省份'
                    return render(request, 'polls/new-author.html', {
                        'data': values, 'err_msg': err_msg})
                province = provinces[province_no]

                if city_no < 0 or city_no >= len(province['city']):
                    err_msg = '不合法的市'
                    return render(request, 'polls/new-author.html', {
                        'data': values, 'err_msg': err_msg})
                city = province['city'][city_no]

                if area_no < 0 or area_no >= len(city['area']):
                    err_msg = '不合法的区县'
                    return render(request, 'polls/new-author.html', {
                        'data': values, 'err_msg': err_msg})
                area = city['area'][area_no]

                addressch = province['name'] + city['name'] + area + values['addressch']
                try:
                    company = Company.objects.get(
                        cnamech1=values['cnamech1'],
                        cnameeg1=values['cnameen1'],
                        cnamech2=values['cnamech2'],
                        cnameeg2=values['cnameen2'],
                        czipcode=values['czipcode'],
                        addressch=addressch,
                    )
                except Company.DoesNotExist:
                    company = Company(
                        cnamech1=values['cnamech1'],
                        cnameeg1=values['cnameen1'],
                        cnamech2=values['cnamech2'],
                        cnameeg2=values['cnameen2'],
                        czipcode=values['czipcode'],
                        addressch=addressch,
                    )
                    company.save()
            else:
                addressen = country_map[values['country']] + ' ' + values['addressen']
                try:
                    company = Company.objects.get(
                        cnamech1=values['cnamech1'],
                        cnameeg1=values['cnameen1'],
                        cnamech2=values['cnamech2'],
                        cnameeg2=values['cnameen2'],
                        czipcode=values['czipcode'],
                        addressen=addressen,
                    )
                except Company.DoesNotExist:
                    company = Company(
                        cnamech1=values['cnamech1'],
                        cnameeg1=values['cnameen1'],
                        cnamech2=values['cnamech2'],
                        cnameeg2=values['cnameen2'],
                        czipcode=values['czipcode'],
                        addressen=addressen,
                    )
                    company.save()
            ac = AuthorCompany(
                author=author,
                company=company,
                acorder=1,
                accurrent=True,
            )
            ac.save()

            return HttpResponseRedirect(reverse('polls:add_step2'))
        else:
            return render(request, 'polls/new-author.html', {'data': request.POST, 'err_msg': '信息不完善'})
    return render(request, 'polls/basic-form.html')
