from django.shortcuts import render
from django.views.decorators import csrf
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import file_organizer
 
def post_search(request):
    number_list = []
    item_list = [] 
    checklist = {}
    fileID = 1
    if request.POST:
        dealer = file_organizer.Dealer()
        userinput = str(request.POST['q']).strip('\n')
        key_list = userinput.split(',')
        for key in key_list:
            number_list = dealer.findKey(key) 
            for number in number_list:
                item = {}
                name = dealer.findName(number)
                if name != None:
                    item['number'] = number
                    item['name'] = name
                if checklist.has_key(name) is False:
                    item_list.append(item)
                    checklist[name] = number
            #print number, item_list[number]
    return render(request, "post.html", {'ItemList': item_list})
def get_file(request, num):
    data_list = []
    dealer = file_organizer.Dealer()
    data_list = dealer.loadFileInfo(num)
    print data_list
    return render(request, "post.html", {'DataList': data_list})
