import datetime
from enum import IntEnum
from typing import Optional, List, Union

from pydantic import BaseModel, Field, UUID5, validator, ValidationError


class CdekThreshold(BaseModel):
    threshold: int = 0
    sum: float = 0
    vat_sum: Optional[float] = None
    vat_rate: Optional[int] = None


class CdekMoney(BaseModel):
    """
    стоимость услуги/товара с учетом налогообложения
    """

    value: float = 0  # Сумма дополнительного сбора
    vat_sum: Optional[float] = None  # Сумма НДС
    vat_rate: Optional[
        int
    ] = None  # Ставка НДС (значение - 0, 10, 18, 20 и т.п. , null - нет НДС)


class CdekPhones(BaseModel):
    """
    номер телефона (мобильный/городской)
    """

    number: str = Field(
        "",
        max_length=255,
        description="Номер телефона. Необходимо передавать в международном формате: "
        "код страны (для России +7) и сам номер (10 и более цифр)",
    )

    additional: str | None = Field(
        None, max_length=255, description="Дополнительная информация (добавочный номер)"
    )


class CdekContact(BaseModel):
    """
    данные контрагента (отправителя, получателя)
    """

    company: str | None = Field(
        None, max_length=255, description="Наименование компании"
    )
    name: str = Field("", max_length=255, description="Ф.И.О контактного лица")
    email: str | None = Field(None, max_length=255, description="Эл. адрес")
    phones: list[CdekPhones] = Field(
        default_factory=list, description="Список телефонов"
    )

    passport_series: str | None = Field(
        None, max_length=255, description="Серия паспорта"
    )
    passport_number: str | None = Field(
        None, max_length=255, description="Номер паспорта"
    )
    passport_date_of_issue: Optional[datetime.date] = None  # Дата выдачи паспорта
    passport_organization: str | None = Field(
        None, max_length=255, description="Орган выдачи паспорта"
    )
    passport_date_of_birth: Optional[datetime.date] = None  # Дата рождения

    # Требования по паспортным данным удовлетворены (актуально для международных заказов):
    # true - паспортные данные собраны или не требуются
    # false - паспортные данные требуются и не собраны
    passport_requirements_satisfied: bool = False

    tin: str | None = Field(None, max_length=255, description="ИНН")


class CdekSeller(BaseModel):
    """
    данные истинного продавца
    """

    name: str = Field(
        None, max_length=255, description="Наименование истинного продавца"
    )
    inn: str = Field(None, max_length=255, description="ИНН истинного продавца")
    phone: str = Field(None, max_length=255, description="Телефон истинного продавца")
    ownership_form: Optional[int] = None  # Код формы собственности

    # Адрес истинного продавца.
    # Используется при печати инвойсов для отображения адреса настоящего продавца товара, либо торгового названия
    address: str = Field(None, max_length=255, description="")


class CdekLocation(BaseModel):
    """
    адрес местоположения контрагента (отправителя, получателя), включая геолокационные данные
    """

    code: str | None = Field(
        None, max_length=255, description="Код локации (справочник СДЭК)"
    )
    region_code: Optional[int]
    fias_guid: Optional[UUID5]  # Уникальный идентификатор ФИАС
    kladr_code: str | None = Field(None, max_length=255, description="Код КЛАДР")
    postal_code: str | None = Field(None, max_length=255, description="Почтовый индекс")

    country_code: str = Field(
        "RU", max_length=2, description="Код страны в формате ISO_3166-1_alpha-2"
    )
    region: str = Field(None, max_length=255, description="Название региона")
    sub_region: str = Field(
        None, max_length=255, description=""
    )  # Название района региона

    city: str = Field("", description="Название города", max_length=255)
    address: str = Field("", description="Строка адреса", max_length=255)

    longitude: Optional[float]
    latitude: Optional[float]


class CdekService(BaseModel):
    """
    данные о дополнительных услугах
    """

    code: str
    parameter: Optional[str]


class CdekItem(BaseModel):
    """
    информация о товарах места заказа (только для заказа типа "интернет-магазин")
    """

    # Наименование товара (может также содержать описание товара: размер, цвет)
    name: str = Field(None, max_length=255, description="")
    weight: int = Field(..., description="Вес (за единицу товара, в граммах)")
    amount: int = Field(..., description="Количество единиц товара (в штуках)")
    # Объявленная стоимость товара (за единицу товара в указанной валюте, значение >=0).
    # С данного значения рассчитывается страховка
    cost: float

    # Оплата за товар при получении (за единицу товара в указанной валюте, значение >=0) — наложенный платеж,
    # в случае предоплаты значение = 0
    payment: CdekMoney = CdekMoney()

    # Содержит wifi/gsm
    wifi_gsm: Optional[bool]
    # Ссылка на сайт интернет-магазина с описанием товара
    url: str = Field(None, max_length=255, description="")
    ware_key: str = Field(
        ..., description="Идентификатор/артикул товара", max_length=20
    )

    material: str = Field(None, max_length=255, description="")  # Код материала
    country_code: str = Field(
        None, description="Код страны в формате  ISO_3166-1_alpha-2", max_length=2
    )

    brand: str = Field(
        None, max_length=255, description=""
    )  # Бренд на иностранном языке
    # Наименование на иностранном языке
    name_i18n: str = Field(None, max_length=255, description="")
    weight_gross: Optional[int]  # Вес брутто


class CdekPackage(BaseModel):
    """
    информация о местах заказа
    """

    # Номер упаковки (можно использовать порядковый номер упаковки заказа или номер заказа),
    # уникален в пределах заказа. Идентификатор заказа в ИС Клиента
    number: str = Field("", max_length=255, description="")
    weight: int  # Общий вес (в граммах)
    length: Optional[int]  # Габариты упаковки. Длина (в сантиметрах)
    width: Optional[int]  # Габариты упаковки. Ширина (в сантиметрах)
    height: Optional[int]  # Габариты упаковки. Высота (в сантиметрах)
    comment: str = Field(None, max_length=255, description="")  # Комментарий к упаковке

    items: Optional[List[CdekItem]]


CDEK_MANAGERS_ERROR_CODES = {
    "v2_internal_error": "Запрос выполнился с системной ошибкой",
    "v2_similar_request_still_processed": "Предыдущий запрос такого же типа над этой же сущностью еще не выполнился",
    "v2_bad_request": "Передан некорректный запрос",
    "v2_parameters_empty": "Все параметры запроса пустые или не переданы",
    "v2_entity_not_found": "Сущность (заказ, заявка и т.д.) с указанным идентификатором не существует, либо удалена",
    "v2_entity_forbidden": "Сущность (заказ, заявка и т.д.) с указанным идентификатором существует, но принадлежит "
    "другому клиенту",
    "v2_entity_invalid": "Сущность (заказ, заявка и т.д.) с указанным идентификатором существует, но некорректна",
    "v2_order_not_found": "Заказ с указанным номером не существует, либо удален",
    "v2_order_forbidden": "Заказ с указанным номером существует, но принадлежит другому клиенту",
    "v2_order_number_empty": "Не переданы номер и идентификатор заказа",
    "v2_sender_location_not_recognized": "Не удалось определить адрес отправителя. "
    "Попробуйте снова чуть позже, СДЭК виснет.",
    "v2_recipient_location_not_recognized": "Не удалось определить адрес получателя. "
    "Попробуйте вставить ID терминала в этом городе в адрес получателя, "
    "если доставка до терминала.",
    "v2_number_items_is_more_126": "Количество позиций товаров в заказе свыше 126",
    "orders_number_is_empty": "Заказ некорректен",
    "v2_intake_exists_by_date_address": "На переданную дату и в переданный адрес уже есть заявка",
    "v2_entity_expired": "Истек срок хранения печатной формы или квитанции с указанным идентификатором",
    "v2_entity_empty": "Печатная форма или квитанция с указанным идентификатором не сформировалась, "
    "так как все заказы некорректны",
    # Истёк токен, он обновляется каждые 30 минут.
    "v2_token_expired": "Попробуйте отправить заявки чуть позже. Если ошибка повторится - подождите 30 минут.",
}


class CdekIntakes(BaseModel):
    name: str = "Консолидированный груз"
    weight: int
    intake_date: str
    intake_time_from: str
    intake_time_to: str
    sender: CdekContact
    from_location: CdekLocation


class CdekIntakesMongo(BaseModel):
    idmonopolia: Union[int, str]
    weight: Union[int, list]
    sender: CdekContact
    from_location: CdekLocation

    @validator("weight", allow_reuse=True)
    def weight_v(cls, v):
        if isinstance(v, list) and len(v) > 0:
            i = v[0]
            if isinstance(i, list) and len(i) > 0:
                return i[0]
            else:
                return i
        raise ValidationError()

    @validator("idmonopolia", allow_reuse=True)
    def idmonopolia_v(cls, v):
        # Где-то видимо монополия пишется как строка
        return int(v)


class CdekTypeEnum(IntEnum):
    """
    Тип заказа:
    1 - "интернет-магазин" (только для договора типа "Договор с ИМ")
    2 - "доставка" (для любого договора)

    По умолчанию - 1
    """

    internet_shop = 1
    delivery = 2


class TariffCodesInternetShops(IntEnum):
    """
    https://confluence.cdek.ru/pages/viewpage.action?pageId=29923959
    """

    ###############
    # 30 kg max
    """
    Услуга экономичной доставки товаров по России для компаний, осуществляющих дистанционную торговлю.
    """
    ###############
    package_warehouse_warehouse = 136
    package_warehouse_door = 137
    package_door_warehouse = 138
    package_door_door = 139
    ###############

    ###############
    # 50 kg max
    """
    Услуга экономичной наземной доставки товаров по России для компаний, осуществляющих дистанционную торговлю.
    Услуга действует по направлениям из Москвы в подразделения СДЭК, находящиеся за Уралом и в Крым.
    """
    ###############
    economical_package_warehouse_door = 233
    economical_package_warehouse_warehouse = 234
    ###############

    ###############
    # unlimited
    """
    Сервис по доставке товаров из-за рубежа в Россию, Украину, Казахстан, Киргизию, Узбекистан с услугами
    по таможенному оформлению.
    Предлагается 2 схемы работы:
    1) клиент доставляет заказ на таможенный пост в России. Мы встречаем, помогаем с таможней и доставляем адресату;
    2) клиент привозит посылки на один из наших складов за рубежом. Мы перевозим их на таможенный пост в
    Россию, проводим очистку и доставляем получателю.
    """
    ###############
    express_warehouse_warehouse = 291
    express_door_door = 293
    express_warehouse_door = 294
    express_door_warehouse = 295
    ###############


class BaseCdekInternetShopOrder(BaseModel):
    type: CdekTypeEnum = CdekTypeEnum.internet_shop.value

    number: str | None = Field(
        None,
        max_length=32,
        description="Номер заказа в ИС Клиента (будет присвоен номер заказа в СДЭК - uuid). Только для ИМ,",
    )

    tariff_code: int = TariffCodesInternetShops.package_door_door.value
    comment: str = Field(None, max_length=255)
    developer_key: Optional[str]

    shipment_point: str | None = Field(
        None,
        max_length=255,
        description="Код ПВЗ СДЭК, на который будет производиться самостоятельный привоз клиентом "
        "Не может использоваться одновременно с from_location "
        'Обяз, если заказ с тарифом "от склада"',
    )

    delivery_point: str | None = Field(
        None,
        max_length=255,
        description="Код ПВЗ СДЭК, на который будет доставлена посылка"
        "Не может использоваться одновременно с to_location"
        'Обяз, если заказ с тарифом "от склада" или "до постамата"',
    )

    # Инвойс является коммерческим документом, выданным продавцом покупателю и относящимся к сделке продажи,
    # с указанием продуктов/услуг, их количеств и согласованных цен. Инвойс может быть как бумажным так и электронным.

    # дата инвойса, Только для заказов "интернет-магазин"
    date_invoice: Optional[datetime.date] = None
    shipper_name: str | None = Field(
        None,
        max_length=255,
        description='Грузоотправитель, Только для заказов "интернет-магазин"',
    )

    shipper_address: str | None = Field(
        None,
        max_length=255,
        description='Адрес грузоотправителя, Только для заказов "интернет-магазин"',
    )

    # Доп. сбор за доставку, которую ИМ берет с получателя.
    # Только для заказов "интернет-магазин"
    delivery_recipient_cost: CdekMoney = CdekMoney()

    # Доп. сбор за доставку (которую ИМ берет с получателя) в зависимости от суммы заказа
    # Только для заказов "интернет-магазин"
    delivery_recipient_cost_adv: Optional[List[CdekThreshold]] = None

    # Отправитель
    # Не обязателен, если заказ типа "интернет-магазин"
    # Обязателен, если заказ типа "доставка"
    sender: CdekContact = CdekContact()

    # Реквизиты истинного продавца
    # Только для заказов "интернет-магазин"
    # Обязателен, если заказ международный
    seller: CdekSeller = CdekSeller()

    # Получатель
    recipient: CdekContact = CdekContact()

    # Адрес отправления
    # Не может использоваться одновременно с shipment_point
    # Обязателен, если заказ с тарифом "от двери"
    from_location: Optional[CdekLocation] = None

    # Адрес получения
    # Не может использоваться одновременно с delivery_point
    # Обязателен, если заказ с тарифом "от двери"
    to_location: Optional[CdekLocation] = None

    # Дополнительные услуги
    services: list[CdekService] = Field(default_factory=list)

    packages: list[CdekPackage] = Field(default_factory=list)

    print: str | None = Field(
        None,
        max_length=7,
        description="""Необходимость сформировать печатную форму по заказу
    Может принимать значения:
    barcode - ШК мест (число копий - 1)
    waybill - квитанция (число копий - 2)""",
    )


class CdekServices:
    # СТРАХОВАНИЕ
    # Услуга начисляется автоматически для всех заказов типа "интернет-магазин",
    # не разрешена для самостоятельной передачи в поле services.code.
    insurance = "INSURANCE"

    # ДОСТАВКА В ВЫХОДНОЙ ДЕНЬ
    deliv_weekend = "DELIV_WEEKEND"

    # ЗАБОР В ГОРОДЕ ОТПРАВИТЕЛЕ
    take_sender = "TAKE_SENDER"

    # ДОСТАВКА В ГОРОДЕ ПОЛУЧАТЕЛЕ
    deliv_receiver = "DELIV_RECEIVER"

    # ПРИМЕРКА
    trying_on = "TRYING_ON"

    # ЧАСТИЧНАЯ ДОСТАВКА
    part_deliv = "PART_DELIV"

    # ОСМОТР ВЛОЖЕНИЯ
    inspection_cargo = "INSPECTION_CARGO"

    # РЕВЕРС
    reverse = "REVERSE"

    # ОПАСНЫЙ ГРУЗ
    danger_cargo = "DANGER_CARGO"

    # УПАКОВКА 1
    # Стоимость коробки размером 310*215*280мм — 30 руб. (для грузов до 10 кг).
    package = "PACKAGE_1"
