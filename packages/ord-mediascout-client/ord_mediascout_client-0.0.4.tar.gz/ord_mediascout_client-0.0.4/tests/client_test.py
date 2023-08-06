import pytest

from ord_mediascout_client import (
    ClientRelationshipType,
    CounterpartyStatus,
    CreateClientWebApiDto,
    LegalForm,
    ORDMediascoutClient,
    ORDMediascoutConfig,
)


@pytest.fixture
def client() -> ORDMediascoutClient:
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


def test_create_client(client: ORDMediascoutClient) -> None:
    request_data = CreateClientWebApiDto(
        createMode=ClientRelationshipType.DirectClient,
        legalForm=LegalForm.JuridicalPerson,
        inn='4401116480',
        name='Совкомбанк',
        mobilePhone='111222333',
        epayNumber='1234',
        regNumber='1234',
        oksmNumber='1234',
    )

    response_data = client.create_client(request_data)

    print(response_data)

    assert request_data.name == response_data.name
    assert request_data.inn == response_data.inn
    # assert request_data.mobilePhone == response_data.mobilePhone
    # assert request_data.epayNumber == response_data.epayNumber
    # assert request_data.regNumber == response_data.regNumber
    # assert request_data.oksmNumber == response_data.oksmNumber
    # assert request_data.createMode == response_data.createMode
    assert request_data.legalForm == response_data.legalForm
    assert response_data.id is not None
    assert response_data.status == CounterpartyStatus.Active
