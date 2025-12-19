from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from app.dependencies import get_current_user

router = APIRouter()

# Simple in-memory store keyed by user id for quick demo purposes
_store: Dict[int, Dict[int, Dict[str, Any]]] = {}
_id_counters: Dict[int, int] = {}


@router.get("/", response_model=List[Dict])
async def list_bills(current_user=Depends(get_current_user)):
	user_id = current_user.id
	items = list(_store.get(user_id, {}).values())
	return items


@router.post("/")
async def create_bill(payload: Dict, current_user=Depends(get_current_user)):
	user_id = current_user.id
	_id_counters.setdefault(user_id, 0)
	_id_counters[user_id] += 1
	bill_id = _id_counters[user_id]
	record = {"id": bill_id, **payload}
	_store.setdefault(user_id, {})[bill_id] = record
	return record


@router.put("/{bill_id}")
async def update_bill(bill_id: int, payload: Dict, current_user=Depends(get_current_user)):
	user_id = current_user.id
	user_bills = _store.get(user_id, {})
	if bill_id not in user_bills:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")
	user_bills[bill_id].update(payload)
	return user_bills[bill_id]


@router.delete("/{bill_id}")
async def delete_bill(bill_id: int, current_user=Depends(get_current_user)):
	user_id = current_user.id
	user_bills = _store.get(user_id, {})
	if bill_id not in user_bills:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")
	del user_bills[bill_id]
	return {"message": "Bill deleted"}

