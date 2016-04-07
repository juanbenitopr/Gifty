from rest_framework import status

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from gifts.models import Gift, GiftsMember, List


class APICreateRelation(ViewSet):
    def create(self,request):
        pk_gift = request.datas.pk_gift
        pk_list = request.datas.pk_list

        gift_member = Gift.objects.filter(pk=pk_gift)
        list_member = List.objects.filter(pk = pk_list)
        new_gift_member = GiftsMember.create(gift=gift_member,list=list)
        return Response(status=status.HTTP_201_CREATED)