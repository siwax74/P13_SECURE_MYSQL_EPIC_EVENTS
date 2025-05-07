from app.mixins import CRUDMixin
from app.models.client import Client
from app.models.contract import Contract


def test_create_contract(session, contract_data):
    crud = CRUDMixin(session)
    contract = crud.create(Contract, **contract_data)
    assert contract is not None
    for key, value in contract_data.items():
        assert getattr(contract, key) == value


def test_update_contract(session, contract_data):
    crud = CRUDMixin(session)
    contract = crud.create(Contract, **contract_data)
    updated_contract = crud.update(Contract, contract.id, total_amount=12000.0)
    assert updated_contract.total_amount == 12000.0


def test_delete_contract(session, contract_data):
    crud = CRUDMixin(session)
    contract = crud.create(Contract, **contract_data)
    deleted_contract = crud.delete(Contract, contract.id)
    assert deleted_contract is not None
    deleted_contract_check = session.query(Contract).filter_by(id=contract.id).first()
    assert deleted_contract_check is None


def test_list_contracts(session, contract_data):
    crud = CRUDMixin(session)
    crud.create(Contract, **contract_data)
    crud.create(
        Contract, client_id=2, contact_commercial_id=2, total_amount=5000.0, remaining_amount=2000.0, signed=False
    )
    contracts = crud.list(Contract)
    assert len(contracts) >= 2
    assert any(c.client_id == 1 for c in contracts)
    assert any(c.client_id == 2 for c in contracts)
