from fastapi import APIRouter, Path
from services.user_service import UserService
from utils.jwt_manager import generate_token, verify_token
from fastapi import HTTPException, status
from bson import ObjectId

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)



# User sends a request with his access link
# The backend checks if the link is valid
# If it is, it returns a token
# If it isn't, it returns an error
@router.get('/check_token/{short_id}')
async def check_token(short_id: str = Path(...)):
    # Get the user from the database
    user_service = UserService()
    try:
      user = user_service.get_user_by_short_id(short_id)
      token = user['token']
    except Exception:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                          detail="Invalid token")
    # Check if the token is valid
    data:dict = verify_token(token)

    if data['code'] == 'token_valid':
        user_id = data['data']['user_id']
        # Return the token
        return {'user_id': user_id}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid token")


# Create a user ADMIN ONLY
@router.post('/create_token/{access_id}')
async def create_token(access_id: str = Path(...)):
    if access_id != 'HardAdminPa$$word': 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid acces id")
    # Create a new user
    user_service = UserService()
    user_id = str(user_service.create_user('sample_token').inserted_id)
    # Generate a token
    token = generate_token(user_id)
    # Update the token of the user
    short_id = str(ObjectId())

    user_service.update_user(user_id, token, short_id)
    # Return the token
    return {'token': short_id}
