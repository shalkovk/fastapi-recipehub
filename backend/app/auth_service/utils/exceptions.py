from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User already exists")

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Incorrect email or password"
)
