from rest_framework import serializers
from datetime import date


class SearchRequestSerializer(serializers.Serializer):
    areaCode = serializers.IntegerField(default=9, min_value=1, error_messages={
        'invalid': 'areaCode は整数で指定してください。',
        'min_value': 'areaCode は 1 以上の値を指定してください。'
    })
    playDate = serializers.DateField(input_formats=['%Y-%m-%d'], error_messages={
        'invalid': 'playDate は YYYY-MM-DD 形式の日付を指定してください。'
    })
    minPrice = serializers.IntegerField(allow_null=True, required=False, min_value=0, error_messages={'invalid': 'minPrice は整数で指定してください。'})
    maxPrice = serializers.IntegerField(allow_null=True, required=False, min_value=0, error_messages={'invalid': 'maxPrice は整数で指定してください。'})
    startTimeZone = serializers.IntegerField(allow_null=True, required=False, min_value=4, max_value=15, error_messages={'invalid': 'startTimeZone は 4-15 の整数で指定してください。'})
    originAddress = serializers.CharField(allow_blank=True, required=False)
    maxTravelTime = serializers.IntegerField(allow_null=True, required=False, min_value=0, error_messages={'invalid': 'maxTravelTime は正の整数（分）で指定してください。'})

    def validate_playDate(self, value):
        # 禁止: 過去日付（当日を許可）
        if value < date.today():
            raise serializers.ValidationError('playDate は過去日を指定できません。')
        return value

    def validate(self, attrs):
        # min/max price の整合性チェック
        min_p = attrs.get('minPrice')
        max_p = attrs.get('maxPrice')
        if min_p is not None and max_p is not None:
            if max_p < min_p:
                raise serializers.ValidationError({'maxPrice': 'maxPrice は minPrice 以上にしてください。'})

        # maxTravelTime の整合性（存在する場合は非負）
        mtt = attrs.get('maxTravelTime')
        if mtt is not None and mtt < 0:
            raise serializers.ValidationError({'maxTravelTime': 'maxTravelTime は 0 以上の整数で指定してください。'})

        return attrs