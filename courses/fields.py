from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# 커스텀 OrderField
# 이 필드는 Django 에서 제공하는 PositiveIntegerField를 상속한다.
# 이 필드는 for_fields 매개변수를 선택적으로 받아서 데이터를 정렬하는데 사용하는 필드를 지정할 수 있다.
class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None,*args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
        
    # PositiveIntegerField 필드의 pre_save() 메서드를 재정의
    # 이 메서드는 필드를 데이터베이스에 저장하기 전에 실행된다.
    def pre_save(self,model_instance, add):
        # 모델 인스턴스에서 이 필드에 대한 값이 이미 있는지 확인
        # self.attname을 사용하여 모델에서 필드에 지정된 속성 이름을 가져온다.
        # 속성의 값이 None일 경우 실행
        if getattr(model_instance, self.attname) is None:
            # 현재 값이 없음
            try:
                # 필드가 속한 모델 클래스는 self.model을 사용하여 가져오고
                # 필드의 모델에 속한 모든 객체를 가져온다.
                qs = self.model.objects.all()
                # 필드의 for_fields 속성에 필드 이름이 있다면 실행
                if self.for_fields:
                    # 'for_fields'에 지정된 필드 값이 동일한 객체로 필터링
                    # QuerySet을 현재 모델 필드의 현재 값을 기준으로 필터링하며 주어진 필드에 따라 순서를 계산
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # 마지막 항목의 순서 가져오기
                # 데이터 베이스에서 가장 높은 순서를 가진 객체를 last_item = qs.latest(self.attname)로 가져온다
                last_item = qs.latest(self.attname)
                # 객체가 발견 되면 최고 순서에 1을 더한다.
                value = last_item.order + 1
            # 객체가 없는 경우 이 객체가 첫번째 객체라고 가정하고 순서를 0으로 할당
            except ObjectDoesNotExist:
                value = 0
            # 계산된 순서를 모델 인스턴스의 필드 값으로 할당하고 반환
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance,add)