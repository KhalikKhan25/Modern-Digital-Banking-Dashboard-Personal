from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from app.dependencies import get_current_user

router = APIRouter()

# In-memory rewards store per-user for demo purposes
_store: Dict[int, Dict[int, Dict[str, Any]]] = {}
_id_counters: Dict[int, int] = {}


@router.get("/", response_model=List[Dict])
async def list_rewards(current_user=Depends(get_current_user)):
	items = list(_store.get(current_user.id, {}).values())
	return items


@router.post("/")
async def create_reward(payload: Dict, current_user=Depends(get_current_user)):
	uid = current_user.id
	_id_counters.setdefault(uid, 0)
	_id_counters[uid] += 1
	rid = _id_counters[uid]
	rec = {"id": rid, **payload}
	_store.setdefault(uid, {})[rid] = rec
	return rec


@router.put("/{reward_id}")
async def update_reward(reward_id: int, payload: Dict, current_user=Depends(get_current_user)):
	uid = current_user.id
	user_rewards = _store.get(uid, {})
	if reward_id not in user_rewards:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found")
	user_rewards[reward_id].update(payload)
	return user_rewards[reward_id]


@router.delete("/{reward_id}")
async def delete_reward(reward_id: int, current_user=Depends(get_current_user)):
	uid = current_user.id
	user_rewards = _store.get(uid, {})
	if reward_id not in user_rewards:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found")
	del user_rewards[reward_id]
	return {"message": "Reward deleted"}

