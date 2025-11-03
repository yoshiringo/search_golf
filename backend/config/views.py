from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.stubs import RakutenGoraServiceStub, GoogleMapsServiceStub
from services.serializers import SearchRequestSerializer
from datetime import datetime


class GolfSearchView(APIView):
    """POST /api/golf-search/

    - バリデーションは Serializer 側で行い、`is_valid(raise_exception=True)` に任せる。
    - 外部サービスの戻り値（stub）を受け取り、出力を一貫したフォーマットに整形する。
    """

    def post(self, request):
        serializer = SearchRequestSerializer(data=request.data)
        # ここで例外を投げることで DRF が標準のエラーフォーマットで返す
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        rakuten = RakutenGoraServiceStub()
        plans = rakuten.search_plans(
            data.get('areaCode'),
            data.get('playDate').isoformat(),
            data.get('minPrice'),
            data.get('maxPrice'),
            data.get('startTimeZone')
        )

        addresses = [p.get('address') for p in plans]
        google = GoogleMapsServiceStub()
        travel_times = google.get_travel_times(data.get('originAddress', ''), addresses)

        results = []
        for p in plans:
            addr = p.get('address')
            tt = travel_times.get(addr)

            # 整形: 出力フィールドを統一する（camelCase）
            item = {
                'courseId': p.get('course_id'),
                'courseName': p.get('course_name'),
                'planName': p.get('plan_name'),
                'price': p.get('price'),
                'address': addr,
                'playDate': p.get('play_date'),
                'startTime': p.get('start_time'),
                'travelTimeMinutes': tt if tt is None or isinstance(tt, int) else int(tt)
            }

            max_travel = data.get('maxTravelTime')
            if max_travel is not None:
                try:
                    if tt is None or tt > int(max_travel):
                        continue
                except Exception:
                    # もし予期せぬ値が来ても無視して継続する
                    pass

            results.append(item)

        resp = {
            'results': results,
            'totalCount': len(results),
            'searchTime': datetime.utcnow().isoformat() + 'Z'
        }

        return Response(resp, status=status.HTTP_200_OK)