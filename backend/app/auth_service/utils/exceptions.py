from fastapi import status, HTTPException
# TokenNoFound, NoJwtException, TokenExpiredException, NoUserIdException, ForbiddenException, UserNotFoundException


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User already exists")

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

TokenNotFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found in header")

NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

NoUserIdException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User id not found")

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
