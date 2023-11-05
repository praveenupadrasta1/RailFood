from rest_framework import serializers
from models import TrainLiveStatus

from BAAS.config import INVALID_TRAIN_NUMBER


class TrainLiveStatusSerializer(serializers.ModelSerializer):
    train_no = serializers.IntegerField()

    class Meta:
        model = TrainLiveStatus

        fields = ['train_no']

    def validate_train_no(self, train_no):
        if str(train_no).isdigit():
            return train_no
        else:
            raise serializers.ValidationError(INVALID_TRAIN_NUMBER)