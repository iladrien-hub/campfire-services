from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.api.v0.serializers import UserRegistrationSerializer, PersonalInfoSerializer, ChangePasswordSerializer, \
    ChangeUsernameSerializer
from account.auth import AppAuthentication
from account.models import ProfileImage


@api_view(('GET',))
def account_view(request):
    account, _ = AppAuthentication().authenticate(request)
    images = ProfileImage.objects.all()

    try:
        item = ProfileImage.objects.get(pk=account.photo)
        photo = {
            "medium": str(item.image_medium),
            "big": str(item.image_big),
            "id": item.pk
        }
    except:
        photo = None

    return Response(data={
        "success": True,
        "errors": {},
        "data": {
            "username": account.username,
            "name": account.name,
            "surname": account.surname,
            "phone": account.phone,
            "photo": photo,
            "gallery": sorted([{
                "medium": str(image.image_medium),
                "big": str(image.image_big),
                "id": image.pk
            } for image in images if image.owner == account], key=lambda x: -x['id'])
        },
        "status": ""
    }, status=status.HTTP_200_OK)


@api_view(('POST',))
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            return Response(data={
                "success": True,
                "errors": {},
                "data": {
                    "token": Token.objects.get(user=account).key
                },
                "status": "User Created Successfully"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                "success": False,
                "errors": serializer.errors,
                "status": "Failed To Create a New User"
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={
        "success": False,
        "errors": {},
        "status": "Method Not Allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(('POST',))
def authentication_view(request):
    account, _ = AppAuthentication().authenticate(request)
    return Response(data={"id": account.pk, "username": account.username}, status=status.HTTP_200_OK)


@api_view(('POST',))
def set_personal_view(request):
    if request.method == 'POST':
        account, _ = AppAuthentication().authenticate(request)
        serializer = PersonalInfoSerializer(data=request.data)
        if serializer.is_valid():
            # Updating data
            account.name = serializer.validated_data['name']
            account.surname = serializer.validated_data['surname']
            account.phone = serializer.validated_data['phone']
            account.save()
            # Returning response
            return Response(data={
                "success": True,
                "errors": {},
                "data": {},
                "status": "Personal Data Successfully Updated"
            }, status=status.HTTP_200_OK)
        else:
            return Response(data={
                "success": False,
                "errors": serializer.errors,
                "status": "Failed To Update Personal Data"
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={
        "success": False,
        "errors": {},
        "status": "Method Not Allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(('POST',))
def set_password_view(request):
    if request.method == 'POST':
        account, _ = AppAuthentication().authenticate(request)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Updating data
            account.set_password(serializer.validated_data['password'])
            account.save()
            # Returning response
            return Response(data={
                "success": True,
                "errors": {},
                "data": {},
                "status": "Password Successfully Changed"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                "success": False,
                "errors": serializer.errors,
                "status": "Failed To Change Password"
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={
        "success": False,
        "errors": {},
        "status": "Method Not Allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(('POST',))
def set_username_view(request):
    if request.method == 'POST':
        account, _ = AppAuthentication().authenticate(request)
        serializer = ChangeUsernameSerializer(data=request.data)

        if serializer.is_valid():
            # Updating data
            account.username = serializer.validated_data['username']
            account.save()
            # Returning response
            return Response(data={
                "success": True,
                "errors": {},
                "data": {},
                "status": "Username Successfully Changed"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                "success": False,
                "errors": serializer.errors,
                "status": "Failed To Change Username"
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={
        "success": False,
        "errors": {},
        "status": "Method Not Allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(('POST',))
def add_photo_view(request):

    if request.method == 'POST':
        try:
            # Saving data
            account, _ = AppAuthentication().authenticate(request)
            photo = ProfileImage()
            photo.set_image(request.data['image'])
            photo.owner = account
            photo.save()
            account.photo = photo.pk
            account.save()
            # Returning response
            return Response(data={
                "success": True,
                "errors": {},
                "data": {
                    "medium": str(photo.image_medium),
                    "big": str(photo.image_big),
                    "id": photo.pk
                },
                "status": "Photo Successfully Saved"
            }, status=status.HTTP_201_CREATED)

        except KeyError:
            return Response(data={
                "success": False,
                "errors": [{"image": ["This is required field"]}],
                "status": "Unable To Save Photo"
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={
        "success": False,
        "errors": {},
        "status": "Method Not Allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(('DELETE',))
def remove_photo_view(request):
    if request.method == 'DELETE':
        account, _ = AppAuthentication().authenticate(request)
        try:
            # Saving data
            pk = request.data['id']
            try:
                photo = ProfileImage.objects.get(pk=pk)
            except ProfileImage.DoesNotExist:
                return Response(data={
                    "success": False,
                    "errors": {},
                    "data": {},
                    "status": "Not Found"
                }, status=status.HTTP_404_NOT_FOUND)

            if account.is_admin or account == photo.owner:
                print(str(photo.owner.photo), pk, str(photo.owner.photo) == pk)
                reset_image = str(photo.owner.photo) == pk

                photo.image_medium.delete(save=True)
                photo.image_big.delete(save=True)
                photo.delete()

                data = {
                    "changed": reset_image
                }
                if reset_image:
                    try:
                        new_photo = ProfileImage.objects.filter(owner=photo.owner).order_by('-pk')[0]
                        photo.owner.photo = new_photo.pk
                        data["new"] = {
                            "medium": str(new_photo.image_medium),
                            "big": str(new_photo.image_big),
                            "id": new_photo.pk
                        }
                    except IndexError:
                        data["new"] = None
                        photo.owner.photo = None
                    photo.owner.save()

                # Returning response
                return Response(data={
                    "success": True,
                    "errors": {},
                    "data": data,
                    "status": "Removed"
                }, status=status.HTTP_200_OK)
            else:
                return Response(data={
                    "success": False,
                    "errors": {},
                    "data": {},
                    "status": "Forbidden"
                }, status=status.HTTP_403_FORBIDDEN)

        except KeyError:
            return Response(data={
                "success": False,
                "errors": [{"id": ["This is required field"]}],
                "status": "Unable To Save Photo"
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={
        "success": False,
        "errors": {},
        "status": "Method Not Allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
