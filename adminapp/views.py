from django.shortcuts import render,redirect
from  hotelbooking.models import Customer,Room,Hotel
# Create your views here.
#for logout
from django.contrib.auth import logout

#for file uploading
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from hotelbooking.models import Customer

curl = settings.BASE_URL
media_url=settings.MEDIA_URL

def sessioncheckadmin_middleware(get_response):
    def middleware(request):
        print("============= request=====:",request.path)
        strpath = request.path
        list1 = strpath.split("/")
        if len(list1)>2:
            strnewpath = "/"+list1[1]+"/"+list1[2]+"/"
            if strnewpath=='/hoteladmin/home/' or strnewpath=='/hoteladmin/managecustomer/' or strnewpath=='/hoteladmin/addroom/' or strnewpath == '/hoteladmin/viewroom/' or strnewpath == '/hoteladmin/addhotel/' or strnewpath == '/hoteladmin/viewhotel/' or strnewpath == '/hoteladmin/changepassword/' or strnewpath == '/changepassword/' or strnewpath == '/forgotpassword/':
                if 'emailid' not in request.session:            
                # if request.session["emailid"]==None or request.session["role"]!="admin":
                #print("EmailId:",request.session["emailid"])
                 response=redirect('http://localhost:8000/login')
                else:
                    response=get_response(request)
            else:
                response=get_response(request)
        else:
            return get_response(request)        
        return response
        
    return middleware 




def home(request):
    emailid=request.session.get("emailid")
    password=request.session.get("password") 
    listofdic=Customer.objects.filter(email=emailid,password=password).values()
    print(listofdic[0])
    
    return render(request,'AdminHome.html',{'admin':listofdic[0]})

def addroom(request):
    emailid=request.session.get("emailid")
    password=request.session.get("password") 
    listofdic=Customer.objects.filter(email=emailid,password=password).values()
    print(listofdic[0])

    if request.method == "GET": 
        hotel = Hotel.objects.all().values("hotel_name")
        return render(request,'AddRoom.html',{'admin':listofdic[0],'hotel':hotel})
    
    elif request.method == "POST":
        roomname=request.POST.get('roomname') 
        #for file uploading .............................
        room_img=request.FILES['room_img']
        #print(docname,docimg)
        fs=FileSystemStorage()
        fs.save(room_img.name,room_img)  
        #....................................................
        price=request.POST.get('price') 
        bed=request.POST.get('bed') 
        bath=request.POST.get('bath') 
        wifi=request.POST.get('wifi') 
        description=request.POST.get('description')
        print(roomname,room_img,price,bed,bath,wifi,description)
        customer = Customer.objects.get(email="admin@gmail.com",password="12345")
        hotelname=request.POST.get('hotelname')
        print("Hotel Name:",hotelname)
        hotel = Hotel.objects.get(hotel_name=hotelname)
        print(hotel)
        
        obj = Room(customer=customer,hotel=hotel,room_name=roomname,room_img=room_img,room_price=price,room_bed=bed,room_bath=bath,room_wifi=wifi,room_description=description)
        msg=""
        try:
            obj.save()
            msg="Room Added Successfully!!"
        except:
            msg="Room Not Uploaded!!"
        
    return render(request,'AddRoom.html',{'curl':curl,'msg':msg})

def viewroom(request):
    emailid=request.session.get("emailid")
    password=request.session.get("password") 
    listofdic=Customer.objects.filter(email=emailid,password=password).values()
    print(listofdic[0])
    #====get image======#
   
    qs=Room.objects.all()
    room_data = qs.values()
    print(room_data)
   
    #====get image======#
    if request.method == "GET": 
        return render(request,'ViewRoom.html',{'admin':listofdic[0],'media_url':media_url,'room_data':room_data})

def addhotel(request):
    emailid=request.session.get("emailid")
    password=request.session.get("password") 
    listofdic=Customer.objects.filter(email=emailid,password=password).values()
    print(listofdic[0])
    if request.method == "GET": 
        return render(request,'AddHotel.html',{'admin':listofdic[0]})
    
    elif request.method == "POST":
        hotelname=request.POST.get('hotelname') 
        #for file uploading .............................
        hotel_img=request.FILES['hotel_img']
        #print(docname,docimg)
        fs=FileSystemStorage()
        fs.save(hotel_img.name,hotel_img)  
        #....................................................
        city=request.POST.get('city') 
        address=request.POST.get('address') 
        price=request.POST.get('price') 
        discount=request.POST.get('discount') 
        oldprice=request.POST.get('oldprice')
        print(hotelname,hotel_img,price,city,address,discount,oldprice)
        customer = Customer.objects.get(email=emailid,password=password)
        obj = Hotel(hotel_name=hotelname,hotel_img=hotel_img,hotel_price=price,hotel_city=city,hotel_address=address,hotel_discount=discount,hotel_old_price=oldprice)
        msg=""
        try:
            obj.save()
            msg="Hotel Added Successfully!!"
        except:
            msg="Hotel Not Uploaded!!"
    return render(request,'AddHotel.html',{'curl':curl,'msg':msg})

def viewhotel(request):
    emailid=request.session.get("emailid")
    password=request.session.get("password") 
    listofdic=Customer.objects.filter(email=emailid,password=password).values()
    print(listofdic[0])
    #====get image======#
   
    qs=Hotel.objects.all()
    hotel_data = qs.values()
    print(hotel_data)
   
    #====get image======#
    if request.method == "GET": 
        return render(request,'ViewHotel.html',{'admin':listofdic[0],'media_url':media_url,'hotel_data':hotel_data})

def managecustomer(request):
    emailid=request.session.get("emailid")
    password=request.session.get("password") 
    listofdic=Customer.objects.filter(email=emailid,password=password).values()
    print(listofdic[0])
    customer = Customer.objects.filter(role="customer").values()
    print(customer)
    return render(request,'ManageCustomer.html',{'admin':listofdic[0],"customers":customer})

def managecustomerstatus(request):
    if request.method=="GET":
        id=request.GET.get('id')
        status=request.GET.get('status')
        print(id,status)
        if status == "0":
           Customer.objects.filter(customer_id=id).update(status=1)
           
        elif status == "1":
           Customer.objects.filter(customer_id=id).update(status=0)
          
        return redirect(curl+'/hoteladmin/managecustomer')    
    
def Logout(request):
    logout(request)
    return redirect('http://localhost:8000/login/')

def deletecustomer(request):
    if request.method=="GET":
        id=request.GET.get('id')
        print("Customer Id:",id)
        Customer.objects.filter(customer_id=id).delete()
        return redirect(curl+'/hoteladmin/managecustomer') 