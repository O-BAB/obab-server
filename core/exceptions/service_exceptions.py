from rest_framework import status

from . import CustomAPIException


class UnknownException(CustomAPIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED
    _msg = ["UNKNOWN-EXCEPTION", "서버에서 알 수 없는 에러가 발생하였습니다."]


class UniqueValidationError(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    _msg = ["UNIQUE-VALIDATION-ERROR", "이미 중복된 정보가 있습니다."]


class InvalidRequest(CustomAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    _msg = ["INVALID-REQUEST", "인가되지 않은 접근입니다. 유저 토큰 혹은 요청 파라미터를 확인해주세요."]


class InvalidPagination(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    _msg = ["PAGINATION-INVALID", "요청 데이터 페이지가 초과하였습니다."]


class EmailRequiredToAuth(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    _msg = ["EMAIL-REQUIRED-TO-AUTH", "로그인을 위한 이메일 정보가 누락되었습니다."]


class JWTOutstandingNotFound(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    _msg = ["JWT-OUTSTANDING-NOT-FOUND", "JWT 토큰을 찾을 수 없습니다."]


class AccessTokenUnAuthorized(CustomAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    _msg = ["JWT-ACCESS-TOKEN-INVALID", "허용할 수 없는 토큰입니다."]


class RefreshTokenUnAuthorized(CustomAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    _msg = ["JWT-REFRESH-TOKEN-INVALID", "허용할 수 없는 토큰입니다."]


class UserNotFound(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    _msg = ["USER-NOT-FOUND", "유저를 찾을 수 없습니다."]


class UserAlreadyExists(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    _msg = ["USER-ALREADY-EXISTS", "이미 존재하는 계정 정보입니다."]


class UserPasswordInvalid(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    _msg = ["USER-PASSWORD-INVALID", "입력하신 비밀번호가 잘못되었습니다."]


class UserIsNotAuthorized(CustomAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    _msg = ["USER-NOT-AUTHORIZED", "차단되었거나 활성화되지 않은 유저입니다."]


class RecipeNotFound(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    _msg = ["Recipes-NOT-FOUND", "레시피를 찾을 수 없습니다."]