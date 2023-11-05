from rest_framework import serializers

from models import TicketDetails
from BAAS.config import INVALID_PNR_NUMBER


class AddJourneySerializer(serializers.ModelSerializer):
    pnr_no = serializers.CharField(min_length=10, max_length=10)

    class Meta:
        model = TicketDetails

        fields = ['pnr_no']

    def validate_pnr_no(self, pnr_no):
        if str(pnr_no).isdigit():
            return pnr_no
        else:
            raise serializers.ValidationError(INVALID_PNR_NUMBER)


class GetJourneySerializer(serializers.ModelSerializer):
    pnr_no = serializers.CharField(min_length=10, max_length=10)

    class Meta:
        model = TicketDetails

        fields = ['pnr_no']

    def validate_pnr_no(self, pnr_no):
        if str(pnr_no).isdigit():
            return pnr_no
        else:
            raise serializers.ValidationError(INVALID_PNR_NUMBER)