from typing import List, Dict
from flask_restx import Model, fields
from decimal import Decimal, ROUND_HALF_EVEN
import copy

class NumberFixed(fields.NumberMixin, fields.Raw):
    """
    A decimal number with a fixed precision.
    """

    def __init__(self, decimals=5, **kwargs):
        super(NumberFixed, self).__init__(**kwargs)
        self.precision = Decimal("0." + "0" * (decimals - 1) + "1")

    def format(self, value):
        dvalue = Decimal(value)
        if not dvalue.is_normal() and dvalue != Decimal():
            raise fields.MarshallingError("Invalid Fixed precision number.")
        return dvalue.quantize(self.precision, rounding=ROUND_HALF_EVEN)

paginator_model = Model('Paginator', {
    'currentPage': fields.Integer(description='Текущая страница'),
    'recordsOnPage': fields.Integer(description='Элементов на странице'),
    'totalPages': fields.Integer(description='Всего страниц')
})

user_model = Model('User', {
    'id': fields.Integer(description='Идентификатор пользователя'),
    'idKey': fields.String(description='ИНН'),
    'titleName': fields.String(description='Имя профиля'),
    'isCompany': fields.Boolean(description='ООО/ФОП')
})

profile_model = Model('Profile', {
    'accountId': fields.Integer(description='Идентификатор аккаунта'),
    'accountName': fields.String(description='Имя аккаунта'),
    'users': fields.List(fields.Nested(user_model), description='Зарегистрированные профили')
})

user_bank_account_common_params:dict = {
    'title': fields.String(description='Название счета'),
    'currency': fields.String(description='Валюта'),
    'num': fields.String(description='Номер счета в банке'),
    'bank': fields.String(description='Название банка'),
    'mfo': fields.String(description='МФО'),
    'comment': fields.String(description='Коментарий'),
    'tfBankPlace': fields.String(description='Адрес банка'),
    'tfBankSwift': fields.String(description='SWIFT'),
    'tfBankCorr': fields.String(description='Названия банка-корреспондента'),
    'tfBankCorrPlace': fields.String(description='Адрес банка-корреспондента'),
    'tfBankCorrSwift': fields.String(description='SWIFT банка-корреспондента'),
    'tfBankCorrAccount': fields.String(description='Счет в банке-корреспонденте'),
}

user_bank_account_model = Model('UserBankAccount', {
    'id': fields.Integer(description='Идентификатор счета профиля'),
    'balance': NumberFixed(description='Баланс счета', decimals=2),
    **user_bank_account_common_params
})

add_user_bank_account_model = Model('AddUserBankAccount', {**user_bank_account_common_params})
add_user_bank_account_response_model = Model('AddUserBankAccountResponse', {
    'id': fields.Integer(description='Идентификатор счета'),
})

user_bank_account_brief_model = Model('UserBankAccountBrief', {
    'id': fields.Integer(description='Идентификатор счета'),
    'title': fields.String(description='Название счета', allow_null=True, skip_none=True),
    'currency': fields.String(description='Валоюта счета', allow_null=True, skip_none=True),
})

user_bank_account_short_model = Model('UserBankAccountShort', {
    'id': fields.Integer(description='Идентификатор счета'),
})

user_accounts_model = Model('UserAccounts', {
    'paginator': fields.Nested(paginator_model, description='Страницы'),
    'accountsCurrencies': fields.List(fields.String, description='Валюты счетов'),
    'accounts': fields.List(fields.Nested(user_bank_account_model, skip_none=True), description='Счета'),
})

operation_brief_content_model = Model('OperationBriefContent', {
        'id': fields.Integer(description='Идентификатор'),
        'date': fields.DateTime(description='Дата'),
        'sumCurrency': NumberFixed(description='Сумма в валюте', decimals=2),
        'accountTitle': fields.String(description='Название профиля'),
        'accountCurrency': fields.String(description='Валюта профиля'),
        'comment': fields.String(description='Коментарий'),
    })

operation_brief_model = Model('OperationBrief', {
    'id': fields.Integer(description='Идентификатор операции'),
    'type': fields.String(description='Тип'),
    'path': fields.String(description='URL для получения полной информации по операции'),
    'comment': fields.String(description='Коментарий', allow_null=True),
    'contents': fields.List(fields.Nested(operation_brief_content_model, allow_null=True), description='Данные', allow_null=True),
})

operations_brief_model = Model('OperationsBrief', {
    'paginator': fields.Nested(paginator_model, description='Страницы'),
    'currencies': fields.List(fields.String, description='Валюты'),
    'operations': fields.List(fields.Nested(operation_brief_model), description='Операции'),
})

contractor_model = Model('Contractor', {
    'id': fields.Integer(description='Идентификатор заказчика'),
    'title': fields.String(description='Название заказчика', allow_null=True, skip_none=True),
})

contractor_short_model = Model('ContractorShort', {
    'id': fields.Integer(description='Идентификатор заказчика'),
})


parent_model = Model('Parent', {
    'id': fields.Integer(description='Идентификатор'),
    'date': fields.DateTime(description='Дата', allow_null=True),
    'number': fields.String(description='Номер', allow_null=True),
    'title': fields.String(description='Название', allow_null=True),
    'type': fields.String(description='Тип', allow_null=True),
    'contractor':fields.Nested(contractor_model, description='Контрагент', allow_null=True,
                                  skip_none=True),
})

parent_short_model = Model('ParentShort', {
    'id': fields.Integer(description='Идентификатор'),
})

parent_short_type_model = Model('ParentShortType', {
    'id': fields.Integer(description='Идентификатор'),
    'type': fields.String(description='Тип', allow_null=True),
})


add_operation_response_model = Model('AddOperationResponse', {
    'id': fields.Integer(description='Идентификатор операции'),
})


operation_base_common_params:Dict = {
    'date': fields.DateTime(description='Дата'),
    'comment': fields.String(description='Коментарий', allow_null=True),
}
operation_base_model = Model('OperationBase', {
    'id': fields.Integer(description='Идентификатор операции'),
    **operation_base_common_params
})


add_operation_base_model = Model('AddOperation', {**operation_base_common_params})

operation_filter_model = Model('OperationFilter', {
    'filterType': fields.String(description='Тип операции (Withdrawal - перевод между счетами; FlowIncome - доход; FlowOutgo - расход; CurrencyExchange - обмен валюты; )'),
})



"""Withdrawal - перевод между счетами"""

operation_withdrawal_common_params:Dict = {
    'outgoTotal': NumberFixed(description='Сумма перевода', decimals=2, allow_null=True, skip_none=True),
}
operation_withdrawal_model = operation_base_model.clone('OperationWithdrawal', {**operation_withdrawal_common_params,
    'outgoAccount': fields.Nested(user_bank_account_brief_model, description='Счет списания', allow_null=True,
                                  skip_none=True),
    'incomeAccount': fields.Nested(user_bank_account_brief_model, description='Счет зачисления', allow_null=True,
                                   skip_none=True),
})
add_operation_withdrawal_model = add_operation_base_model.clone('AddOperationWithdrawal', {**operation_withdrawal_common_params,
    'outgoAccount': fields.Nested(user_bank_account_short_model, description='Счет списания', allow_null=True,
                                  skip_none=True),
    'incomeAccount': fields.Nested(user_bank_account_short_model, description='Счет зачисления', allow_null=True,
                                   skip_none=True),
})

"""FlowIncome - доход"""
operation_flowincome_common_params:Dict = {
    'financeType': fields.String(
        description='Тип дохода ("custom" - Основной; "custom_free" - Безвозмездно полученные товары и услуги; "tax_free" - Не учитываемый; "custom_debts" - Списанные задолжености;'
                    ' "tax15_1" - 15% Превышение основного дохода; "tax15_2" - 15% Не указанная в свидетельстве деятельность; "tax15_2" - 15% Запрещенные для ЕН расчеты)<br>'
                    'или <br>Тип расхода ("custom" - Основной; "esv" - Оплата ЕСВ; "en" - Оплата ЕН; "moneyback" - Возвращенные деньги)',
        allow_null=True),
    'total': NumberFixed(description='Сумма перевода', decimals=2, allow_null=True, skip_none=True),
    'payedSum': NumberFixed(description='Сумма по документу', decimals=2, allow_null=True, skip_none=True),
}
flowincome_params:Dict = {
    'account': fields.Nested(user_bank_account_brief_model, description='Счет зачисления', allow_null=True,
                             skip_none=True),
    'contractor':fields.Nested(contractor_model, description='Контрагент', allow_null=True,
                                  skip_none=True),
    'parent': fields.Nested(parent_model, description='Договор', allow_null=True,
                                skip_none=True),

}
operation_flowincome_model = operation_base_model.clone('OperationFlowIncome', {**operation_flowincome_common_params,
    'account': fields.Nested(user_bank_account_brief_model, description='Счет зачисления', allow_null=True,
                             skip_none=True),
    'contractor':fields.Nested(contractor_model, description='Контрагент', allow_null=True,
                                  skip_none=True),
    'parent': fields.Nested(parent_model, description='Договор', allow_null=True,
                                skip_none=True),
})
add_operation_flowincome_model = add_operation_base_model.clone('AddOperationFlowIncome', {**operation_flowincome_common_params,
    'account': fields.Nested(user_bank_account_short_model, description='Счет зачисления', allow_null=True,
                             skip_none=True),
    'contractor':fields.Nested(contractor_short_model, description='Контрагент', allow_null=True,
                                  skip_none=True),
    'parent': fields.Nested(parent_short_type_model, description='Договор', allow_null=True,
                                skip_none=True),
})

"""FlowOutgo - расход"""
operation_flowoutgo_model = operation_flowincome_model.clone('OperationFlowOutgo')
add_operation_flowoutgo_model = add_operation_flowincome_model.clone('AddOperationFlowOutgo')

"""CurrencyExchange - обмен валюты"""
currency_exchange_model = operation_withdrawal_model.clone('CurrencyExchange', {
    'total': NumberFixed(description='Сумма', decimals=2, allow_null=True, skip_none=True),
    'incomeCurrency': NumberFixed(description='Курс', decimals=2, allow_null=True, skip_none=True),
    'exchangeDifferenceAmount': NumberFixed(description='Курсовая разница', decimals=2, allow_null=True, skip_none=True),
})
add_currency_exchange_model = add_operation_withdrawal_model.clone('AddCurrencyExchange', {
    'incomeCurrency': NumberFixed(description='Курс', decimals=2, allow_null=True, skip_none=True),
})

"""AutoExchange - валютный доход"""
auto_exchange_common_params:Dict = {
    'payedSum': NumberFixed(description='Сумма по документу', decimals=2, allow_null=True, skip_none=True),
    'uahDate': fields.DateTime(description='Дата обязательной продажи'),
    'uahTotal': NumberFixed(description='Сумма в UAH обязательной продажи', decimals=2, allow_null=True,
                            skip_none=True),
    'currencyTotal': NumberFixed(description='Сумма зашедшая на валютный счет', decimals=2, allow_null=True,
                                 skip_none=True),
}

auto_exchange_model = operation_base_model.clone('AutoExchange', {**auto_exchange_common_params,
 'parent': fields.Nested(parent_model, description='Договор', allow_null=True, skip_none=True),
 'contractor': fields.Nested(contractor_model, description='Контрагент', allow_null=True, skip_none=True),
 'uahAccount': fields.Nested(user_bank_account_brief_model, description='Счет зачисления при обязательной продаже',
                             allow_null=True, skip_none=True),
 'currencyAccount': fields.Nested(user_bank_account_brief_model, description='Валютный счет', allow_null=True,
                                  skip_none=True),
})
add_auto_exchange_model = add_operation_base_model.clone('AddAutoExchange', {**auto_exchange_common_params,
 'parent': fields.Nested(parent_short_type_model, description='Договор', allow_null=True, skip_none=True),
 'contractor': fields.Nested(contractor_short_model, description='Контрагент', allow_null=True, skip_none=True),
 'uahAccount': fields.Nested(user_bank_account_short_model, description='Счет зачисления при обязательной продаже',
                             allow_null=True, skip_none=True),
 'currencyAccount': fields.Nested(user_bank_account_short_model, description='Валютный счет', allow_null=True,
                                  skip_none=True),
})

"""********************************   Documents ******************************"""

document_common_params:Dict = {
    'date': fields.DateTime(description='Дата создания/подписания документа'),
    'direction': fields.Integer(description='0 - продажа, 1 покупка??'),
    'number': fields.String(description='Номер документа'),
#    'contractor': fields.Nested(contractor_model, description='Контрагент', allow_null=True, skip_none=True),
    'currency': fields.String(description='Валюта документа'),
    'total': NumberFixed(description='Сумма документа', decimals=2, allow_null=True, skip_none=True),
    'title': fields.String(description='Название документа'),
    'comment': fields.String(description='Коментарий'),
}


document_brief_params:Dict = {**document_common_params,
    'id': fields.Integer(description='Идентификатор документа'),
    'type': fields.String(description='Тип документа'),
    'contractor': fields.Nested(contractor_model, description='Контрагент', allow_null=True, skip_none=True),
    'paid': NumberFixed(description='Оплачено по документу', decimals=2, allow_null=True, skip_none=True),
}

new_document_params:Dict = {**document_common_params,
    'contractor': fields.Nested(contractor_short_model, description='Контрагент', allow_null=True, skip_none=True),
}


document_brief_model = Model('DocumentBrief', {**document_brief_params,
    'path': fields.String(description='URL для получения полной информации по операции'),
                                               })
#new_document_params = document_brief_params.copy()
#del new_document_params['id']
#del new_document_params['type']
#del new_document_params['paid']

document_contract_params = {
    'expireDate': fields.DateTime(description='Дата окончания действия документа'),
    'description': fields.String(description='Описание'),
    'place': fields.String(description='Место'),
}

"""contract - Договор"""

document_contract_model = Model('DocumentContract', {**document_brief_params, **document_contract_params})
add_document_contract_model = Model('AddDocumentContract', {**new_document_params, **document_contract_params})


"""act - Акт"""
act_content_model = Model("ActContent", {
    'id': fields.Integer(description='Идентификатор записи'),
    'title': fields.String(description='Название'),
    'titleTf': fields.String(description='Название2'),
    'measure': fields.String(description='Еденица измерения'),
    'measureTf': fields.String(description='Еденица измерения2'),
    'quantity': fields.Integer(description='Количество'),
    'price': NumberFixed(description='Цена', decimals=2, allow_null=True, skip_none=True),
})

document_act_common_params:Dict = {
    'nds': fields.Integer(description='НДС (-1 - Без НДС)'),
    'actPlace': fields.String(description='Место'),
    'actType': fields.String(description='actType'),
    'actPrintType': fields.String(description='actPrintType'),
    'isForeign': fields.Integer(description='isForeign'),
    'contents' : fields.List(fields.Nested(act_content_model, allow_null=False), description='Содержание', allow_null=False, required=True, min_items=1),
}
document_act_model = Model('DocumentAct', {**document_brief_params, **document_act_common_params,
    'account': fields.Nested(user_bank_account_brief_model, description='Счет', allow_null=True, skip_none=True),
    'parent': fields.Nested(parent_model, description='Договор', allow_null=True, skip_none=True),
})
add_document_act_model = Model('AddDocumentAct', {**new_document_params, **document_act_common_params,
    'account': fields.Nested(user_bank_account_short_model, description='Счет', allow_null=True, skip_none=True),
    'parent': fields.Nested(parent_short_type_model, description='Договор', allow_null=True, skip_none=True),
})

documents_model = Model('Documents', {
    'paginator': fields.Nested(paginator_model, description='Страницы'),
    'documents': fields.List(fields.Nested(document_brief_model), description='Документы'),
})

add_document_response_model = Model('AddDocumentResponse', {
    'id': fields.Integer(description='Идентификатор документа'),
})


models:List[Model] = [
    paginator_model, user_model, profile_model, user_bank_account_model, user_accounts_model, user_bank_account_brief_model, user_bank_account_short_model, add_user_bank_account_model
    , add_user_bank_account_response_model
    , operation_brief_content_model, operation_brief_model
    , operations_brief_model, contractor_model, contractor_short_model, document_brief_model, document_contract_model, document_act_model, documents_model, add_operation_response_model
    , add_operation_base_model

    , operation_base_model, operation_filter_model, parent_model, parent_short_model, parent_short_type_model
    , operation_withdrawal_model, add_operation_withdrawal_model
    , operation_flowincome_model, add_operation_flowincome_model
    , operation_flowoutgo_model, add_operation_flowoutgo_model
    , currency_exchange_model, add_currency_exchange_model
    , auto_exchange_model, add_auto_exchange_model
    , add_document_contract_model, act_content_model, add_document_act_model, add_document_response_model
]
