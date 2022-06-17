from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from app_api.models import PaymentType


class PaymentTypeView(ViewSet):
    def list(self, request):
        """Get a list of payment types for the current user"""
        payment_types = PaymentType.objects.filter(customer=request.auth.user)
        serializer = PaymentTypeSerializer(payment_types, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create a payment type for the current user"""
        try:
            payment_type = PaymentType.objects.create(
                customer=request.auth.user,
                card_type=request.data['cardType'],
                card_number=request.data['cardNumber']
            )
            serializer = PaymentTypeSerializer(payment_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Delete a payment type"""
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            payment_type.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ('id','card_type','obscured_num','customer')

class CreatePaymentType(serializers.Serializer):
    cardType = serializers.CharField()
    cardNumber = serializers.CharField()
