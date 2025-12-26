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
    # startTimeZone: 単一の整数またはカンマ区切りの複数値（例: "5,7,9"）を受け付ける
    # フロントエンドは複数選択時に "5,7,9" のような文字列を送信します
    startTimeZone = serializers.CharField(allow_blank=True, allow_null=True, required=False)
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

        # startTimeZone の追加検証: 空でなければ整数リストまたは単一整数として妥当性を確認
        stz = attrs.get('startTimeZone')
        if stz is not None and stz != '':
            # 既に整数が来るケースにも対応するため、str にして処理
            stz_str = str(stz)
            parts = [p.strip() for p in stz_str.split(',') if p.strip() != '']
            parsed = []
            for p in parts:
                try:
                    v = int(p)
                except Exception:
                    raise serializers.ValidationError({'startTimeZone': 'startTimeZone は整数またはカンマ区切りの整数列表現で指定してください。'})
                if v < 4 or v > 15:
                    raise serializers.ValidationError({'startTimeZone': 'startTimeZone の各値は 4-15 の範囲で指定してください。'})
                parsed.append(v)
            # バリデータは値をそのまま文字列で保持しておき、ビュー/クライアントでそのまま外部APIに渡す
            # ただし、内部で数値として参照したい場合は parsed を利用できるように補助キーを追加しておく
            attrs['_startTimeZone_list'] = parsed

        return attrs