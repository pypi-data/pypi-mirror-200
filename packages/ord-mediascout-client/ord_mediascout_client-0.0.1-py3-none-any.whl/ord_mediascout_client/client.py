from typing import Any, Optional

import requests as requests
from pydantic.main import BaseModel
from pydantic.tools import parse_raw_as
from requests.auth import HTTPBasicAuth

from .config import ORDMediascoutConfig
from .models import (
    BadRequestWebApiDto,
    ClearInvoiceDataWebApiDto,
    ClientWebApiDto,
    CreateClientWebApiDto,
    CreateCreativeWebApiDto,
    CreateFinalContractWebApiDto,
    CreateInitialContractWebApiDto,
    CreateInvoiceWebApiDto,
    CreateOuterContractWebApiDto,
    CreatePlatformWebApiDto,
    CreativeWebApiDto,
    EditCreativeWebApiDto,
    EditFinalContractWebApiDto,
    EditInitialContractWebApiDto,
    EditInvoiceDataWebApiDto,
    EditInvoiceStatisticsWebApiDto,
    EditOuterContractWebApiDto,
    EditPlatformWebApiDto,
    EntityIdWebApiDto,
    FinalContractWebApiDto,
    GetClientsWebApiDto,
    GetCreativesWebApiDto,
    GetFinalContractsWebApiDto,
    GetInitialContractsWebApiDto,
    GetInvoicesWebApiDto,
    GetOuterContractsWebApiDto,
    InitialContractWebApiDto,
    InvoiceSummaryWebApiDto,
    InvoiceWebApiDto,
    OuterContractWebApiDto,
    PlatformCardWebApiDto,
    SelfPromotionContractWebApiDto,
    SupplementInvoiceWebApiDto,
)


class APIError(Exception):
    pass


class BadResponse(APIError):
    def __init__(self, status_code: int, error: Optional[BadRequestWebApiDto] = None):
        super().__init__(error and error.errorType or f'Bad response from API: {status_code}')
        self.status_code = status_code
        self.error = error


class ORDMediascoutClient:
    def __init__(self, config: ORDMediascoutConfig):
        self.config = config
        self.auth = HTTPBasicAuth(self.config.username, self.config.password)

    def _call(
        self, method: str, url: str, obj: Optional[BaseModel] = None, **kwargs: dict[str, Any]
    ) -> requests.Response:
        response = requests.request(
            method, f'{self.config.url}{url}', json=obj and obj.dict(), auth=self.auth, **kwargs
        )
        match response.status_code:
            case 400 | 401:
                bad_response = BadRequestWebApiDto.parse_raw(response.text)
                raise BadResponse(response.status_code, bad_response)
            case 500:
                raise BadResponse(response.status_code)
            case 200 | 201:
                return response
        raise BadResponse(response.status_code)

    # Clients
    def create_client(self, client: CreateClientWebApiDto) -> ClientWebApiDto:
        response = self._call('post', '/webapi/Clients/CreateClient', client)
        client = ClientWebApiDto.parse_raw(response.text)
        return client

    def get_clients(self, parameters: GetClientsWebApiDto) -> list[ClientWebApiDto]:
        response = self._call('post', '/webapi/Clients/GetClients', parameters)
        clients: list[ClientWebApiDto] = parse_raw_as(list[ClientWebApiDto], response.text)
        return clients

    # Contracts
    def create_initial_contract(self, contract: CreateInitialContractWebApiDto) -> InitialContractWebApiDto:
        response = self._call('post', '/webapi/Contracts/CreateInitialContract', contract)
        contract = InitialContractWebApiDto.parse_raw(response.text)
        return contract

    def edit_initial_contract(self, contract: EditInitialContractWebApiDto) -> InitialContractWebApiDto:
        response = self._call('post', '/webapi/Contracts/EditInitialContract', contract)
        contract = InitialContractWebApiDto.parse_raw(response.text)
        return contract

    def get_initial_contracts(self, parameters: GetInitialContractsWebApiDto) -> list[InitialContractWebApiDto]:
        response = self._call('post', '/webapi/Contracts/GetInitialContracts', parameters)
        contracts: list[InitialContractWebApiDto] = parse_raw_as(list[InitialContractWebApiDto], response.text)
        return contracts

    def create_final_contract(self, contract: CreateFinalContractWebApiDto) -> FinalContractWebApiDto:
        response = self._call('post', '/webapi/Contracts/CreateFinalContract', contract)
        contract = FinalContractWebApiDto.parse_raw(response.text)
        return contract

    def edit_final_contract(self, contract: EditFinalContractWebApiDto) -> FinalContractWebApiDto:
        response = self._call('post', '/webapi/Contracts/EditFinalContract', contract)
        contract = FinalContractWebApiDto.parse_raw(response.text)
        return contract

    def get_final_contracts(self, parameters: GetFinalContractsWebApiDto) -> list[FinalContractWebApiDto]:
        response = self._call('post', '/webapi/Contracts/GetFinalContracts', parameters)
        contracts: list[FinalContractWebApiDto] = parse_raw_as(list[FinalContractWebApiDto], response.text)
        return contracts

    def create_outer_contract(self, contract: CreateOuterContractWebApiDto) -> OuterContractWebApiDto:
        response = self._call('post', '/webapi/Contracts/CreateOuterContract', contract)
        contract = OuterContractWebApiDto.parse_raw(response.text)
        return contract

    def edit_outer_contract(self, contract: EditOuterContractWebApiDto) -> OuterContractWebApiDto:
        response = self._call('post', '/webapi/Contracts/EditOuterContract', contract)
        contract = OuterContractWebApiDto.parse_raw(response.text)
        return contract

    def get_outer_contracts(self, parameters: GetOuterContractsWebApiDto) -> list[OuterContractWebApiDto]:
        response = self._call('post', '/webapi/Contracts/GetOuterContracts', parameters)
        contracts: list[OuterContractWebApiDto] = parse_raw_as(list[OuterContractWebApiDto], response.text)
        return contracts

    def create_self_promotion_contract(
        self, contract: SelfPromotionContractWebApiDto
    ) -> SelfPromotionContractWebApiDto:
        response = self._call('post', '/webapi/Contracts/CreateSelfPromotionContract', contract)
        contract = SelfPromotionContractWebApiDto.parse_raw(response.text)
        return contract

    def get_self_promotion_contracts(self) -> list[SelfPromotionContractWebApiDto]:
        response = self._call('post', '/webapi/Contracts/GetSelfPromotionContracts')
        contracts: list[SelfPromotionContractWebApiDto] = parse_raw_as(
            list[SelfPromotionContractWebApiDto], response.text
        )
        return contracts

    # Creatives
    def create_creative(self, creative: CreateCreativeWebApiDto) -> EntityIdWebApiDto:
        response = self._call('post', '/webapi/creatives/CreateCreative', creative)
        entity = EntityIdWebApiDto.parse_raw(response.text)
        return entity

    def edit_creative(self, creative: EditCreativeWebApiDto) -> CreativeWebApiDto:
        response = self._call('post', '/webapi/creatives/EditCreative', creative)
        contract = CreativeWebApiDto.parse_raw(response.text)
        return contract

    def get_creatives(self, parameters: GetCreativesWebApiDto) -> list[CreativeWebApiDto]:
        response = self._call('post', '/webapi/creatives/GetCreatives', parameters)
        clients: list[CreativeWebApiDto] = parse_raw_as(list[CreativeWebApiDto], response.text)
        return clients

    # Invoices
    def create_invoice(self, invoice: CreateInvoiceWebApiDto) -> EntityIdWebApiDto:
        response = self._call('post', '/webapi/Invoices/CreateInvoice', invoice)
        entity = EntityIdWebApiDto.parse_raw(response.text)
        return entity

    def edit_invoice(self, invoice: EditInvoiceDataWebApiDto) -> InvoiceWebApiDto:
        response = self._call('post', '/webapi/Invoices/EditInvoice', invoice)
        invoice = InvoiceWebApiDto.parse_raw(response.text)
        return invoice

    def overwrite_invoice(self, invoice: EditInvoiceStatisticsWebApiDto) -> None:
        self._call('post', '/webapi/Invoices/OverwriteInvoice', invoice)

    def clear_invoice(self, invoice: ClearInvoiceDataWebApiDto) -> None:
        self._call('post', '/webapi/Invoices/ClearInvoice', invoice)

    def supplement_invoice(self, invoice: SupplementInvoiceWebApiDto) -> EntityIdWebApiDto:
        response = self._call('post', '/webapi/Invoices/SupplementInvoice', invoice)
        entity = EntityIdWebApiDto.parse_raw(response.text)
        return entity

    def get_invoices(self, parameters: GetInvoicesWebApiDto) -> list[InvoiceWebApiDto]:
        response = self._call('post', '/webapi/Invoices/GetInvoices', parameters)
        invoices: list[InvoiceWebApiDto] = parse_raw_as(list[InvoiceWebApiDto], response.text)
        return invoices

    def get_invoice_summary(self, entity: EntityIdWebApiDto) -> InvoiceSummaryWebApiDto:
        response = self._call('post', '/webapi/Invoices/GetInvoiceSummary', entity)
        invoice_summary = InvoiceSummaryWebApiDto.parse_raw(response.text)
        return invoice_summary

    def confirm_invoice(self, entity: EntityIdWebApiDto) -> None:
        self._call('post', '/webapi/Invoices/ConfirmInvoice', entity)

    def delete_invoice(self, entity: EntityIdWebApiDto) -> None:
        self._call('post', '/webapi/Invoices/DeleteInvoices', entity)

    # WebApiPlatform
    def create_platform(self, platform: CreatePlatformWebApiDto) -> EntityIdWebApiDto:
        response = self._call('post', '/webapi/Platforms/CreatePlatform', platform)
        entity = EntityIdWebApiDto.parse_raw(response.text)
        return entity

    def edit_platform(self, platform: EditPlatformWebApiDto) -> PlatformCardWebApiDto:
        response = self._call('post', '/webapi/Platforms/EditPlatform', platform)
        platform = PlatformCardWebApiDto.parse_raw(response.text)
        return platform

    # PING
    def ping(self) -> bool:
        tmp_auth, self.auth = self.auth, None
        self._call('get', '/webapi/Ping')
        self.auth = tmp_auth
        return True

    def ping_auth(self) -> bool:
        self._call('get', '/webapi/PingAuth')
        return True
